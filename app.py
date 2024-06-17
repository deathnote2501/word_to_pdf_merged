import streamlit as st
from PyPDF2 import PdfMerger
from docx import Document
from io import BytesIO
from docx2pdf import convert as convert_docx_to_pdf

# Fonction pour convertir un fichier DOCX en PDF
def convert_to_pdf(docx_file):
    output = BytesIO()
    with open("temp.docx", "wb") as f:
        f.write(docx_file.getbuffer())
    convert_docx_to_pdf("temp.docx", output)
    return output.getvalue()

# Fonction pour concaténer les fichiers PDF
def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(BytesIO(pdf))
    output = BytesIO()
    merger.write(output)
    merger.close()
    return output.getvalue()

# Interface Streamlit
st.title("Convertir et concaténer des fichiers PDF et Word")

uploaded_files = st.file_uploader("Téléchargez des fichiers PDF ou Word", type=['pdf', 'docx'], accept_multiple_files=True)
if uploaded_files:
    pdf_files = []
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_files.append(uploaded_file.read())
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            pdf_files.append(convert_to_pdf(uploaded_file))

    if pdf_files:
        merged_pdf = merge_pdfs(pdf_files)
        st.success("Les fichiers ont été concaténés avec succès !")
        st.download_button(label="Télécharger le PDF concaténé", data=merged_pdf, file_name="merged.pdf", mime="application/pdf")
