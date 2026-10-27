# Python Study Planner

A command-line planner that stores study tasks in a local JSON file.

## Features
- Add tasks with a subject and due date
- List pending tasks or all tasks
- Mark tasks complete
- Sort by status and due date
- Automated unit tests
- No third-party dependencies

## Requirements
Python 3.10+.

## Usage
```bash
python study_planner.py add "Revise BFS" --subject AI --due 2026-10-30
python study_planner.py list
python study_planner.py done 1
python study_planner.py list --all
```
Use a different data file:
```bash
python study_planner.py --file data/tasks.json list
```
Dates use `YYYY-MM-DD`.

## Tests
```bash
python -m unittest -v
```
