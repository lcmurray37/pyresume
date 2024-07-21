from pylatex import Document, Section, Subsection, Command, NoEscape
from pylatex.utils import bold

# Define custom colors
section_color = 'gray!30'  # Define your preferred color, e.g., gray with 30% intensity

# Create a document
doc = Document()

# Define a custom command for section headers with background color
doc.preamble.append(Command('usepackage', 'xcolor'))
doc.preamble.append(Command('definecolor', 'sectioncolor', section_color))
doc.preamble.append(NoEscape(r'''
    \usepackage{titlesec}
    \titleformat{\section}
      {\normalfont\Large\bfseries}
      {\colorbox{sectioncolor}{\makebox[\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax]{\textcolor{white}{\thesection}}}}
      {0em}
      {\color{sectioncolor}\MakeUppercase}
    \titlespacing*{\section}{0pt}{\baselineskip}{\baselineskip}
    
    \titleformat{\subsection}
      {\normalfont\large\bfseries}
      {\thesubsection}
      {1em}
      {}
    \titlespacing*{\subsection}{0pt}{\baselineskip}{\baselineskip}
'''))

# Remove section numbering
doc.preamble.append(NoEscape(r'\renewcommand{\thesection}{}'))

# Title with name
doc.preamble.append(Command('title', 'Lucy Murray'))
doc.append(NoEscape(r'\maketitle'))

# Contact information section
with doc.create(Section('Contact Information')):
    doc.append(bold('Phone Number: '))
    doc.append('+1 (123) 456-7890\n')
    doc.append(bold('Email: '))
    doc.append('lucy.murray@example.com\n')
    doc.append(bold('GitHub: '))
    doc.append('github.com/lucymurray')

# Sections with custom formatting
with doc.create(Section('Experience')):
    with doc.create(Subsection('2023 - Present')):
        doc.append(bold('Software Engineer at XYZ Inc.'))

with doc.create(Section('Tools')):
    doc.append('Python, LaTeX, Git, VS Code')

with doc.create(Section('Education')):
    with doc.create(Subsection('2019 - 2023')):
        doc.append(bold('Bachelor of Science in Computer Science'))

# Generate the PDF
doc.generate_pdf('resume_customized_final', clean_tex=False)