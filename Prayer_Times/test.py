import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

image_paths = ['WhatsApp Image 2023-08-01 at 9.14.18 PM.jpeg']
pdf_filename = 'images_to_pdf.pdf'
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

# List to store image elements
elements = []

# Add images to the list of elements
for image_path in image_paths:
    img = Image(image_path, width=400, height=400)
    elements.append(img)

# Build the PDF document
doc.build(elements)

pdf_filename = 'images_to_pdf.pdf'
# Open the PDF file in read-binary mode
with open(pdf_filename, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Read text from all pages
    full_text = ''
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        page_text = page.extract_text()
        print(page_text)
        full_text += page_text

# Print the extracted text
print(full_text)