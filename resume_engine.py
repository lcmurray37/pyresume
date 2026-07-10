import re
from typing import List, Dict
from pydantic import BaseModel, Field
from openai import OpenAI
from pylatex import Document, Package, Section, NoEscape, Command

DEFAULT_MODEL = "gpt-4o-mini"

# ==========================================
# SCHEMA DEFINITIONS FOR STRUCTURED OUTPUTS
# ==========================================
class ContactInfo(BaseModel):
    email: str
    phone: str
    github: str

class ResumeSchema(BaseModel):
    name: str
    contact: ContactInfo
    summary: List[str]
    experience: List[Dict[str, List[str]]] = Field(
        description="List of roles, where each dict has a job title as a key and a list of bullet points as the value."
    )

def escape_latex_chars(text: str) -> str:
    """Utility function to prevent LaTeX compilation errors."""
    if not isinstance(text, str):
        return text
    conv = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}', '\\': r'\textbackslash{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

# ==========================================
# RESUME TAILORING FUNCTION
# ==========================================
def tailor_resume_data(client: OpenAI, job_description: str, base_resume: dict, model_name: str = DEFAULT_MODEL) -> ResumeSchema:
    """
    Inputs a job description and base resume schema, 
    and returns a structured object matching ResumeSchema.
    """
    prompt = f"""
    You are an expert technical resume writer. Rewrite and tailor the provided resume data 
    to match the target Job Description.

    CRITICAL RULES:
    1. Do NOT change company names, job titles, universities, degrees, or dates.
    2. Modify the 'summary' and the bullet points under experience to highlight key skills requested in the job description.
    3. Keep descriptions accurate, professional, and crisp. Do not use markdown.
    """

    response = client.beta.chat.completions.parse(
        model=model_name,
        response_format=ResumeSchema,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"[JOB DESCRIPTION]\n{job_description}\n\n[BASE RESUME DATA]\n{base_resume}"}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.parsed

def generate_latex_source(resume_data: ResumeSchema) -> str:
    """Builds the PyLaTeX document structure dynamically."""
    doc = Document()

    # Document & Package Setup
    for pkg, options in [("geometry", "margin=0.7in"), ("inputenc", "utf8")]:
        doc.packages.append(Package(pkg, options=options))
    for pkg in ["parskip", "setspace", "enumitem"]:
        doc.packages.append(Package(pkg))

    # Line formatting & spacing metrics
    doc.preamble.append(NoEscape(r"\setstretch{0.88}"))
    doc.preamble.append(NoEscape(r"\setcounter{secnumdepth}{0}"))
    doc.preamble.append(NoEscape(r"\setlist[itemize]{noitemsep,topsep=0pt,leftmargin=*}"))

    # Header / Title Block
    doc.preamble.append(Command("title", escape_latex_chars(resume_data.name)))
    doc.preamble.append(Command("date", ""))
    doc.append(NoEscape(r"\maketitle"))

    # Contact Details Section
    with doc.create(Section("Contact Information")):
        c = resume_data.contact
        doc.append(NoEscape(
            rf"\textbf{{Email:}} {escape_latex_chars(c.email)}\\"
            rf"\textbf{{Phone:}} {escape_latex_chars(c.phone)}\\"
            rf"\textbf{{GitHub:}} {escape_latex_chars(c.github)}\\"
        ))

    # Professional Summary Section
    with doc.create(Section("Professional Summary")):
        doc.append(NoEscape(r"\begin{itemize}"))
        for line in resume_data.summary:
            doc.append(NoEscape(r"\item " + escape_latex_chars(line)))
        doc.append(NoEscape(r"\end{itemize}"))

    # Work Experience Section
    with doc.create(Section("Work Experience")):
        for job in resume_data.experience:
            for section_title, bullets in job.items():
                doc.append(NoEscape(r"\textbf{" + escape_latex_chars(section_title) + r"}\\"))
                doc.append(NoEscape(r"\begin{itemize}"))
                for bullet in bullets:
                    doc.append(NoEscape(r"\item " + escape_latex_chars(bullet)))
                doc.append(NoEscape(r"\end{itemize}"))

    return doc.dumps()