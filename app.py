import streamlit as st
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO

# Function to concatenate PDF files
def concatenate_pdfs(pdf_files):
    pdf_writer = PdfFileWriter()
    
    for pdf in pdf_files:
        pdf_reader = PdfFileReader(pdf)
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page)
    
    output = BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    return output

# Streamlit UI
st.title("PDF Concatenation Tool")

uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

if uploaded_files:
    if st.button("Concatenate PDFs"):
        concatenated_pdf = concatenate_pdfs(uploaded_files)
        st.success("PDF files concatenated successfully!")
        
        # Provide a download button
        st.download_button(
            label="Download Concatenated PDF",
            data=concatenated_pdf,
            file_name="concatenated.pdf",
            mime="application/pdf"
        )
