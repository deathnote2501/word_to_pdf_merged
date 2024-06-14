import streamlit as st
import sys

# Basic check to ensure Streamlit is rendering something
st.title("Streamlit App Debugging")
st.write("If you can see this message, Streamlit is working correctly.")

# Display Python version to ensure environment is correct
st.write(f"Python version: {sys.version}")

# Check if required libraries are installed
try:
    from PyPDF2 import PdfMerger
    from docx import Document
    from io import BytesIO
    from docx2pdf import convert as convert_docx_to_pdf
    st.write("All required libraries are imported successfully.")
except ImportError as e:
    st.error(f"Error importing libraries: {e}")

# Simple uploader to test file upload functionality
uploaded_files = st.file_uploader("Upload PDF or Word files", type=['pdf', 'docx'], accept_multiple_files=True)

if uploaded_files:
    st.write("Files uploaded:")
    for uploaded_file in uploaded_files:
        st.write(f"- {uploaded_file.name}")

# Check if any files are uploaded
if st.button("Check Files"):
    if uploaded_files:
        st.write("Files are present.")
    else:
        st.write("No files uploaded.")
