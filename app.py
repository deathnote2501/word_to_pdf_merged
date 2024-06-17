import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import pypandoc
import tempfile
import os

def check_pandoc():
    """Check if Pandoc is installed."""
    try:
        pypandoc.get_pandoc_version()
        return True
    except OSError:
        return False

def doc_to_pdf(file_path):
    output_file = file_path + ".pdf"
    pypandoc.convert_file(file_path, 'pdf', outputfile=output_file)
    return output_file

def main():
    st.title("PDF and DOC/DOCX File Uploader and Merger")

    # Check if Pandoc is installed
    if not check_pandoc():
        st.error("Pandoc is not installed. Please install Pandoc to use this app.")
        st.stop()

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

                # Convert the DOC or DOCX file to PDF
                pdf_file_path = doc_to_pdf(tmp_file_path)
                
                # Read the converted PDF and add its pages to the writer
                pdf_reader = PdfReader(pdf_file_path)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Clean up the temporary files
                os.remove(tmp_file_path)
                os.remove(pdf_file_path)

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
