import streamlit as st
from PyPDF2 import PdfMerger
from docx import Document
from io import BytesIO
from docx2pdf import convert as convert_docx_to_pdf

# Function to convert a DOCX file to PDF
def convert_to_pdf(docx_file):
    output = BytesIO()
    with open("temp.docx", "wb") as f:
        f.write(docx_file.getbuffer())
    convert_docx_to_pdf("temp.docx", output)
    return output.getvalue()

# Function to merge PDF files
def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(BytesIO(pdf))
    output = BytesIO()
    merger.write(output)
    merger.close()
    return output.getvalue()

# Streamlit app interface
st.title("Convert and Merge Word and PDF Files")

uploaded_files = st.file_uploader("Upload PDF or Word files", type=['pdf', 'docx'], accept_multiple_files=True)

if uploaded_files:
    pdf_files = []
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_files.append(uploaded_file.read())
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            pdf_files.append(convert_to_pdf(uploaded_file))
    
    if pdf_files:
        merged_pdf = merge_pdfs(pdf_files)
        st.success("Files have been successfully merged!")
        st.download_button(label="Download Merged PDF", data=merged_pdf, file_name="merged.pdf", mime="application/pdf")

# Add some basic content for testing
st.write("This is a test to ensure the app is working.")
st.write("Upload files above to convert and merge them.")
