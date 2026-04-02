from fpdf import FPDF

# Initialize PDF
pdf = FPDF()
pdf.add_page()

# ---------- Fonts ----------
pdf.add_font("ArialUnicode", "", "ArialUnicode.ttf", uni=True)
pdf.set_font("ArialUnicode", size=12)

# Page width minus margins
page_width = pdf.w - 2 * pdf.l_margin

# ---------- Header ----------
pdf.set_font("ArialUnicode", size=16)
pdf.cell(0, 10, "Xiao Yuan", ln=True, align="C")
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "AI Developer | Python & Machine Learning Specialist", ln=True, align="C")
pdf.ln(8)

# Contact Info (emoji safe)
pdf.set_font("ArialUnicode", size=12)
contact_info = "Myanmar | xiaoyuan@example.com | +95 9xxxxxxx | LinkedIn: linkedin.com/in/xiaoyuan"
pdf.multi_cell(page_width, 7, contact_info)
pdf.ln(5)

# ---------- Professional Summary ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Professional Summary:", ln=True)
pdf.set_font("ArialUnicode", size=12)
summary = (
    "Passionate AI Developer with experience in machine learning, deep learning, "
    "and data analysis. Skilled in Python, Java, and SQL, with experience building "
    "AI-driven applications and integrating cloud-based solutions. Strong problem-solving "
    "skills with a focus on delivering scalable and efficient AI solutions."
)
pdf.multi_cell(page_width, 7, summary)
pdf.ln(5)

# ---------- Skills ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Skills:", ln=True)
pdf.set_font("ArialUnicode", size=12)
skills = [
    "Programming Languages: Python, Java, SQL",
    "Machine Learning: Scikit-learn, TensorFlow, PyTorch",
    "Data Analysis & Visualization: Pandas, NumPy, Matplotlib, Seaborn",
    "Cloud & DevOps: AWS, Docker, Git",
    "Soft Skills: Problem Solving, Team Collaboration, Communication"
]
for s in skills:
    pdf.multi_cell(page_width, 7, "- " + s)
pdf.ln(5)

# ---------- Professional Experience ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Professional Experience:", ln=True)
pdf.set_font("ArialUnicode", size=12)
experience = [
    ("AI Developer | LunaTech Solutions — Myanmar | Jan 2024 – Present", [
        "Developed and deployed machine learning models for predictive analytics and recommendation systems.",
        "Built Python pipelines for data preprocessing and feature engineering.",
        "Integrated AI services into web and mobile applications, reducing processing time by 30%.",
        "Collaborated with cross-functional teams to design scalable AI solutions."
    ]),
    ("Junior AI Developer | DataNova AI — Remote | Jun 2022 – Dec 2023", [
        "Implemented NLP and computer vision models for client projects.",
        "Assisted in data collection, cleaning, and labeling for ML training.",
        "Wrote reusable Python modules for AI algorithms and model evaluation.",
        "Participated in code reviews and optimized model performance by 20%."
    ])
]
for role, points in experience:
    pdf.multi_cell(page_width, 7, role)
    for p in points:
        pdf.multi_cell(page_width, 7, "- " + p)
    pdf.ln(3)
pdf.ln(5)

# ---------- Education ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Education:", ln=True)
pdf.set_font("ArialUnicode", size=12)
education = [
    "Diploma in Artificial Intelligence — University of Information Technology (UIT), Myanmar | 2023 – 2024",
    "B.Sc. in Computer Science — University of Yangon, Myanmar | 2019 – 2023"
]
for e in education:
    pdf.multi_cell(page_width, 7, "- " + e)
pdf.ln(5)

# ---------- Projects ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Projects:", ln=True)
pdf.set_font("ArialUnicode", size=12)
projects = [
    "AI Task Manager – Python, Tkinter, Scikit-learn: Desktop app prioritizing tasks using ML-based sentiment scoring.",
    "Personal News / Price Alchemist – Python, OpenAI API: Tool to summarize news and track price changes.",
    "LunaStay Hotel Booking App – Kotlin (Android), PHP, MySQL: Designed AI-powered hotel room recommendations."
]
for p in projects:
    pdf.multi_cell(page_width, 7, "- " + p)
pdf.ln(5)

# ---------- Certifications ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Certifications:", ln=True)
pdf.set_font("ArialUnicode", size=12)
certifications = [
    "Applied Information Technology Engineer (AP ITPEC) – Expected 2026",
    "Python for Data Science – Coursera"
]
for c in certifications:
    pdf.multi_cell(page_width, 7, "- " + c)
pdf.ln(5)

# ---------- Languages ----------
pdf.set_font("ArialUnicode", size=14)
pdf.cell(0, 8, "Languages:", ln=True)
pdf.set_font("ArialUnicode", size=12)
languages = ["English – Professional", "Myanmar – Native"]
for l in languages:
    pdf.multi_cell(page_width, 7, "- " + l)

# ---------- Save PDF ----------
pdf.output("ai_developer_cv.pdf")
print("✅ ai_developer_cv.pdf created successfully with full Unicode support!")