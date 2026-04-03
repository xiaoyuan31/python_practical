import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import os
import random
from PIL import Image, ImageTk
import requests
from io import BytesIO
from PIL import Image, ImageTk  # pip install pillow
import openai
from tkmacosx import Button 

# ---------- Set your OpenAI API key ----------
openai.api_key ="YOUR_OPENAI_API_KEY" 

# ---------- File to store personas ----------
DATA_FILE = "personas.json"

# Load existing personas
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        personas = json.load(f)
else:
    personas = []

# ---------- Role Colors ----------
role_colors = {
    "Hero": "#8ED081",
    "Villain": "#E57373",
    "Support": "#64B5F6",
    "Other": "#FFD54F"
}

avatar_folder = "avatars"
os.makedirs(avatar_folder, exist_ok=True)

def generate_avatar(name, role):
    """
    Generate a unique avatar via OpenAI's Images API.
    Returns the local filename path.
    """
    filename = os.path.join(avatar_folder, f"{name}.png")
    
    # if avatar already exists, reuse it
    if os.path.exists(filename):
        return filename

    prompt = f"A vibrant cartoon avatar of a {role} named {name}, front facing, colorful background"

    try:
        # using the new Images API
        result = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="256x256"
        )
        
        # get the Base64 image data
        image_b64 = result.data[0].b64_json
        image_bytes = BytesIO(base64.b64decode(image_b64))
        
        img = Image.open(image_bytes)
        img.save(filename)  # store locally
        return filename

    except Exception as e:
        print("Avatar generation failed:", e)
        # fallback: gray block
        fallback = Image.new("RGB", (256, 256), "#CCCCCC")
        fallback.save(filename)
        return filename


def load_avatar_tk(name, role):
    """
    Convert the generated avatar to a Tkinter PhotoImage.
    """
    path = generate_avatar(name, role)
    img = Image.open(path).resize((50, 50))
    return ImageTk.PhotoImage(img)

# ---------- AI Trait Generator ----------
def generate_traits(name, role):
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
        fallback_traits = ["Brave", "Clever", "Kind", "Mysterious", "Funny"]
        return ", ".join(fallback_traits[:3])

# ---------- GUI ----------
root = tk.Tk()
root.title("AI Persona List with Avatars")
root.geometry("600x450")

# ---------- Avatar Images ----------


# Keep reference to images to prevent garbage collection
avatar_images = []

# Treeview for personas (allows colors & images)
columns = ("Role", "Traits")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
tree.heading("Role", text="Role")
tree.heading("Traits", text="Traits")
tree.pack(pady=10, fill=tk.X)

# ---------- Functions ----------
def refresh_tree():
    tree.delete(*tree.get_children())
    for i, p in enumerate(personas):
        role_color = role_colors.get(p["role"], role_colors["Other"])
        tree.insert(
            "",
            tk.END,
            values=(p["role"], p["traits"]),
            text=p["name"],
            tags=(p["role"],)
        )
        avatar = load_avatar_tk(p['name'], p['role'])
       
        tk.Label(root, image=avatar).pack()
        tree.tag_configure(p["role"], background=role_color, foreground="black")
        
def add_persona():
    name = simpledialog.askstring("Name", "Enter persona name:")
    if not name:
        return
    role = simpledialog.askstring("Role", "Enter persona role (Hero/Villain/Support/Other):")
    if not role:
        role = "Other"
    description = simpledialog.askstring("Description", "Enter persona description (optional):")
    
    traits = generate_traits(name, role)
    
    persona = {
        "name": name,
        "role": role,
        "traits": traits,
        "description": description or ""
    }
    personas.append(persona)
    save_personas()
    refresh_tree()
    messagebox.showinfo("Added", f"Persona '{name}' added!\nTraits: {traits}")

def view_persona():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a persona to view.")
        return
    index = tree.index(selected[0])
    p = personas[index]
    info = f"Name: {p['name']}\nRole: {p['role']}\nTraits: {p['traits']}\nDescription: {p['description']}"
    messagebox.showinfo("Persona Details", info)

def delete_persona():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a persona to delete.")
        return
    index = tree.index(selected[0])
    confirm = messagebox.askyesno("Confirm Delete", f"Delete persona '{personas[index]['name']}'?")
    if confirm:
        personas.pop(index)
        save_personas()
        refresh_tree()

def save_personas():
    with open(DATA_FILE, "w") as f:
        json.dump(personas, f, indent=4)


avatar_folder = "avatars"
os.makedirs(avatar_folder, exist_ok=True)

# ---------- Buttons ----------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

Button(btn_frame, text="Add Persona", command=add_persona, width=130, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
Button(btn_frame, text="View Persona", command=view_persona, width=130, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete Persona", command=delete_persona, width=130, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)

refresh_tree()
root.mainloop()