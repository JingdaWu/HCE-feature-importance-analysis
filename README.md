# AI Agent-Aided Research System

An autonomous research pipeline that uses 7 specialized AI agents to produce
publication-ready academic papers. Fork this template to start a new paper.

Part of [AIDER — AI-Driven Energy Research](https://ai-driven-energy-research.github.io/).

## Quick Start

### Prerequisites

- [Claude Code CLI](https://github.com/anthropics/claude-code) installed
- Python 3.10+
- LaTeX distribution (texlive recommended)
- `poppler-utils` (for PDF analysis: `apt install poppler-utils`)

### 1. Fork This Template

Click **"Use this template"** on GitHub to create your own repository.

### 2. Set Up Your Paper

```bash
# Interactive mode (recommended):
python3 setup.py

# Or quick mode:
python3 setup.py \
    --name "my_paper" \
    --journal "Applied Energy" \
    --topic "Neural network surrogate for heat exchanger design" \
    --gap "No existing surrogate captures turbulent regime transitions" \
    --methods "Physics-informed neural network with boundary layer constraints"
```

This creates the project structure, seeds `plan.md` with your input, then runs
the Director and Librarian to complete the research plan.

### 3. Start the Production Loop

```bash
python3 watcher.py
```

The watcher orchestrates the agent rotation automatically. It runs forever until
you press Ctrl+C. Drop instructions into `reviews/USER_REVIEW.md` at any time
to redirect all agents.

## License

- **Paper** (`paper/`): CC-BY 4.0
- **Code** (`code/`): MIT License
- **Data** (`data/`): See `data/README.md`
