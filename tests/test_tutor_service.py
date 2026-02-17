import pytest
from src.services.tutor_service import TutorService

@pytest.fixture
def tutor_service():
    return TutorService()

def test_answer_question(tutor_service):
    question = "What is a Python list?"
    answer = tutor_service.answer_question(question)
    assert isinstance(answer, str)
    assert len(answer) > 0

def test_provide_code_feedback(tutor_service):
    code = "def add(a, b):\n    return a + b"
    language = "Python"
    feedback = tutor_service.provide_code_feedback(code, language)
    assert isinstance(feedback, str)
    assert len(feedback) > 0
