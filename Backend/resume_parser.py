import pymupdf

def extract_resume_text(pdf_file):

    try:
        # Open uploaded PDF
        document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")

        extracted_text = ""

        # Extract text from every page
        for page in document:
            extracted_text += page.get_text()

        document.close()

        return extracted_text

    except Exception as error:
        raise ValueError(f"Unable to read PDF: {error}")