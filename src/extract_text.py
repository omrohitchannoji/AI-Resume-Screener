import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from a Streamlit UploadedFile PDF.
    """
    try:
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # Reset pointer so it can be reused

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:
        print("PDF extraction error:", e)
        return ""
