import streamlit as st
import requests
from utils.format_pdf import format_pdf
from utils.format_docx import format_docx
from utils.format_txt import format_txt
API_URL = "https://http://127.0.0.1:8000"
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #f4f6fa; }
h1, h2, h3 { color: #142d4e; }
.stButton > button {
    background-color: #142d4e;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚖️ LegalEase")
page = st.sidebar.radio("Navigation", ["Home", "Create Document"])

st.sidebar.info(
    "LegalEase is an AI drafting assistant, "
    "not a substitute for legal advice."
)

if "document" not in st.session_state:
    st.session_state.document = ""

if "details" not in st.session_state:
    st.session_state.details = {}

if page == "Home":
    st.title("⚖️ LegalEase")
    st.header("AI-Powered Legal Document Generator")
    st.write(
        "Create professional legal document drafts "
        "with the help of Generative AI."
    )
    st.write("### Features")
    st.markdown("""
    - AI-assisted legal document drafting
    - Editable document preview
    - PDF, DOCX and TXT downloads
    - Simple and user-friendly interface
    """)

    if st.button("Create Document"):
        st.session_state.page = "Create Document"
        st.rerun()

if page == "Create Document" or st.session_state.get("page") == "Create Document":
    st.title("Create Legal Document")

    document_types = [
        "Employment Contract",
        "Non-Disclosure Agreement (NDA)",
        "Lease Agreement",
        "Freelance Work Contract",
        "Employment Offer Letter",
        "General Agreement"
    ]

    with st.form("document_form"):
        doc_type = st.selectbox("Document Type", document_types)

        st.subheader("First Party")
        first_name = st.text_input("First Party Name")
        first_role = st.text_input("First Party Role")

        st.subheader("Second Party")
        second_name = st.text_input("Second Party Name")
        second_role = st.text_input("Second Party Role")

        terms = st.text_area("Terms and Conditions")
        effective_date = st.text_input(
            "Effective Date", placeholder="DD/MM/YYYY"
        )
        instructions = st.text_area("Additional Instructions")
        company = st.text_input("Company Name (optional)")

        submitted = st.form_submit_button("Generate Document")

    if submitted:
        if not all([
            first_name.strip(),
            second_name.strip(),
            terms.strip(),
            effective_date.strip()
        ]):
            st.error("Please fill in all required fields.")
        else:
            details = {
                "document_type": doc_type,
                "parties": (
                    f"{first_name} ({first_role or 'Role unspecified'}) "
                    f"and {second_name} "
                    f"({second_role or 'Role unspecified'}). "
                    f"Company: {company or 'Not specified'}"
                ),
                "terms": terms,
                "effective_date": effective_date,
                "instructions": instructions
            }

            st.session_state.details = details

            try:
                with st.spinner("Generating your document..."):
                    response = requests.post(
                        f"{API_URL}/generate",
                        json=details,
                        timeout=120
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.session_state.document = result["document"]

                st.success("Document generated successfully!")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to backend. "
                    "Please start the FastAPI server."
                )

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")

            except requests.exceptions.HTTPError as e:
                st.error(f"AI generation failed: {e}")
                st.exception(e)

            except (KeyError, ValueError):
                st.error("The backend returned an invalid response.")

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

    if st.session_state.document:
        st.subheader("Document Preview")

        edited = st.text_area(
            "Edit your document",
            value=st.session_state.document,
            height=400
        )

        st.session_state.document = edited

        if st.button("Regenerate Document"):
            details = st.session_state.details

            try:
                with st.spinner("Regenerating document..."):
                    response = requests.post(
                        f"{API_URL}/generate",
                        json=details,
                        timeout=120
                    )
                    response.raise_for_status()
                    st.session_state.document = response.json()["document"]

                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Regeneration failed: {e}")

        st.subheader("Download Document")
        text = st.session_state.document

        col1, col2, col3 = st.columns(3)

        with col1:
            try:
                pdf_data = format_pdf(text, "LegalEase Document")
                st.download_button(
                    "Download PDF",
                    data=pdf_data,
                    file_name="LegalEase_Document.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF export failed: {e}")

        with col2:
            try:
                docx_data = format_docx(text, "LegalEase Document")
                st.download_button(
                    "Download DOCX",
                    data=docx_data,
                    file_name="LegalEase_Document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"DOCX export failed: {e}")

        with col3:
            try:
                txt_data = format_txt(text)
                st.download_button(
                    "Download TXT",
                    data=txt_data,
                    file_name="LegalEase_Document.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"TXT export failed: {e}")

        st.caption(
            "Disclaimer: This is an AI-generated draft. "
            "Please have it reviewed by a qualified legal "
            "professional before signing."
        )
