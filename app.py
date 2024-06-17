import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os

def convert_docx_to_pdf(file_path):
    document = Document(file_path)
    output_buffer = BytesIO()
    c = canvas.Canvas(output_buffer, pagesize=letter)
    width, height = letter

    for paragraph in document.paragraphs:
        c.drawString(72, height - 72, paragraph.text)
        height -= 14
        if height <= 72:
            c.showPage()
            height = letter[1]

    c.save()
    output_buffer.seek(0)
    return output_buffer

def main():
    st.title("PDF and DOC/DOCX File Uploader and Merger")

    # Create a file uploader for multiple PDF, DOC, and DOCX files
    uploaded_files = st.file_uploader("Choose PDF, DOC, and DOCX files", type=["pdf", "doc", "docx"], accept_multiple_files=True)

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
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx" if uploaded_file.type.endswith("document") else ".doc") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name

                if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    # Convert the DOCX file to PDF
                    pdf_buffer = convert_docx_to_pdf(tmp_file_path)
                    pdf_reader = PdfReader(pdf_buffer)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                else:
                    st.error("Currently, only DOCX files are supported for conversion. Please upload DOCX files.")
                    continue
                
                # Clean up the temporary files
                os.remove(tmp_file_path)

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
