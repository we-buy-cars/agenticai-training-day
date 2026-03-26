WE BUY CARS  ·  BUSINESS ANALYST TEAM
Claude for Business Analysts
Your practical guide to saving time and doing better work with AI

Claude can be configured to understand your team's tools, formats, and ways of working. The more context you give it  about your organisation, your processes, and what you need  the more useful it becomes. Think of it as a highly capable assistant that gets better the more you brief it.

1.  Core Use Cases for BAs

Writing User Stories
One of the most time-consuming parts of our job is writing User Stories in the right format. Claude handles this instantly just describe the requirement.
You can get consistent, perfectly formatted User Stories every time by setting up instructions in your Claude project. Claude will reference these instructions automatically every time you ask it to draft a story.
Instructions you can use to generate User Stories with Claude:
Instructions to paste into your Claude project:
You are a Business Analyst assistant helping me draft User Stories. Every User Story I ask you to create must follow this exact format:

TITLE: A clear, concise title that describes what needs to be done.
DESCRIPTION: A short paragraph (3–5 sentences) that provides context of what the problem is and what needs to be done at a high level. Do not repeat or preview the steps below.
STEPS: Step-by-step instructions for what needs to be built or done. Each step must be a clear, actionable instruction. No duplication of anything already said in the Description. Be specific — avoid vague terms like "make it work" or "fix it".
•	ACCEPTANCE CRITERIA: This section tells testers exactly what to test and what the expected outcome is. Only include sub-sections where there is relevant content — never force a section if there is nothing meaningful to say. Always include at minimum: what must be tested and the expected outcome. Include the following sub-sections where applicable:
•	WHAT MUST BE TESTED: List success conditions and failure/edge conditions. For each, state the condition and the expected outcome. This section is always required.
•	WHAT MUST NOT BE TESTED: Anything explicitly out of scope. Only include if there is a genuine risk of a tester testing something that does not belong to this story.
•	FUNCTIONAL CRITERIA: Specific behaviours, rules and logic the system must perform. Format: "The system must [action] when [condition]." Only include if there are clear functional rules to enforce.
•	NON-FUNCTIONAL CRITERIA: Usability, accessibility, compatibility or reliability requirements. Only include if specific standards apply.
•	PERFORMANCE CRITERIA: Measurable speed or load expectations. Only include if performance is a concern for this story.
•	PRIMARY ACTOR(S): The main user(s) or system(s) who trigger or interact with this feature. Include when actors are relevant to understanding the scope of testing.
•	SECONDARY ACTOR(S): Any other users or systems indirectly involved. Only include if secondary actors exist.
•	ACTOR ROLES & PERMISSIONS: For each actor, describe their access level and what they can or cannot do. Only include if roles and permissions are relevant to what is being tested.
•	DEVIATIONS FROM CURRENT DESIGN: If an existing feature or screen has changed, describe what it was before and what it is now. Only include if something has changed.
•	Additional rules: Always write in English (UK). If I give you the requirement in Afrikaans, translate it first then apply the format. If I give you multiple requirements, draft each one as a separate User Story. Ask me to clarify if anything is too vague. Never include a sub-section with no content — leave it out entirely rather than writing "N/A". Use simple, plain language. Keep stories short and to the point.

Try this prompt:
Draft a user story: Users on the WBC website must be able to save a vehicle to a favourites list so they can come back to it later.

•	Title
•	Description
•	What to do
•	Acceptance Criteria

Claude also works in Afrikaans — it translates your input and applies the exact same format:

Afrikaans example:
Skep 'n user story: Gebruikers moet 'n voertuig aan hulle gunsteling-lys kan byvoeg op die WBC webwerf.

Creating Azure DevOps Work Items
Once you are happy with a User Story, push it directly into Azure DevOps without leaving Claude. The Preview → Confirm → Create flow means nothing is created until you approve it.

Try this prompt:
Create a User Story in Azure DevOps:  Title: Save vehicle to favourites list Description: Users on the WBC website must be able to save a vehicle to a favourites list to revisit later. Product: WBC Website

What happens automatically:
•	Claude suggests the Product Owner, Department and Sponsor
•	Acceptance Criteria is generated for the DevOps ticket
•	A full preview appears first — review everything before it is submitted
•	Only after you confirm does the item get created in Azure DevOps

Extracting Stories from Documents
Upload any requirements document  a BRD, meeting notes, or an email  and ask Claude to extract User Stories directly. What used to take half a day now takes two minutes.

Try this prompt:
Please read this document and extract all the requirements as separate User Stories using my standard format.

Quick Practical Tasks
A few more things Claude handles easily:
•	Summarise this document in 5 bullet points.
•	Rewrite this in simpler language for a non-technical stakeholder: "The API endpoint must validate the JWT token on every request before processing the payload."
•	Create a Word document: a one-page meeting agenda template for BA stakeholder sessions. Include sections for attendees, discussion points, decisions and actions.

2.  Prompting Tips To Get Better Results

The single most important rule: the more context you give Claude, the better the output. Think of it like briefing a new team member  the more background you provide, the better their work will be.

❌  Vague (Don't do this)	✅  Specific (Do this)
Make me a ticket	Create a User Story for the Pricing product. Users must be able to filter by make and model on the WBC app.
Fix this	Rewrite this description in plain English for a non-technical audience.
Summarise	Summarise this in 3 bullet points focused on what the BA team needs to action.


3.  The Biggest Opportunity Most BAs Miss

The thing BAs use least but would benefit from most is using Claude as a thinking partner — not just a drafting tool. Try these:
Remember
Claude won't replace what you do as a BA — it handles the repetitive formatting and drafting so you can focus on the thinking and the stakeholder work. The more you use it, the better you will get at prompting it.
