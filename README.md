# Advanced Calculator (Design Patterns + pandas + CI)

## Overview
A modular command-line calculator that supports:
- REPL interface (continuous input until exit)
- Operations: add(+), sub(-), mul(*), div(/), pow(^), root
- History stored in a pandas DataFrame and persisted to CSV
- Undo/redo via Memento snapshots
- Observers for logging / autosave behavior
- CI with GitHub Actions enforcing **100% test coverage**

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
