from pathlib import Path

from pylatex import (
    Command,
    Document,
    NoEscape,
    Package,
    Section,
    Subsection,
)

from resume_data import resume

# -----------------------
# Document setup
# -----------------------

doc = Document()

# Packages
doc.packages.append(Package("geometry", options="margin=0.7in"))
doc.packages.append(Package("parskip"))
doc.packages.append(Package("setspace"))
doc.packages.append(Package("enumitem"))
doc.packages.append(Package("inputenc", options="utf8"))

# Formatting
doc.preamble.append(NoEscape(r"\setstretch{0.88}"))
doc.preamble.append(NoEscape(r"\setcounter{secnumdepth}{0}"))
doc.preamble.append(
    NoEscape(
        r"\setlist[itemize]{noitemsep,topsep=0pt,leftmargin=*}"
    )
)

# -----------------------
# Title
# -----------------------

doc.preamble.append(Command("title", resume["name"]))
doc.preamble.append(Command("date", ""))

doc.append(NoEscape(r"\maketitle"))

# -----------------------
# Contact Information
# -----------------------

with doc.create(Section("Contact Information")):
    c = resume["contact"]

    doc.append(
        NoEscape(
            rf"\textbf{{Email:}} {c['email']}\\"
            rf"\textbf{{Phone:}} {c['phone']}\\"
            rf"\textbf{{GitHub:}} {c['github']}\\"
        )
    )

# -----------------------
# Professional Summary
# -----------------------

with doc.create(Section("Professional Summary")):

    doc.append(NoEscape(r"\begin{itemize}"))

    for line in resume["summary"]:
        doc.append(NoEscape(r"\item " + line))

    doc.append(NoEscape(r"\end{itemize}"))

# -----------------------
# Experience
# -----------------------

with doc.create(Section("Experience")):

    for job in resume["experience"]:

        heading = (
            f"{job['company']} | "
            f"{job['title']} | "
            f"{job['dates']}"
        )

        with doc.create(Subsection(heading)):

            for section, bullets in job["sections"].items():

                doc.append(
                    NoEscape(
                        rf"\textbf{{{section}}}\\"
                    )
                )

                doc.append(NoEscape(r"\begin{itemize}"))

                for bullet in bullets:
                    doc.append(
                        NoEscape(
                            r"\item " + bullet
                        )
                    )

                doc.append(NoEscape(r"\end{itemize}"))

# -----------------------
# Education
# -----------------------

with doc.create(Section("Education")):

    doc.append(NoEscape(r"\begin{itemize}"))

    for edu in resume["education"]:
        doc.append(NoEscape(r"\item " + edu))

    doc.append(NoEscape(r"\end{itemize}"))

# -----------------------
# Core Competencies
# -----------------------

with doc.create(Section("Core Competencies")):

    for category, skills in resume["skills"].items():

        doc.append(
            NoEscape(
                rf"\textbf{{{category}:}} {skills}\\"
            )
        )

# -----------------------
# Build PDF
# -----------------------

build_dir = Path("build")
build_dir.mkdir(exist_ok=True)

# Remove stale latexmk files
for ext in [".aux", ".log", ".fls", ".fdb_latexmk"]:
    f = build_dir / f"resume_customized_final{ext}"

    if f.exists():
        f.unlink()

doc.generate_pdf(
    filepath=str(build_dir / "resume_customized_final"),
    clean_tex=True,
)