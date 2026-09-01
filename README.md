# Daymark Task Manager

A small desktop task manager built with Tkinter and SQLite. I made it to practice event-driven interfaces while keeping data local.

## Features

- Priorities, completion state, search, and filtering
- Keyboard shortcuts: Enter adds and Delete removes
- SQLite storage in `~/.daymark/tasks.db`
- Confirmation before deletion

## Run

```powershell
$env:PYTHONPATH = "src"
python -m daymark.app
```

Run tests with `python -m unittest discover -s tests -v`. A future version could add due dates and reminders.

