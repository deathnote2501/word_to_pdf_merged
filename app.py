import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def main():
    st.title("PDF File Uploader and Merger")
    
    # Create a file uploader for multiple PDF files
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        # Create a new PDF document
        merged_pdf = fitz.open()

        # Iterate over the uploaded files
        for uploaded_file in uploaded_files:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page_num in range(len(pdf_document)):
                merged_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        # Save the merged PDF to a BytesIO object
        merged_pdf_bytes = merged_pdf.write()
        merged_pdf_io = BytesIO(merged_pdf_bytes)
        merged_pdf_io.seek(0)

        # Create a download button
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf_io,
            file_name="merged.pdf",
            mime="application/pdf"
        )
