# Dracary

An AI agent for generating task plans.

## Installation

### Method 1: Using uv (Recommended)

1. Install uv:

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Clone the repository:

3. Create a new virtual environment and activate it:

```bash
uv venv --python 3.12
# on Windows:
.venv\Scripts\activate
```

4. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## Configuration

1. Create and edit `config/config.toml` file.

## Quick Start

```bash
python main.py
```

## Roadmap

1. **Task Execution**: Implement the ability to execute generated plans and track their progress.
