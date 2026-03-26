"""Tool for fetching PR details from Azure DevOps."""

from __future__ import annotations

import re
from typing import Any

from langchain_core.tools import tool

from src.agent.config import AgentConfig, load_config
from src.agent.state import PRContext
from src.tools.azure_devops.client import AzureDevOpsClient
from src.tools.git_diff import get_pr_diff
from src.utils.logging import get_logger

logger = get_logger("tools.fetch_pr")


def parse_pr_url(url: str) -> dict[str, str]:
    """Parse an Azure DevOps PR URL into its components.

    Supports URLs like:
    - https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{id}
    - https://{org}.visualstudio.com/{project}/_git/{repo}/pullrequest/{id}

    Returns:
        Dict with keys: org_url, project, repository_id, pull_request_id
    """
    # Pattern for dev.azure.com URLs
    ado_pattern = re.compile(
        r"https://dev\.azure\.com/(?P<org>[^/]+)/(?P<project>[^/]+)"
        r"/_git/(?P<repo>[^/]+)/pullrequest/(?P<pr_id>\d+)"
    )

    # Pattern for legacy visualstudio.com URLs
    vs_pattern = re.compile(
        r"https://(?P<org>[^.]+)\.visualstudio\.com/(?P<project>[^/]+)"
        r"/_git/(?P<repo>[^/]+)/pullrequest/(?P<pr_id>\d+)"
    )

    match = ado_pattern.match(url) or vs_pattern.match(url)
    if not match:
        raise ValueError(
            f"Invalid Azure DevOps PR URL: {url}. "
            "Expected format: https://dev.azure.com/{{org}}/{{project}}/_git/{{repo}}/pullrequest/{{id}}"
        )

    org = match.group("org")
    return {
        "org_url": f"https://dev.azure.com/{org}",
        "project": match.group("project"),
        "repository_id": match.group("repo"),
        "pull_request_id": match.group("pr_id"),
    }


@tool
def fetch_pr_details(
    pr_url: str | None = None,
    project: str | None = None,
    repository_id: str | None = None,
    pull_request_id: int | None = None,
) -> dict[str, Any]:
    """Fetch pull request details from Azure DevOps.

    Can be called with either a full PR URL or individual components.

    Args:
        pr_url: Full Azure DevOps PR URL (preferred).
        project: Azure DevOps project name.
        repository_id: Repository name or ID.
        pull_request_id: Pull request number.

    Returns:
        Dict containing PR details including title, author, changed files, and diffs.
    """
    config = load_config()

    if pr_url:
        parsed = parse_pr_url(pr_url)
        project = parsed["project"]
        repository_id = parsed["repository_id"]
        pull_request_id = int(parsed["pull_request_id"])
        # Override org URL from the parsed URL
        config.azure_devops_org_url = parsed["org_url"]

    if not all([project, repository_id, pull_request_id]):
        return {
            "success": False,
            "error": "Must provide either pr_url or all of: project, repository_id, pull_request_id",
        }

    assert repository_id is not None
    assert pull_request_id is not None

    logger.info(
        "fetching_pr",
        project=project,
        repo=repository_id,
        pr_id=pull_request_id,
    )

    try:
        client = AzureDevOpsClient(config)
        pr_context = client.build_pr_context(
            repository_id=repository_id,
            pull_request_id=pull_request_id,
            project=project,
        )

        # Fetch proper git diffs by cloning the repo
        diff_result = get_pr_diff(
            org_url=config.azure_devops_org_url,
            project=project or config.azure_devops_project,
            repository=repository_id,
            pat=config.azure_devops_pat,
            source_branch=pr_context.source_branch,
            target_branch=pr_context.target_branch,
        )

        if diff_result.success:
            pr_context.diffs = diff_result.diffs
        else:
            logger.warning("git_diff_failed", error=diff_result.error)
            pr_context.diffs = {}

        return {
            "success": True,
            "pr_context": pr_context.model_dump(),
        }

    except Exception as e:
        logger.error("fetch_pr_failed", error=str(e))
        return {"success": False, "error": str(e)}
