import argparse
import json
from datetime import date
from pathlib import Path

DEFAULT_FILE = Path("study_tasks.json")

def load_tasks(path):
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Task file contains invalid JSON: {error}") from error
    if not isinstance(data, list):
        raise ValueError("Task file must contain a JSON list.")
    return data

def save_tasks(path, tasks):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def add_task(path, title, subject, due):
    if not title.strip() or not subject.strip():
        raise ValueError("Task title and subject cannot be empty.")
    date.fromisoformat(due)
    tasks = load_tasks(path)
    task_id = max((int(task["id"]) for task in tasks), default=0) + 1
    tasks.append({"id": task_id, "title": title.strip(), "subject": subject.strip(),
                  "due": due, "done": False})
    save_tasks(path, tasks)
    return task_id

def list_tasks(path, show_all=False):
    tasks = load_tasks(path)
    if not show_all:
        tasks = [task for task in tasks if not task["done"]]
    if not tasks:
        print("No tasks to show.")
        return
    for task in sorted(tasks, key=lambda item: (item["done"], item["due"], item["id"])):
        status = "DONE" if task["done"] else "TODO"
        print(f"#{task['id']} [{status}] {task['due']} | {task['subject']} | {task['title']}")

def complete_task(path, task_id):
    tasks = load_tasks(path)
    for task in tasks:
        if int(task["id"]) == task_id:
            task["done"] = True
            save_tasks(path, tasks)
            print(f"Marked task #{task_id} as complete.")
            return
    raise ValueError(f"No task found with ID {task_id}.")

def main():
    parser = argparse.ArgumentParser(description="Organize study tasks from your terminal.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="JSON task file")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title")
    add.add_argument("--subject", required=True)
    add.add_argument("--due", required=True, help="Date in YYYY-MM-DD format")
    listing = sub.add_parser("list", help="List pending tasks")
    listing.add_argument("--all", action="store_true", help="Include completed tasks")
    done = sub.add_parser("done", help="Mark a task complete")
    done.add_argument("id", type=int)
    args = parser.parse_args()
    try:
        if args.command == "add":
            print(f"Added task #{add_task(args.file, args.title, args.subject, args.due)}.")
        elif args.command == "list":
            list_tasks(args.file, args.all)
        else:
            complete_task(args.file, args.id)
    except (ValueError, OSError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
