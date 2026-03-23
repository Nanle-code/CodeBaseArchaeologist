# Codebase Archaeologist - GitLab Duo Custom Agent

**GitLab AI Hackathon 2026 Project** | Deadline: March 25, 2026

> **Answering the fundamental question: "Why does this code look like this?"**

A specialized GitLab Duo Custom Agent that traces git history, issues, MR discussions, and CI failures to provide comprehensive explanations of code decisions and architectural patterns.

---

## 🎯 The Problem

Every developer has asked: *"Why is this timeout set to 47000?"* or *"Why does this file look like this?"*

Traditional approaches require manually digging through:
- Git commit history and messages
- Issue threads and merge request discussions  
- CI/CD pipeline logs and failures
- Code review comments and decisions

This investigation is time-consuming and context is often lost.

---

## 🚀 The Solution

**Codebase Archaeologist** - A native GitLab Duo Custom Agent that automates codebase investigation using a three-agent methodology:

### 🔍 Three-Agent Methodology

1. **Git History Agent** - Analyzes commit chronology, author patterns, and evolution
2. **Issues & MR Agent** - Investigates discussions, reviews, and decision context
3. **CI Failure Agent** - Examines pipeline constraints and technical limitations
4. **Synthesis Agent** - Combines all evidence into coherent narratives

### 🏗️ Architecture

```
User Question → GitLab Duo Flow → Parallel Agent Analysis → Synthesized Answer
                    ↓
            ┌─────────────────────────────────┐
            │     archaeologist-flow.yaml     │
            └─────────────────────────────────┘
                    ↓
    ┌─────────────┬─────────────┬─────────────┐
    │ Git History │ Issues & MR │ CI Failures │
    │   Agent     │   Agent     │   Agent     │
    └─────────────┴─────────────┴─────────────┘
                    ↓
            ┌─────────────────────────────────┐
            │      Evidence Synthesis        │
            │      (Comprehensive Answer)     │
            └─────────────────────────────────┘
```

---

## 🛠️ Implementation

### Files Created

```
.gitlab/
├── agents/
│   └── archaeologist/
│       └── config.yaml          # Agent configuration & persona
└── flows/
    └── archaeologist-flow.yaml  # Three-agent orchestration

AGENTS.md                          # Agent behavior & usage guide
README.md                          # This file
```

### Key Features

- **Native GitLab Integration** - No external APIs, uses GitLab's built-in tools
- **Pattern Recognition** - Identifies scaffold-then-fix, refactoring, bug-driven development
- **Evidence-Based Analysis** - Every conclusion backed by specific commits, issues, or pipeline data
- **Digital Archaeologist Persona** - Methodical, storytelling approach

---

## 🎪 Demo Scenario

### The Perfect Test Case

This repository demonstrates a classic **"scaffold-then-fix"** pattern:

```bash
git log --oneline --all
1f02ae9 Add missing publishConfig          # March 20, 2026
9f5b8c4 Fix some wrong options in package.json  # March 20, 2026  
a0ffaa7 Add usage example                   # March 20, 2026
1bb58c3 Initial commit                       # March 20, 2026
```

### Sample Questions

**Q**: "Why is publishConfig missing from the initial commit?"

**A**: The publishConfig was missing from the initial commit because this follows a classic "scaffold-then-fix" development pattern. The repository was created with three commits on March 20, 2026:

1. **Initial commit** (1bb58c3): Basic package scaffolding with essential fields
2. **Fix some wrong options** (9f5b8c4): Corrected package.json configuration issues  
3. **Add missing publishConfig** (1f02ae9): Added the missing publishConfig for npm publishing

This pattern shows the author started with a basic scaffold, then rapidly refined the configuration in follow-up commits. The publishConfig was added last because it's typically configured after the basic package structure is verified.

---

## 💡 Hackathon Innovation

### The Challenge We Solved

**Problem**: No Anthropic API credits ❌  
**Traditional Solution**: External AI API calls 💰  
**Our Solution**: Native GitLab Duo Custom Agent ✅

### Why This Matters

1. **No External Dependencies** - Works entirely within GitLab ecosystem
2. **Cost Effective** - Uses included GitLab Ultimate features
3. **Privacy Focused** - No data leaves GitLab infrastructure
4. **Native Integration** - Seamless developer experience

### Technical Achievement

