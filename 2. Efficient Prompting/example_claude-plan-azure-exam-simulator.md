# Azure Exam Simulator - Claude Code Plan Mode

> This document showcases Claude Code's **Plan Mode** feature. Before writing any code, Claude analyses the task, breaks it down into steps, defines the architecture, and presents the plan for approval. Only after the user confirms does Claude begin implementation. This ensures alignment before any code is written.

---

## Context

Create a .NET 10 console app that serves as an Azure certification exam simulator. The user has 5 ExamTopics PDF files containing exam questions for Microsoft Azure certifications. The app should extract questions from these PDFs into JSON files, then provide a terminal-based exam UI where users can select an exam, answer questions, see correct answers, and get a score.

## PDF Sources (1,551 pages total)

| Exam | File | Pages |
|------|------|-------|
| AI-102 | AI-102.pdf | 230 |
| AZ-204 | AZ-204 Full.pdf | 349 |
| AI-900 | AI-900 Full (1).pdf | 92 |
| AZ-104 | AZ-104 Full.pdf | 476 |
| AZ-400 | AZ-400 Full (1).pdf | 404 |

## Approach

### Step 1: Create .NET 10 Console App
- `dotnet new console` in `/Users/stephankroukamp/RiderProjects/AzureExamSimulator`
- Add `Spectre.Console` NuGet package for rich terminal UI
- Add `System.Text.Json` for JSON serialization

### Step 2: Extract Questions from PDFs into JSON

Use a Python extraction script (leveraging `pdfplumber` or similar) to:
1. Read each PDF page-by-page
2. Parse question text, options, correct answers, and explanations
3. Output one JSON file per exam into the app's `Data/` folder

**JSON Schema per exam:**
```json
{
  "examCode": "AI-102",
  "examTitle": "Azure AI Engineer Associate",
  "questions": [
    {
      "id": 1,
      "topic": "Topic 1",
      "type": "SingleChoice | MultipleChoice | TrueFalse",
      "questionText": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correctAnswers": ["C"],
      "explanation": "..."
    }
  ]
}
```

**Question types to support:**
- **SingleChoice**: Standard A/B/C/D with one correct answer
- **MultipleChoice**: Multiple correct answers (e.g., "choose two")
- **TrueFalse / YesNo**: Yes/No questions
- **DragDrop / Hotspot**: Simplified to text-based multiple choice since visual elements can't render in terminal

### Step 3: Build the Console UI with Spectre.Console

**App flow:**
1. **Welcome screen** - App title banner
2. **Exam selection** - Dropdown/selection prompt listing all 5 exams with question counts
3. **Exam mode selection** - "Practice mode" (show answer after each question) or "Exam mode" (show results at end)
4. **Question display** - Show question number, topic, question text, and options
5. **Answer input** - User selects answer(s) via arrow keys
6. **Feedback** - Show correct/incorrect with explanation (practice mode)
7. **Results screen** - Final score with pass/fail indicator, breakdown by topic

**Two exam modes:**
1. **Practice mode** - Show correct answer + explanation after each question, final score at end
2. **Timed exam mode** - Hide answers until the end, countdown timer (configurable), full results review at end

**UI features:**
- Color-coded feedback (green = correct, red = incorrect)
- Progress bar showing question N of total
- Countdown timer in exam mode (top-right corner)
- Ability to skip questions
- Navigation (next/previous)
- Score summary at the end with percentage and pass/fail (700/1000 passing)

### Step 4: Project Structure
```
AzureExamSimulator/
├── Program.cs              # Entry point, exam selection
├── Models/
│   ├── Exam.cs             # Exam model
│   ├── Question.cs         # Question model
│   └── ExamResult.cs       # Results tracking
├── Services/
│   ├── ExamLoader.cs       # Load JSON files
│   └── ExamRunner.cs       # Run exam session with UI
├── Data/
│   ├── AI-102.json
│   ├── AZ-204.json
│   ├── AI-900.json
│   ├── AZ-104.json
│   └── AZ-400.json
└── AzureExamSimulator.csproj
```

### Step 5: Make it Zero-Config
- JSON files embedded as content files (CopyToOutputDirectory)
- No external dependencies beyond NuGet packages
- `dotnet run` just works

## Implementation Order
1. Create project scaffolding + NuGet references
2. Define models (Exam, Question, ExamResult)
3. Build ExamLoader service
4. Build ExamRunner service with Spectre.Console UI
5. Write Program.cs entry point
6. Extract questions from all 5 PDFs into JSON (most time-consuming step - 1,551 pages)
7. Test with `dotnet run`

## Verification
- `dotnet build` succeeds
- `dotnet run` launches, shows exam selector
- Each exam loads questions from its JSON file
- User can answer questions and see scores
- No config or setup needed beyond `dotnet run`

## Key Files to Create
- `AzureExamSimulator.csproj`
- `Program.cs`
- `Models/Exam.cs`
- `Models/Question.cs`
- `Models/ExamResult.cs`
- `Services/ExamLoader.cs`
- `Services/ExamRunner.cs`
- `Data/*.json` (5 exam files)
