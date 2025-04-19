import streamlit as st
from pdf2docx import Converter
import tempfile
import os

st.set_page_config(page_title="PDF to Word Converter", layout="centered")
st.title("📄 PDF to Word Converter")

st.write("Upload a PDF file and download the converted Word (.docx) file.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    output_docx_path = temp_pdf_path.replace(".pdf", ".docx")

    with st.spinner("Converting..."):
        try:
            converter = Converter(temp_pdf_path)
            converter.convert(output_docx_path, start=0, end=None)
            converter.close()

            with open(output_docx_path, "rb") as f:
                st.success("✅ Conversion successful!")
                st.download_button(
                    label="📥 Download Word File",
                    data=f,
                    file_name=os.path.basename(output_docx_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"Conversion failed: {e}")

    # Clean up
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)
    if os.path.exists(output_docx_path):
        os.remove(output_docx_path)

