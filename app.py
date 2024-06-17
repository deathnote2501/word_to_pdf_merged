import streamlit as st
import pdfplumber
from fpdf import FPDF
from io import BytesIO

def main():
    st.title("PDF File Uploader and Merger")
    
    # Create a file uploader for multiple PDF files
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        # Create a FPDF object
        pdf_writer = FPDF()

        # Iterate over the uploaded files
        for uploaded_file in uploaded_files:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    pdf_writer.add_page()
                    text = page.extract_text()
                    if text:
                        pdf_writer.set_font("Arial", size=12)
                        pdf_writer.multi_cell(0, 10, text)

        # Save the merged PDF to a BytesIO object
        merged_pdf = BytesIO()
        pdf_writer.output(merged_pdf)
        merged_pdf.seek(0)

        # Create a download button
        st.download_button(
            label="Download Merged PDF",
            data=merged_pdf,
            file_name="merged.pdf",
            mime="application/pdf"
        )
