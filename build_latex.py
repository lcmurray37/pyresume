from pylatex import Document, Section, Subsection, Command, NoEscape
from resume_data import resume

# -----------------------
# Document setup
# -----------------------
doc = Document()

# Page + spacing tuning (resume density)
doc.packages.append(NoEscape(r"\usepackage[margin=0.7in]{geometry}"))
doc.packages.append(NoEscape(r"\usepackage{parskip}"))
doc.packages.append(NoEscape(r"\usepackage{setspace}"))
doc.packages.append(NoEscape(r"\usepackage{enumitem}"))
doc.packages.append(NoEscape(r"\setstretch{0.88}"))

# Remove numbering
doc.preamble.append(NoEscape(r"\setcounter{secnumdepth}{0}"))

# Make lists tight globally
doc.preamble.append(NoEscape(r"\setlist[itemize]{noitemsep, topsep=0pt, leftmargin=*}"))

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

    doc.append(NoEscape(r"\textbf{Email: } " + c["email"] + r"\\"))
    doc.append(NoEscape(r"\textbf{Phone: } " + c["phone"] + r"\\"))
    doc.append(NoEscape(r"\textbf{GitHub: } " + c["github"] + r"\\"))

# -----------------------
# Professional Summary (bullets)
# -----------------------
with doc.create(Section("Professional Summary")):
    doc.append(NoEscape(r"\begin{itemize}"))
    for line in resume["summary"]:
        doc.append(NoEscape(r"\item " + line))
    doc.append(NoEscape(r"\end{itemize}"))

# -----------------------
# Experience (FULL RESTORED CONTENT)
# -----------------------
with doc.create(Section("Experience")):

    # -------- TECHNOMICS --------
    with doc.create(Subsection("TECHNOMICS, INC. | Senior Analyst | Aug 2021 – Present")):

        doc.append(NoEscape(r"\textbf{Project Management & Leadership:}\\"))
        doc.append(NoEscape(r"\begin{itemize}"))
        doc.append(NoEscape(r"\item Led enterprise data science and analytics initiatives for federal, defense, and international clients."))
        doc.append(NoEscape(r"\item Managed Agile/Kanban teams of up to 14+ members."))
        doc.append(NoEscape(r"\item Directed sprint planning, code reviews, and technical mentorship."))
        doc.append(NoEscape(r"\end{itemize}"))

        doc.append(NoEscape(r"\textbf{Data Science & Engineering:}\\"))
        doc.append(NoEscape(r"\begin{itemize}"))
        doc.append(NoEscape(r"\item Migrated legacy MS Access systems to DuckDB and R-based pipelines."))
        doc.append(NoEscape(r"\item Optimized SQL/R queries and validated data pipelines for modeling accuracy."))
        doc.append(NoEscape(r"\item Built prioritization models using Python and Palantir Foundry."))
        doc.append(NoEscape(r"\item Automated Excel-heavy reporting workflows using R and Python."))
        doc.append(NoEscape(r"\item Implemented Git/GitLab version-controlled data extraction workflows."))
        doc.append(NoEscape(r"\item Developed BI dashboards tracking cost growth and engineering change trends."))
        doc.append(NoEscape(r"\end{itemize}"))

        doc.append(NoEscape(r"\textbf{Training & Organizational Impact:}\\"))
        doc.append(NoEscape(r"\begin{itemize}"))
        doc.append(NoEscape(r"\item Led Data & Analytics certification program for ~1,200 personnel."))
        doc.append(NoEscape(r"\item Developed training modules in statistical sampling and enterprise data systems."))
        doc.append(NoEscape(r"\end{itemize}"))

    # -------- KCIC --------
    with doc.create(Subsection("KCIC, LLC | Senior Data Analyst | Mar 2019 – Aug 2021")):

        doc.append(NoEscape(r"\textbf{Database Engineering & Analytics:}\\"))
        doc.append(NoEscape(r"\begin{itemize}"))
        doc.append(NoEscape(r"\item Built optimized SQL views, stored procedures, and indexes improving query performance."))
        doc.append(NoEscape(r"\item Developed SQL + Excel reporting pipelines for large claims datasets."))
        doc.append(NoEscape(r"\item Designed validation systems ensuring data integrity under strict deadlines."))
        doc.append(NoEscape(r"\end{itemize}"))

        doc.append(NoEscape(r"\textbf{Process Improvement & Training:}\\"))
        doc.append(NoEscape(r"\begin{itemize}"))
        doc.append(NoEscape(r"\item Standardized analytics training programs across analyst teams."))
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
    for k, v in resume["skills"].items():
        doc.append(NoEscape(r"\textbf{" + k + r": } " + v + r"\\"))

# -----------------------
# Build PDF
# -----------------------
doc.generate_pdf("resume_customized_final", clean_tex=True)