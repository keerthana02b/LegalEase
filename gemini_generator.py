import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiDocumentGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "your_api_key_here":
            raise ValueError("Gemini API key is missing. Please set it in .env")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        instructions: str = ""
    ):
        prompt = f"""
You are an AI assistant that drafts legal documents.

Create a clear and professionally structured draft
based on the following information.

Document Type: {document_type}
Parties: {parties}
Terms and Conditions: {terms}
Effective Date: {effective_date}
Additional Instructions: {instructions}

Include:
1. Document Title
2. Parties Involved
3. Purpose
4. Terms and Conditions
5. Effective Date
6. Signature Sections

Use formal and easy-to-understand legal language.
Do not invent missing facts.
If any important information is missing, mention it
clearly in the draft.

Add a note that this is an AI-generated draft
and should be reviewed by a qualified lawyer.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text

        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}") from e