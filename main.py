#!/usr/bin/env python3
import argparse
import sqlite3
from datetime import datetime

DB = "tasks.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tasks "
        "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER DEFAULT 0, created_at TEXT)"
    )
    return conn


def add_task(title):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO tasks (title, created_at) VALUES (?, ?)",
            (title, datetime.now().isoformat()),
        )
    print(f"Added: {title}")


def list_tasks(show_all=False):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, done, created_at FROM tasks"
            + ("" if show_all else " WHERE done = 0")
            + " ORDER BY id"
        ).fetchall()
    if not rows:
        print("No tasks found.")
        return
    for row in rows:
        status = "✓" if row[2] else "○"
        print(f"[{status}] {row[0]}. {row[1]}  ({row[3][:10]})")


def complete_task(task_id):
    with get_conn() as conn:
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    print(f"Marked task {task_id} as done.")


def delete_task(task_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    print(f"Deleted task {task_id}.")


def main():
    parser = argparse.ArgumentParser(description="Task CLI — simple SQLite task list")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title", nargs="+", help="Task title")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Include completed tasks")

    p_done = sub.add_parser("done", help="Mark task as done")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int)

    args = parser.parse_args()
    if args.cmd == "add":
        add_task(" ".join(args.title))
    elif args.cmd == "list":
        list_tasks(args.all)
    elif args.cmd == "done":
        complete_task(args.id)
    elif args.cmd == "delete":
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
