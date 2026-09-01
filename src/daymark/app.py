import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from .store import TaskStore


class TaskApp:
    def __init__(self, root: tk.Tk, store: TaskStore) -> None:
        self.root, self.store = root, store
        root.title("Daymark Tasks")
        root.geometry("680x450")
        self.title = tk.StringVar()
        self.priority = tk.StringVar(value="medium")
        self.search = tk.StringVar()
        self.show_done = tk.BooleanVar(value=True)
        form = ttk.Frame(root, padding=12); form.pack(fill="x")
        ttk.Entry(form, textvariable=self.title).pack(side="left", fill="x", expand=True)
        ttk.Combobox(form, textvariable=self.priority, values=("low", "medium", "high"), state="readonly", width=9).pack(side="left", padx=6)
        ttk.Button(form, text="Add task", command=self.add).pack(side="left")
        filters = ttk.Frame(root, padding=(12, 0)); filters.pack(fill="x")
        ttk.Label(filters, text="Search").pack(side="left")
        ttk.Entry(filters, textvariable=self.search).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Checkbutton(filters, text="Show completed", variable=self.show_done, command=self.refresh).pack(side="left")
        self.tree = ttk.Treeview(root, columns=("title", "priority", "status"), show="headings", selectmode="browse")
        for name, width in (("title", 380), ("priority", 90), ("status", 100)):
            self.tree.heading(name, text=name.title()); self.tree.column(name, width=width)
        self.tree.pack(fill="both", expand=True, padx=12, pady=10)
        actions = ttk.Frame(root, padding=(12, 0, 12, 12)); actions.pack(fill="x")
        ttk.Button(actions, text="Toggle done", command=self.toggle).pack(side="left")
        ttk.Button(actions, text="Delete", command=self.delete).pack(side="left", padx=6)
        self.search.trace_add("write", lambda *_: self.refresh())
        root.bind("<Return>", lambda _: self.add())
        root.bind("<Delete>", lambda _: self.delete())
        self.refresh()

    def selected_id(self) -> int | None:
        selected = self.tree.selection()
        return int(selected[0]) if selected else None

    def add(self) -> None:
        try: self.store.add(self.title.get(), self.priority.get())
        except ValueError as exc: messagebox.showerror("Cannot add task", str(exc)); return
        self.title.set(""); self.refresh()

    def toggle(self) -> None:
        task_id = self.selected_id()
        if task_id is None: return
        done = self.tree.item(str(task_id), "values")[2] == "Open"
        self.store.set_done(task_id, done); self.refresh()

    def delete(self) -> None:
        task_id = self.selected_id()
        if task_id is not None and messagebox.askyesno("Delete task", "Delete the selected task?"):
            self.store.delete(task_id); self.refresh()

    def refresh(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for task in self.store.list(self.search.get(), self.show_done.get()):
            self.tree.insert("", "end", iid=str(task.id), values=(task.title, task.priority.title(), "Done" if task.done else "Open"))


def main() -> None:
    store = TaskStore(Path.home() / ".daymark" / "tasks.db"); store.initialize()
    root = tk.Tk(); TaskApp(root, store); root.mainloop()


if __name__ == "__main__": main()

