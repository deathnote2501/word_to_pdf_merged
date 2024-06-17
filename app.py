import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

def docx_to_pdf(docx_file):
    document = Document(docx_file)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    for paragraph in document.paragraphs:
        c.drawString(72, height - 72, paragraph.text)
        height -= 14
        if height <= 72:
            c.showPage()
            height = letter[1]
    
    c.save()
    buffer.seek(0)
    return buffer

def main():
    st.title("PDF and DOCX File Uploader and Merger")
    
    # Create a file uploader for multiple PDF and DOCX files
    uploaded_files = st.file_uploader("Choose PDF and DOCX files", type=["pdf", "docx"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        # Create a PDF writer object
        pdf_writer = PdfWriter()

        # Process the uploaded files
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                pdf_buffer = docx_to_pdf(uploaded_file)
                pdf_reader = PdfReader(pdf_buffer)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

        # Save the merged PDF to a BytesIO object
        merged_pdf = BytesIO()
        pdf_writer.write(merged_pdf)
        merged_pdf.seek(0)

        # Create a download button
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf,
            file_name="merged.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
