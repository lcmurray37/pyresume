import pylatex
from pylatex import Document, Section, Itemize, Command

# Create a new Document
doc = Document()

# Document metadata
doc.preamble.append(Command('title', 'Resume'))
doc.preamble.append(Command('author', 'Lucy Murray'))
doc.preamble.append(Command('date', ''))

# Title (Name)
doc.append(Section('Lucy Murray'))
doc.append(Section('Contact Information'))
doc.append('Address: Your Address\n')
doc.append('Phone: Your Phone Number\n')
doc.append('Email: Your Email Address\n')

# Summary
doc.append(Section('Summary'))
doc.append('A summary of your skills and experience.')

# Experience
doc.append(Section('Experience'))
with doc.create(Section('Job Title')):
    doc.append('Company Name, Location\n')
    doc.append('Dates of Employment\n')
    doc.append('Responsibilities and achievements.\n')

# Education
doc.append(Section('Education'))
doc.append('Degree Name in Major\n')
doc.append('University Name, Location\n')
doc.append('Graduation Date\n')

# Generate PDF
doc.generate_pdf('resume', clean_tex=False)

# Clean up auxiliary files
doc.generate_tex(clean_tex=True)