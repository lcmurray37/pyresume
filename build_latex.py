from pylatex import Document, Section, Subsection, Command
from pylatex.utils import bold, NoEscape

def generate_resume():
    # Create a new Document
    doc = Document()

    # Document metadata
    doc.preamble.append(Command('title', 'Resume'))
    doc.preamble.append(Command('author', 'Your Name'))
    doc.preamble.append(Command('date', ''))

    # Define a custom command for section headers
    doc.preamble.append(NoEscape(r'''
        \newcommand{\sectionheader}[1]{
            \par\bigskip
            {\Large\bfseries #1}
            \par\smallskip
            \hrule
            \par\medskip
        }
    '''))

    # Title (Name)
    doc.append(Section(bold('Your Name')))

    # Contact Information
    doc.append(Section('Contact Information'))
    doc.append(NoEscape(r'\textbf{Phone:} Your Phone Number'))
    doc.append(NoEscape(r'\newline'))
    doc.append(NoEscape(r'\textbf{Email:} Your Email Address'))
    doc.append(NoEscape(r'\newline'))
    doc.append(NoEscape(r'\textbf{GitHub:} \url{https://github.com/yourusername}'))  # Update URL

    # Experience
    with doc.create(Section()):
        doc.append(NoEscape(r'\sectionheader{Experience}'))
        with doc.create(Subsection('Job Title 1')):
            doc.append('Company Name, Location\n')
            doc.append('Dates of Employment\n')
            doc.append('Responsibilities and achievements.\n')

        with doc.create(Subsection('Job Title 2')):
            doc.append('Company Name, Location\n')
            doc.append('Dates of Employment\n')
            doc.append('Responsibilities and achievements.\n')

    # Tools
    with doc.create(Section()):
        doc.append(NoEscape(r'\sectionheader{Tools}'))
        doc.append('List of tools and technologies relevant to data analysis.\n')

    # Education
    with doc.create(Section()):
        doc.append(NoEscape(r'\sectionheader{Education}'))
        doc.append('Degree Name in Major\n')
        doc.append('University Name, Location\n')
        doc.append('Graduation Date\n')

    # Generate PDF
    doc.generate_pdf('resume', clean_tex=False)

    # Clean up auxiliary files
    doc.generate_tex(clean_tex=True)

if __name__ == '__main__':
    generate_resume()