- ✅ **GitLab Duo Agent Platform** - Custom agent with advanced orchestration
- ✅ **Three-Agent Pattern** - Parallel processing and synthesis
- ✅ **Flow-Based Architecture** - Reproducible investigation methodology
- ✅ **Pattern Recognition** - Identifies common development workflows

---

## 🚀 Getting Started

### Prerequisites

- GitLab Ultimate trial (30-day active)
- Project with GitLab Duo enabled
- Repository with git history

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://gitlab.com/Nanle-code/redux-mock-store.git
   ```

2. **Copy agent configuration** to your project:
   ```bash
   cp -r .gitlab/agents/archaeologist /path/to/your/project/.gitlab/agents/
   cp -r .gitlab/flows/archaeologist-flow.yaml /path/to/your/project/.gitlab/flows/
   ```

3. **Commit and push** to enable the agent

### Usage

1. **Open GitLab Duo Chat** in your project
2. **Select "Archaeologist"** agent from dropdown
3. **Ask questions** like:
   - "Why is this timeout set to 47000?"
   - "Why does this file look like this?"
   - "Why was this feature implemented this way?"

---

## 🔧 Development Pipeline

For demonstration purposes, we also built a Python pipeline that shows the same methodology:

```bash
cd ~/Desktop/Hackathon/codebase-archaeologist
python3 archaeologist.py package.json "Why is publishConfig missing?"
```

**Note**: This demonstrates the concept but requires Anthropic API credits. The GitLab Duo agent solves this limitation.

---

## 📊 Supported Patterns

### Development Patterns We Recognize

- 🏗️ **Scaffold-Then-Fix** - Initial setup → Rapid refinement → Final state
- 🔄 **Incremental Refactoring** - Large codebase → Small targeted changes
- 🐛 **Bug-Driven Development** - Bug report → Fix → Test → Documentation
- ⚡ **Performance Optimization** - Issue → Benchmarking → Optimization
- 🔒 **Security Hardening** - Concern → Fix → Security tests

### Question Types

- **Configuration**: "Why is this timeout set to 47000?"
- **Architecture**: "Why does this file look like this?"  
- **Historical**: "Why was this feature implemented this way?"
- **Pattern**: "Why are there so many small commits for this feature?"

---

## 🏆 Hackathon Impact

### Innovation Score

- **Technical Novelty**: ⭐⭐⭐⭐⭐ Native GitLab Duo Agent Platform usage
- **Practical Utility**: ⭐⭐⭐⭐⭐ Solves real developer pain point
- **Hackathon Spirit**: ⭐⭐⭐⭐⭐ Creative solution to API limitation
- **Presentation Value**: ⭐⭐⭐⭐⭐ Visual demo with clear before/after

### Demo Strategy

1. **Problem Introduction** - Show the investigation challenge
2. **Python Demo** - Working pipeline hitting API limits  
3. **Solution Reveal** - GitLab Duo Custom Agent
4. **Live Demo** - Agent answering questions about this repo
5. **Technical Deep Dive** - Architecture and methodology

---

## 🔮 Future Roadmap

### Version 2.0 Features

- [ ] **Multi-Repository Analysis** - Cross-project dependency tracing
- [ ] **Team Pattern Recognition** - Identify team-specific workflows
- [ ] **Automated Documentation** - Generate architecture docs
- [ ] **Integration with IDE** - VS Code / JetBrains extensions
- [ ] **Performance Metrics** - Codebase health scoring

### Enterprise Features

- [ ] **Compliance Analysis** - SOC2 / GDPR impact tracing
- [ ] **Security Audit Trail** - Vulnerability decision documentation
- [ ] **Cost Analysis** - Technical debt quantification
- [ ] **Onboarding Assistant** - New developer codebase orientation

---

## 🤝 Contributing

We welcome contributions! Key areas:

1. **Pattern Recognition** - Add new development patterns
2. **Agent Improvements** - Better synthesis algorithms
3. **Integration** - More GitLab data sources
4. **Documentation** - Examples and case studies

### Development Setup

```bash
# Fork and clone
git clone https://gitlab.com/your-username/redux-mock-store.git

# Make changes
# Test with GitLab Duo Chat in your fork

# Submit merge request
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

*"Every line of code tells a story. We're here to help you read it."* 

**Codebase Archaeologist** - Understanding your codebase, one commit at a time.
