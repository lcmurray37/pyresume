import json
import argparse
import re
from pathlib import Path

from pylatex import Command, Document, NoEscape, Package, Section, Subsection

def escape_latex_chars(text: str) -> str:
    """Escapes special LaTeX characters to prevent compilation crashes."""
    if not isinstance(text, str):
        return text
    conv = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}', '\\': r'\textbackslash{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

def build_pdf(json_path: str, output_name: str = "resume_customized_final"):
    # 1. Load Data Dynamically from JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        resume = json.load(f)

    doc = Document()

    # Document setup
    doc.packages.append(Package("geometry", options="margin=0.7in"))
    doc.packages.append(Package("parskip"))
    doc.packages.append(Package("setspace"))
    doc.packages.append(Package("enumitem"))
    doc.packages.append(Package("inputenc", options="utf8"))

    doc.preamble.append(NoEscape(r"\setstretch{0.88}"))
    doc.preamble.append(NoEscape(r"\setcounter{secnumdepth}{0}"))
    doc.preamble.append(NoEscape(r"\setlist[itemize]{noitemsep,topsep=0pt,leftmargin=*}"))

    # Title
    doc.preamble.append(Command("title", escape_latex_chars(resume.get("name", "Name Missing"))))
    doc.preamble.append(Command("date", ""))
    doc.append(NoEscape(r"\maketitle"))

    # Contact Information
    with doc.create(Section("Contact Information")):
        c = resume.get("contact", {})
        doc.append(
            NoEscape(
                rf"\textbf{{Email:}} {escape_latex_chars(c.get('email', ''))}\\"
                rf"\textbf{{Phone:}} {escape_latex_chars(c.get('phone', ''))}\\"
                rf"\textbf{{GitHub:}} {escape_latex_chars(c.get('github', ''))}\\"
            )
        )

    # Professional Summary
    summary = resume.get("summary", [])
    if summary:
        with doc.create(Section("Professional Summary")):
            doc.append(NoEscape(r"\begin{itemize}"))
            for line in summary:
                doc.append(NoEscape(r"\item " + escape_latex_chars(line)))
            doc.append(NoEscape(r"\end{itemize}"))

    # Experience (Updated to match your schema structure)
    experience = resume.get("experience", [])
    if experience:
        with doc.create(Section("Experience")):
            for job in experience:
                # Handles your specific nested dictionary structure safely
                heading = f"{job.get('company', '')} | {job.get('title', '')} | {job.get('dates', '')}"
                with doc.create(Subsection(escape_latex_chars(heading))):
                    for section_title, bullets in job.get("sections", {}).items():
                        doc.append(NoEscape(rf"\textbf{{{escape_latex_chars(section_title)}}}\\" ))
                        doc.append(NoEscape(r"\begin{itemize}"))
                        for bullet in bullets:
                            doc.append(NoEscape(r"\item " + escape_latex_chars(bullet)))
                        doc.append(NoEscape(r"\end{itemize}"))

    # Education
    education = resume.get("education", [])
    if education:
        with doc.create(Section("Education")):
            doc.append(NoEscape(r"\begin{itemize}"))
            for edu in education:
                doc.append(NoEscape(r"\item " + escape_latex_chars(edu)))
            doc.append(NoEscape(r"\end{itemize}"))

    # Core Competencies
    skills = resume.get("skills", {})
    if skills:
        with doc.create(Section("Core Competencies")):
            for category, skill_list in skills.items():
                doc.append(NoEscape(rf"\textbf{{{escape_latex_chars(category)}:}} {escape_latex_chars(skill_list)}\\" ))

    # Build PDF
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    for ext in [".aux", ".log", ".fls", ".fdb_latexmk"]:
        f = build_dir / f"{output_name}{ext}"
        if f.exists():
            f.unlink()

    output_path = build_dir / output_name
    doc.generate_pdf(filepath=str(output_path), clean_tex=True)
    print(f"✅ Successfully compiled: {output_path}.pdf")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile tailored JSON resume to LaTeX PDF.")
    parser.add_argument("-i", "--input", required=True, help="Path to the tailored JSON resume file.")
    parser.add_argument("-o", "--output", default="resume_customized_final", help="Output PDF filename (without extension).")
    
    args = parser.parse_args()
    build_pdf(args.input, args.output)