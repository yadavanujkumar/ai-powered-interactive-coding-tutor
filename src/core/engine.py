import openai

class AIEngine:
    def __init__(self):
        openai.api_key = "your_openai_api_key"

    def generate_answer(self, question: str) -> str:
        """Generate an AI-powered answer to a user's question."""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a coding tutor. Answer the following question: {question}",
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def analyze_code(self, code: str, language: str) -> str:
        """Analyze the submitted code and provide feedback."""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a coding tutor. Provide feedback for the following {language} code: {code}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
