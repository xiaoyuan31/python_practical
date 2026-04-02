from fpdf import FPDF

# Create PDF
pdf = FPDF()
pdf.add_page()

# Add local Arial Unicode font (normal style only)
pdf.add_font("ArialUnicode", "", "ArialUnicode.ttf", uni=True)
pdf.set_font("ArialUnicode", "", 12)

# ---------- Content ----------

# Title (larger font instead of bold)
pdf.set_font("ArialUnicode", "", 16)
pdf.cell(0, 10, "Job Description: AI / Machine Learning Engineer", ln=True, align="C")
pdf.ln(10)

pdf.set_font("ArialUnicode", "", 12)
pdf.cell(0, 8, "Company: TechNova Solutions", ln=True)
pdf.cell(0, 8, "Location: Remote", ln=True)
pdf.ln(5)

# Job Overview (larger font for heading)
pdf.set_font("ArialUnicode", "", 14)
pdf.cell(0, 8, "Job Overview:", ln=True)
pdf.set_font("ArialUnicode", "", 12)
overview = (
    "TechNova Solutions is seeking a motivated AI / Machine Learning Engineer "
    "to design, develop, and deploy intelligent solutions for our clients. "
    "The ideal candidate is passionate about AI, data analysis, and modern software development practices."
)
pdf.multi_cell(0, 7, overview)
pdf.ln(5)

# Key Responsibilities
pdf.set_font("ArialUnicode", "", 14)
pdf.cell(0, 8, "Key Responsibilities:", ln=True)
pdf.set_font("ArialUnicode", "", 12)
responsibilities = [
    "Develop and implement machine learning models and AI solutions.",
    "Write efficient, reusable code in Python, Java, and SQL.",
    "Collaborate with cross-functional teams to deliver data-driven insights.",
    "Work with cloud platforms and container technologies such as Docker.",
    "Participate in code reviews, testing, and debugging."
]
for r in responsibilities:
    pdf.multi_cell(0, 7, "- " + r)
pdf.ln(5)

# Required Skills
pdf.set_font("ArialUnicode", "", 14)
pdf.cell(0, 8, "Required Skills:", ln=True)
pdf.set_font("ArialUnicode", "", 12)
skills = ["Python", "Java", "SQL", "Machine Learning / AI", "Data Analysis",
          "Communication skills", "Teamwork", "Cloud computing", "Docker"]
for skill in skills:
    pdf.multi_cell(0, 7, "- " + skill)
pdf.ln(5)

# Preferred Qualifications
pdf.set_font("ArialUnicode", "", 14)
pdf.cell(0, 8, "Preferred Qualifications:", ln=True)
pdf.set_font("ArialUnicode", "", 12)
preferred = [
    "Experience with deep learning frameworks (TensorFlow, PyTorch)",
    "Understanding of software development lifecycle",
    "Strong analytical and problem-solving skills"
]
for p in preferred:
    pdf.multi_cell(0, 7, "- " + p)
pdf.ln(5)

# Education
pdf.set_font("ArialUnicode", "", 14)
pdf.cell(0, 8, "Education:", ln=True)
pdf.set_font("ArialUnicode", "", 12)
pdf.multi_cell(0, 7, "- Bachelor’s degree in Computer Science, Engineering, or related field")
pdf.ln(5)

# Experience
pdf.set_font("ArialUnicode", "", 14)
pdf.cell(0, 8, "Experience:", ln=True)
pdf.set_font("ArialUnicode", "", 12)
pdf.multi_cell(0, 7, "- 2+ years in AI or Data Analysis projects")

# Save PDF
pdf.output("job_description.pdf")
print("✅ job_description.pdf created successfully with UTF-8 support on macOS!")