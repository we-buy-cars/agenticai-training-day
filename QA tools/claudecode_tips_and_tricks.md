# AI-Assisted QA: Tips & Tricks

A practical guide for QA testers — from manual to senior automation. These are patterns we use daily on real projects, not theory. By the end you'll know how to turn test ideas into running scripts, write prompts that produce consistent results, debug flaky tests fast, and explore pages systematically before writing a single assertion.

---

## Section 1: From Manual to Automated

**You already know how to test it — now let Claude Code write the script.**

Manual testers carry deep product knowledge. Claude Code bridges the gap between "I know what to check" and "I have a runnable Playwright script." You describe the test in plain English; Claude Code produces a working script that plugs into the team's shared framework automatically.

### Example Prompt

```
Write a test that logs into Nex, navigates to lead 71071437,
clicks the Finance tab, and verifies the finance wizard loads
with 7 steps. Use nexus_helpers for login and navigation.
```

### What Claude Code Produces

```python
from claude._shared.nexus_helpers import ni, navigate_to_lead, click_tab

def test_finance_wizard_loads(logged_in_page):
    page = logged_in_page
    navigate_to_lead(page, "71071437")
    assert click_tab(page, "Finance"), "Finance tab not found"

    # Verify all 7 wizard steps are visible
    steps = page.locator("mat-step-header")
    steps.first.wait_for(state="visible", timeout=10000)
    assert steps.count() == 7, f"Expected 7 steps, got {steps.count()}"
```

Notice what you *didn't* have to do:
- Set up the browser, login flow, or session management — `conftest.py` handles that
- Figure out how to click Angular tabs — `click_tab()` already knows the `<li>` regex pattern
- Write screenshot-on-failure logic — the `auto_screenshot_on_failure` fixture runs automatically

> **Why this works:** Our `CLAUDE.md` file tells Claude Code about every shared helper. When you say "use nexus_helpers," it knows `navigate_to_lead()` takes a page and lead ID, `click_tab()` takes a tab name, and `ni()` handles Angular's never-ending network activity. The framework does the heavy lifting.

### Test Data Without the Guesswork

Need a complete applicant for a finance form? One function generates everything:

```python
from claude._shared.data_generators import generate_applicant_data

applicant = generate_applicant_data()
# Returns 28 fields ready to use:
#   id_number    -> valid 13-digit SA ID (correct Luhn checksum)
#   mobile       -> valid SA prefix + 7 digits
#   first_name, surname, email, province, city, suburb,
#   gross_income, net_income, deposit, employer_name, ...
```

No more inventing fake data that fails validation. The ID numbers pass Luhn checks, the phone numbers have real SA prefixes, and income figures are realistic ranges.

---

## Section 2: Prompt Engineering for QA

**Context + intent + constraints = dramatically better output.**

The difference between a vague prompt and a precise one is the difference between "close but needs rework" and "copy-paste and run."

### Weak vs. Strong Prompt

**Weak:**
```
Write a test for the filter page.
```
This gives Claude Code almost nothing — which page? Which filters? What should pass or fail?

**Strong:**
```
Write a Filter V3 test for the Auction List page at
/sales/auction-list. The page has these filters: Stock No,
Description, Branch. Each filter opens a mat-dialog when
clicked. Test that:
1. Each filter chip is visible and clickable
2. The search field inside the dialog works
3. Clicking CANCEL closes the dialog without applying
4. The clear (X) button on Stock No resets the filter

Follow the CDK overlay safety rules from CONVENTIONS.md —
dismiss with CANCEL not APPLY, and clean up overlays between
tests.
```

### Why the Strong Version Works

| Element | What it does |
|---------|-------------|
| **URL** | Claude Code navigates to the right page |
| **Filter names** | Assertions target real elements, not guesses |
| **Specific behaviors** | Each test has a clear pass/fail condition |
| **CONVENTIONS.md reference** | Triggers CDK overlay safety patterns automatically |

> **Why this works:** Our project encodes QA rules in `CLAUDE.md` (7 rules covering directory structure, test format, QA checklists) and `CONVENTIONS.md` (Angular CDK safety, dialog dismissal patterns, API capture). Claude Code reads these files and applies the rules *every time* — so every team member gets consistent output, not just whoever remembers the gotchas.

### The CLAUDE.md Advantage

When Claude Code reads our `CLAUDE.md`, it enforces rules like:
- **Rule 6**: Every ticket directory must have `conftest.py`, `test_*.py`, `screenshots/`, and `test_results_summary.txt`
- **Rule 9**: New user stories get a filtered QA checklist (forms, auth, file uploads, API, security — only relevant sections)
- **CDK safety**: Always dismiss filter dialogs with CANCEL (APPLY with empty arrays causes 400 errors)

These rules are *encoded*, not tribal knowledge. A junior tester's first prompt gets the same structural quality as a senior's.

---

## Section 3: Debugging & Fixing Failures Fast

**Paste the error + code, get a diagnosis and fix.**

