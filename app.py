import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def main():
    # Affichage du titre, sous-titre, et image avant la demande de mot de passe
    st.markdown("<h1 style='text-align: center;'>Concaténer vos fichiers PDFs</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Par Jérome IAvarone - IAvaronce conseil</p>", unsafe_allow_html=True)
    st.write("")
    image_url = "https://www.iacademy-formation.com/wp-content/uploads/2024/08/iyus-sugiharto-jpkxJAcp6a4-unsplash-modified-1.png"
    st.image(image_url, use_column_width=True)

    # Password input
    password = st.text_input("Entrez le mot de passe pour accéder à l'application", type="password")

    if password == st.secrets["PASSWORD"]:  # Mot de passe correct
        st.write("")
        st.markdown("<h2 style='text-align: left;'>Chargez vos fichiers PDF</h2>", unsafe_allow_html=True)
        
        # Crée un téléchargeur de fichiers pour plusieurs fichiers PDF
        uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

        if uploaded_files:
            st.write(f"Nombre de fichiers chargés : {len(uploaded_files)}")

            # Crée un objet PdfWriter pour fusionner les fichiers
            pdf_writer = PdfWriter()

            # Parcourt les fichiers PDF chargés
            try:
                for uploaded_file in uploaded_files:
                    pdf_reader = PdfReader(uploaded_file)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                # Enregistre le PDF fusionné dans un objet BytesIO
                merged_pdf = BytesIO()
                pdf_writer.write(merged_pdf)
                merged_pdf.seek(0)

                # Stocke le PDF fusionné dans l'état de session
                st.session_state.merged_pdf = merged_pdf

                # Crée un bouton de téléchargement
                st.download_button(
                    label="Télécharger les fichiers PDF concaténés",
                    data=st.session_state.merged_pdf,
                    file_name="merged.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erreur lors de la fusion des fichiers PDF : {str(e)}")

    elif password:  # Vérifie que l'utilisateur a saisi un mot de passe incorrect
        st.warning("Mot de passe incorrect.")

    # Affichage du pied de page
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<p style='text-align: center;'>© 2024 Jérome IAvarone - jerome.iavarone@gmail.com</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
