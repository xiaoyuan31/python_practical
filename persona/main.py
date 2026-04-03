import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random 
from tkmacosx import Button
import openai

# ---------- Set your OpenAI API key ----------
openai.api_key = "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"  # <-- Replace with your API key


# ---------- File to store personas ----------
DATA_FILE = "personas.json"

# Load existing personas
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        personas = json.load(f)
else:    personas = []

# ---------- AI Trait Generator ----------
def generate_ai_traits(name, role):
    prompt = (
        f"Generate 3–5 unique personality traits for a fictional character.\n"
        f"Name: {name}\nRole: {role}\n"
        f"Return only a comma-separated list of traits."
    )
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0.7
        )
        traits = response.choices[0].text.strip()
        return traits
    except Exception as e:
        print("AI Error:", e)
        # Fallback to random traits
        fallback_traits = ["Brave", "Clever", "Kind", "Mysterious", "Funny"]
        return ", ".join(fallback_traits[:3])

# ---------- AI-like trait generator (placeholder) ----------
def generate_traits(name, role):
    traits_pool = [
        "Brave", "Clever", "Kind", "Mysterious", "Funny",
        "Serious", "Creative", "Loyal", "Energetic", "Curious",
        "Wise", "Adventurous", "Charming", "Cautious", "Optimistic",
        "Pessimistic", "Confident", "Shy", "Ambitious", "Relaxed",
        "Intelligent", "Resourceful", "Empathetic", "Determined", "Friendly"
    ]
    return ", ".join(random.sample(traits_pool, 3))

# ---------- GUI ----------
root = tk.Tk()
root.title("Persona List Manager")
root.geometry("400x500")

# Listbox to display personas
persona_listbox = tk.Listbox(root, width=50, height=20)
persona_listbox.pack(pady=20)

# Display personas in the listbox
def refresh_persona_list():
    persona_listbox.delete(0, tk.END)
    for i, persona in enumerate(personas):
        persona_listbox.insert(tk.END, f"{i+1}. {persona['name']} ({persona['role']})")
   
refresh_persona_list()

# ---------- Functions ----------
def add_persona():
    name = simpledialog.askstring("Input", "Enter persona name:")
    if not name:
        messagebox.showerror("Error", "Name cannot be empty!")
        return
    
    role = simpledialog.askstring("Input", "Enter persona role:")
    if not role:
        messagebox.showerror("Error", "Role cannot be empty!")
        return
    
    # traits = generate_traits(name, role)

    # AI generates traits
    traits = generate_ai_traits(name, role)
    
    description = simpledialog.askstring("Description", "Enter persona description (optional):")
    new_persona = {
        "name": name,
        "role": role,
        "traits": traits,
        "description": description if description else ""
    }
    
    personas.append(new_persona)
    save_personas()
    refresh_persona_list()
    messagebox.showinfo("Success", f"Persona '{name}' added with traits: {traits}")

def view_persona():
    selected = persona_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No persona selected!")
        return
    
    index = selected[0]
    persona = personas[index]
    info = f"Name: {persona['name']}\nRole: {persona['role']}\nTraits: {persona['traits']}\nDescription: {persona['description']}"
    messagebox.showinfo("Persona Details", info)

def delete_persona():
    selected = persona_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No persona selected!")
        return
    
    index = selected[0]
    persona_name = personas[index]['name']
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{persona_name}'?"):
        del personas[index]
        save_personas()
        refresh_persona_list()
        messagebox.showinfo("Deleted", f"Persona '{persona_name}' has been deleted.")

def save_personas():
    with open(DATA_FILE, "w") as f:
        json.dump(personas, f, indent=4)

# ---------- Buttons ----------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

Button(root, text="Add Persona", command=add_persona, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
Button(root, text="View Persona", command=view_persona, bg="#2196F3", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
Button(root, text="Delete Persona", command=delete_persona, bg="#f44336", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

root.mainloop()