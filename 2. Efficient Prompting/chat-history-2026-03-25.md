# Chat History - 2026-03-25

## Building an Exam Simulator .NET App with Claude Code

> This chat log demonstrates efficient prompting — building a full application with Claude in just a few prompts.

---

### Prompt 1 (Previous Session)

**User:**
> *Uploaded 6 PDF files:*
> - AZ-204 Full.pdf
> - AI-900 Full (1).pdf
> - AZ-104 Full.pdf
> - AI-102.pdf
> - AZ-400 Full (1).pdf
>
> Create a new dotnet 10 console app that runs and displays a test exam UI
>
> Attached is 5 PDF's for each of the different Microsoft AZ exams. Please transcribe the PDF to text and use the JSON files as databases. Then render a dropdown to choose which exam you want to write. And then display a nice exam UI that uses can answers questions. See the correct answers etc, commit the JSON files and use them for the specific test wanted to be rendered. The app must be able to just dotnet run and no config needed extra.

**Claude:**
Let me start by understanding the structure of each PDF exam file.

*Read all 5 PDF files to understand the exam question formats.*

Good, I now understand all 5 PDF formats. They're all ExamTopics-style PDFs with varying structures. Let me check the page counts and then write the plan.

*Ran 4 commands to check page counts and .NET availability.*

Now I have all the details. Total: 1,551 pages across 5 PDFs. .NET 10 is available. Let me write the plan.

*Created a plan file and began implementation.*

Plan is ready. Visual questions will be simplified to text-based format, and both practice mode and timed exam mode will be supported.

*Claude then proceeded to build the entire application — transcribing all 5 PDFs into JSON question banks, creating a .NET 10 console app with a terminal UI featuring exam selection, question navigation, answer checking, score tracking, and review functionality. The app was built to just `dotnet run` with no configuration needed.*

---

### Prompt 2 (This Session)

**User:**
> continue

**Claude:**
It looks like this is the start of our conversation, so I don't have any previous context to continue from. Could you let me know what you'd like me to help with? I'm ready to assist with coding, research, Azure DevOps, document creation, or any other task you have in mind.

---

### Prompt 3

**User:**
> you were busy creating a exam simulator dotnet app for me

**Claude:**
Let me check what's already in the workspace from our previous session.

*Claude searched the project directory for existing solution files, project files, and IDE configuration folders to understand the current state of the app.*

---

### Prompt 4

**User:**
> make it so that it can be debugged in vs code please and all popular IDEs, vs (windows) vs code, rider etc

**Claude:**
*Claude attempted to inspect the project structure to determine what IDE debug/launch configurations were needed (VS Code `.vscode/launch.json`, Visual Studio `.sln` / `launchSettings.json`, JetBrains Rider `.idea` run configs). The command was rejected by the user due to permission settings.*

---

### Prompt 5

**User:**
> Continue from where you left off.

**Claude:**
*Waiting for tool availability to resume the task.*
