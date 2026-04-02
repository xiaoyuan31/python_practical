import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import matplotlib.pyplot as plt
from tkmacosx import Button

# Sample skill database
skills_db = ["python", "java", "sql", "machine learning", "ai", "data analysis", "communication", "teamwork", "cloud", "docker"]

# ---------------- AI / Scoring ----------------
def analyze_text(text):
    text = text.lower()
    found_skills = [skill for skill in skills_db if skill in text]
    return found_skills

def calculate_fit(resume_skills, job_skills):
    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]

    fit = int(len(matched) / len(job_skills) * 100) if job_skills else 0

    suggestions = []
    if len(missing) > 0:
        suggestions.append("- Focus on acquiring missing skills")
    if len(resume_skills) < 3:
        suggestions.append("- Add more skills or projects")

    return fit, matched, missing, suggestions

# ---------------- GUI Logic ----------------
resume_path = ""
job_path = ""

def upload_resume():
    global resume_path
    resume_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if resume_path:
        resume_label.config(text=f"📄 Resume: {resume_path.split('/')[-1]}")

def upload_job():
    global job_path
    job_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if job_path:
        job_label.config(text=f"📄 Job Description: {job_path.split('/')[-1]}")

def analyze_match():
    if not resume_path or not job_path:
        messagebox.showwarning("Warning", "Upload both Resume and Job Description PDFs")
        return

    # Extract resume text
    with open(resume_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text() + " "

    # Extract job description text
    with open(job_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        job_text = ""
        for page in reader.pages:
            job_text += page.extract_text() + " "

    resume_skills = analyze_text(resume_text)
    job_skills = analyze_text(job_text)

    fit, matched, missing, suggestions = calculate_fit(resume_skills, job_skills)

    # Display text result
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)

    result_text.insert(tk.END, f"📊 Job Fit: {fit}%\n\n", "score")

    result_text.insert(tk.END, "✅ Skills Matched:\n", "header")
    for skill in matched:
        result_text.insert(tk.END, f"- {skill}\n", "found")

    result_text.insert(tk.END, "\n❌ Missing Skills:\n", "header")
    for skill in missing:
        result_text.insert(tk.END, f"- {skill}\n", "missing")

    result_text.insert(tk.END, "\n💡 Suggestions:\n", "header")
    for sug in suggestions:
        result_text.insert(tk.END, f"{sug}\n", "suggestion")

    result_text.config(state="disabled")

    # Show pie chart
    # labels = ["Matched", "Missing"]
    # sizes = [len(matched), len(missing)]
    # colors = ["#00ff00", "#ff4d4d"]
    # plt.figure(figsize=(4,4))
    # plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    # plt.title("Skill Match Overview")
    # plt.show()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("📝 AI Job-Matching Resume Analyzer")
root.geometry("700x750")
root.configure(bg="#1e1e1e")

tk.Label(root, text="📝 AI Job-Matching Resume Analyzer", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)

Button(root, text="📁 Upload Resume PDF", command=upload_resume, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
resume_label = tk.Label(root, text="📄 Resume: Not Uploaded", bg="#1e1e1e", fg="white")
resume_label.pack(pady=5)

Button(root, text="📁 Upload Job Description PDF", command=upload_job, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
job_label = tk.Label(root, text="📄 Job Description: Not Uploaded", bg="#1e1e1e", fg="white")
job_label.pack(pady=5)

Button(root, text="🔍 Analyze Fit", command=analyze_match, bg="#FF9800", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(frame, width=80, height=25, bg="#2b2b2b", fg="white", font=("Arial", 10), yscrollcommand=scrollbar.set)
result_text.pack()
scrollbar.config(command=result_text.yview)

# Tag colors
result_text.tag_config("found", foreground="#00ff00")
result_text.tag_config("missing", foreground="#ff4d4d")
result_text.tag_config("suggestion", foreground="#ffd700")
result_text.tag_config("header", foreground="#00ffff", font=("Arial", 11, "bold"))
result_text.tag_config("score", foreground="#00ffcc", font=("Arial", 12, "bold"))

result_text.config(state="disabled")

root.mainloop()