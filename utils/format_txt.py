def format_txt(document_text):
    if not document_text or not document_text.strip():
        raise ValueError("Document content is empty")
    return document_text.strip() + "\n"
