import streamlit as st
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO

def main():
    st.title("PDF File Uploader and Merger")
    
    # Create a file uploader for multiple PDF files
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        # Create a PDF writer object
        pdf_writer = PdfFileWriter()

        # Iterate over the uploaded files
        for uploaded_file in uploaded_files:
            pdf_reader = PdfFileReader(uploaded_file)
            for page_num in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page_num))

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
