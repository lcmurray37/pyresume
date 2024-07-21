import pylatex
from pylatex import Document, Section, Itemize, Command

# Create a basic document
doc = Document()
doc.preamble.append(Command('title', 'My Resume'))
doc.preamble.append(Command('author', 'Your Name'))
doc.preamble.append(Command('date', 'Today\'s Date'))
doc.append(Section('Summary'))
doc.append('This is a summary of your experience.')
doc.append(Section('Experience'))
with doc.create(Itemize()) as itemize:
    itemize.add_item('Job 1: Description of job 1.')
    itemize.add_item('Job 2: Description of job 2.')
doc.append(Section('Education'))
doc.append('Your educational background.')
doc.generate_pdf('resume', clean_tex=False)
