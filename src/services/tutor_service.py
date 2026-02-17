from src.core.engine import AIEngine

class TutorService:
    def __init__(self):
        self.ai_engine = AIEngine()

    def answer_question(self, question: str) -> str:
        """Process a user's question and return an AI-generated answer."""
        return self.ai_engine.generate_answer(question)

    def provide_code_feedback(self, code: str, language: str) -> str:
        """Analyze the submitted code and provide feedback."""
        return self.ai_engine.analyze_code(code, language)