Flaky tests are the #1 time sink in automation. Claude Code excels at pattern-matching failures to known root causes — especially when it has access to your project's documented gotchas.

### Example Prompt

```
This test fails intermittently with TimeoutError on the
residential address field. Here's the error and test code:

  TimeoutError: locator.fill: Timeout 30000ms exceeded.
  Call log:
    waiting for get_by_role("textbox", name="Enter a location")

The page uses Google Places autocomplete for the address.
```

### Real Gotchas We've Solved This Way

**1. The `ni()` helper — Angular SPA networkidle never completes**

Angular SPAs poll constantly, so Playwright's `networkidle` wait hangs forever. Claude Code identified this pattern across multiple tests and created a try/except fallback:

```python
def ni(page, timeout=8000):
    """networkidle with timeout fallback — Angular SPA never truly idle."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeoutError:
        pass  # Good enough — the page is usable
```

Every test uses `ni()` instead of raw `wait_for_load_state`. Solved once, reused everywhere.

**2. CDK overlay backdrop blocking clicks**

Angular Material dropdowns (`mat-select`) leave an invisible `cdk-overlay-backdrop` layer that intercepts all clicks. Tests pass individually but fail when run together.

Fix: navigate fresh between tests, or remove the overlay via JS:
```python
page.evaluate("document.querySelector('.cdk-overlay-backdrop')?.remove()")
```

**3. Google Places flaky at 40% failure rate**

`get_by_role("textbox", name="Enter a location")` depends on external Google Maps JS loading — unreliable. Switched to the raw DOM selector:
```python
# Flaky (depends on Google JS):
page.get_by_role("textbox", name="Enter a location")

# Stable (targets the HTML input directly):
page.locator('[id="addressSearch"]')
```

> **Why this works:** Each of these gotchas was solved once, documented in `CONVENTIONS.md`, and never rediscovered. When you paste an error, Claude Code checks these patterns first — you get the fix in seconds instead of hours of debugging.

---

## Section 4: Exploratory Testing with AI Assistance

**Inventory the page before writing tests — discover what's there, then decide what to test.**

Exploration is often ad-hoc: click around, take notes, miss things. Our `/explore` pattern makes it systematic — generate a script that logs in, navigates, and dumps every interactive element, API call, and DOM structure.

### Example Prompt

```
Explore the cancellation task list page at
/sales/cancellation-task-list. List all interactive elements,
filter chips, table columns, and any API calls made on load.
I need to know what's testable before I write the test plan.
```

### What Exploration Scripts Do

The generated explore script uses Playwright's `page.evaluate()` to introspect the live DOM:

```python
# Discover all interactive elements on the page
buttons = page.get_by_role("button").all()
textboxes = page.get_by_role("textbox").all()
comboboxes = page.get_by_role("combobox").all()

for btn in buttons:
    if btn.is_visible():
        print(f"  Button: {btn.inner_text().strip()}")

# Capture API calls during page load
captured, handler = start_api_capture(page, ["api/", "Sales/"])
page.reload()
ni(page)
stop_api_capture(page, handler)
for call in captured:
    print(f"  {call['method']} {call['url']} -> {call['status']}")
```

### Real Example: Document Upload Discovery

An explore script for the Doc Vals tab discovered:
- `mat-expansion-panel` containers for each document category
- Hidden `input#fileDropRef` elements for file upload slots
- Button states (enabled/disabled) that depend on workflow stage
- API calls to `/PartialApplication/` and `/DocumentValidation/` on tab load

This turned a 30-minute manual walkthrough into a 2-minute script run with complete, repeatable output.

> **Why this works:** No more "I missed that button" or "I didn't know that API call happened." Exploration becomes systematic: run the script, review the output, decide what to test. Junior testers get the same complete picture as someone who's been on the project for months.

---

## Quick Reference Card

### Prompt Templates

**1. Generate a test** (Section 1)
```
Write a test that [action sequence]. Verify [expected outcome].
Use [specific helpers] from the shared modules.
```

**2. Detailed test spec** (Section 2)
```
Write a test for [page] at [URL]. The page has [elements].
Test that: 1) [behavior] 2) [behavior] 3) [behavior].
Follow [specific convention] from CONVENTIONS.md.
```

**3. Debug a failure** (Section 3)
```
This test fails with [error type] on [element/action].
Here's the error output and test code: [paste both].
The page uses [relevant technology/pattern].
```

**4. Explore a page** (Section 4)
```
Explore [page name] at [URL]. List all interactive elements,
filters, table columns, and API calls on load. I need to
know what's testable before writing the test plan.
```

### Three Golden Rules

1. **Be specific about what you see** — Include the URL, element names, filter labels, and error messages. Claude Code works with what you give it.

2. **Reference the project conventions** — Mention `CONVENTIONS.md`, `CLAUDE.md`, or specific helpers by name. This activates the patterns the team has already solved and documented.

3. **Start with exploration, then test** — Run a discovery pass first. You'll write fewer tests that cover more ground, and you won't miss hidden elements or API calls.
