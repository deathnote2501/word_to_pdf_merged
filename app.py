import streamlit as st

def main():
    st.title("PDF File Uploader")
    
    # Create a file uploader for multiple PDF files
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")

if __name__ == "__main__":
    main()
