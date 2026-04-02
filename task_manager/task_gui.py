import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from tkmacosx import Button  # Use tkmacosx for better button support on MacOS

# ---------- Task Manager with Canvas (MacOS-friendly) ----------

TASK_FILE = "tasks.json"
tasks = []
IMPORTANT_WORDS = ["exam", "deadline", "urgent", "project", "assignment", "meeting"]

# ---------- Functions ----------

def auto_priority(text):
    text = text.lower()
    for word in IMPORTANT_WORDS:
        if word in text:
            return 1
    return 0


def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def load_tasks():
    global tasks
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r") as f:
                tasks = json.load(f)
        except:
            tasks = []
    refresh_canvas()


def sort_tasks():
    def get_deadline(task):
        if task.get("deadline"):
            try:
                return datetime.strptime(task["deadline"], "%Y-%m-%d")
            except:
                return datetime.max
        return datetime.max

    tasks.sort(key=lambda x: (x["done"], -x.get("priority", 0), get_deadline(x)))


def get_status(task):
    if not task.get("deadline"):
        return ""
    try:
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
        today = datetime.today()
        if deadline.date() < today.date():
            return "⚠️ Overdue"
        elif deadline.date() == today.date():
            return "⏰ Today"
        else:
            return f"📅 {task['deadline']}"
    except:
        return ""


def refresh_canvas():
    sort_tasks()
    canvas.delete("all")

    y = 10
    for idx, t in enumerate(tasks):
        text = t['task']
        color = "white"
        if t.get('priority', 0) == 1:
            text = "⭐️ " + text

        status = get_status(t)
        if status:
            text += f" ({status})"

        if t['done']:
            text += " 🎉"
            color = "gray"

        # Draw text on canvas
        canvas.create_text(10, y, anchor='nw', text=text, fill=color, font=("Arial", 12), tags=(f"task{idx}",))
        y += 30


def add_task():
    text = entry.get().strip()
    deadline = deadline_entry.get().strip()

    if text == "":
        messagebox.showwarning("Warning", "Enter a task")
        return

    if deadline == "":
        deadline = ""
    else:
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except:
            messagebox.showwarning("Error", "Use YYYY-MM-DD")
            return

    priority = auto_priority(text)

    tasks.append({
        "task": text,
        "done": False,
        "priority": priority,
        "deadline": deadline
    })

    entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    save_tasks()
    refresh_canvas()


def mark_done():
    selected_idx = get_selected_task()
    if selected_idx is not None:
        tasks[selected_idx]['done'] = True
        save_tasks()
        refresh_canvas()


def mark_priority():
    selected_idx = get_selected_task()
    if selected_idx is not None:
        tasks[selected_idx]['priority'] = 1
        save_tasks()
        refresh_canvas()


def delete_task():
    selected_idx = get_selected_task()
    if selected_idx is not None:
        del tasks[selected_idx]
        save_tasks()
        refresh_canvas()


def get_selected_task():
    # get selected task based on last click
    if hasattr(canvas, 'selected_idx'):
        return canvas.selected_idx
    else:
        messagebox.showwarning("Warning", "Select a task by clicking on it")
        return None


def on_canvas_click(event):
    y_click = event.y
    index = y_click // 30  # each row height = 30
    if index >= len(tasks):
        return
    canvas.selected_idx = index
    refresh_canvas()
    # highlight selected
    canvas.create_rectangle(0, index*30, 480, index*30 + 30, tags=(f"highlight{index}",), fill="green", outline="")
    text = tasks[index]['task']
    if tasks[index].get('priority',0)==1:
        text = "🌟 " + text
    status = get_status(tasks[index])
    if status:
        text += f" ({status})"
    if tasks[index]['done']:
        text += " 🎊"
    canvas.create_text(10, index*30 + 10, anchor='nw', text=text, fill="white", font=("Arial", 12))


# ---------- UI ----------
root = tk.Tk()
root.title("Smart Task Manager - Canvas Version")
root.geometry("480x520")
root.configure(bg="#1e1e2f")

# Title
label = tk.Label(root, text="Smart Task Manager", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white")
label.pack(pady=10)

# Entry fields
entry = tk.Entry(root, width=35, font=("Arial", 12), bg="#2c2c3e", fg="white", insertbackground="white")
entry.pack(pady=5)

deadline_entry = tk.Entry(root, width=35, font=("Arial", 12), bg="#2c2c3e", fg="white", insertbackground="white")
deadline_entry.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=10)

btn_style = {"font": ("Arial", 10, "bold"), "width": 12}

add_btn = Button(btn_frame, text="Add", command=add_task, bg="#4CAF50", fg="white")
add_btn.grid(row=0, column=0, padx=5, pady=5)
done_btn = Button(btn_frame, text="Done", command=mark_done, bg="#2196F3", fg="white")
done_btn.grid(row=0, column=1, padx=5, pady=5)
priority_btn = Button(btn_frame, text="High Priority", command=mark_priority, bg="#FF9800", fg="white")
priority_btn.grid(row=1, column=0, padx=5, pady=5)
del_btn = Button(btn_frame, text="Delete", command=delete_task, bg="#F44336", fg="white")
del_btn.grid(row=1, column=1, padx=5, pady=5)

# Canvas for tasks
canvas = tk.Canvas(root, width=480, height=300, bg="#2c2c3e")
canvas.pack(pady=10)
canvas.bind("<Button-1>", on_canvas_click)

entry.bind("<Return>", lambda e: add_task())

load_tasks()
root.mainloop()