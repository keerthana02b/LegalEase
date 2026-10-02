from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str
    instructions: str = ""

@router.get("/health")
def health():
    return {"status": "LegalEase is running"}

@router.post("/generate")
def generate_document(data: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        document = generator.generate_document(
            document_type=data.document_type,
            parties=data.parties,
            terms=data.terms,
            effective_date=data.effective_date,
            instructions=data.instructions
        )
        return {"document": document}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))