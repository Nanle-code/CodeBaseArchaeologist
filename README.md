# Codebase Archaeologist

> Ask *why* your code looks the way it does. Get a real answer.

The Codebase Archaeologist is a multi-agent GitLab tool that traces any file
back through commit history, issues, MR discussions, and CI failures to
reconstruct the story of why code exists in its current form.

---

## Setup

### 1. Install dependencies
```bash
pip install requests anthropic python-dotenv
```

### 2. Configure credentials
```bash
cp .env.example .env
```

Edit `.env` and fill in:

| Variable | Where to find it |
|---|---|
| `GITLAB_TOKEN` | GitLab → Edit Profile → Access Tokens |
| `GITLAB_PROJECT_ID` | Your project's main page → Settings → General (or the number in any API URL) |
| `ANTHROPIC_API_KEY` | console.anthropic.com |

### 3. Find your Project ID
Go to your GitLab project. The ID is shown under the project name on the main page,
or visible in the URL of any API call. It's a number like `12345678`.

### 4. Test your connection
```bash
python test_connection.py
```

You should see your project name, default branch, and recent commits.

---

## Usage

```bash
python archaeologist.py <file_path> "<your question>"
```

### Examples

```bash
# Why does this specific value exist?
python archaeologist.py src/payments/processor.py "Why is the timeout set to 47000?"

# What happened to this file?
python archaeologist.py config/database.yml "Why are there so many retry settings?"

# Understanding a pattern
python archaeologist.py app/auth/session.py "Why is session management done this way?"
```

---

## Project structure

```
codebase-archaeologist/
├── archaeologist.py          # Main entry point (orchestrator + synthesis)
├── test_connection.py        # Day 1 sanity check
├── .env                      # Your credentials (never commit this)
├── .env.example              # Template
├── agents/
│   ├── git_history_agent.py  # Analyses commits and diffs
│   ├── issues_mr_agent.py    # Searches issues and MR discussions
│   └── ci_failure_agent.py   # Scans CI failure logs
└── tools/
    └── gitlab_client.py      # All GitLab API calls
```

---

## How it works

1. You ask a question about a file
2. The **orchestrator** dispatches 3 agents in parallel
3. **Git history agent** — fetches commits, diffs, and MR discussions for the file
4. **Issues & MR agent** — searches for issues mentioning the file or related concepts
5. **CI failure agent** — scans recent failed pipeline logs for references to the file
6. The **synthesis agent** weaves all findings into a single narrative answer

---

## Tips for good questions

- Be specific: *"Why is the timeout 47000?"* beats *"tell me about this file"*
- Name the thing you're confused about: *"Why is there a try/except here?"*
- Ask about patterns: *"Why is authentication handled in two different places?"*
