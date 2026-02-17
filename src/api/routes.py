from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.tutor_service import TutorService

router = APIRouter()

# Request and Response Models
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

class SubmitCodeRequest(BaseModel):
    code: str
    language: str

class SubmitCodeResponse(BaseModel):
    feedback: str

# Initialize the service
tutor_service = TutorService()

@router.post("/api/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        answer = tutor_service.answer_question(request.question)
        return AskResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/submit_code", response_model=SubmitCodeResponse)
def submit_code(request: SubmitCodeRequest):
    try:
        feedback = tutor_service.provide_code_feedback(request.code, request.language)
        return SubmitCodeResponse(feedback=feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
