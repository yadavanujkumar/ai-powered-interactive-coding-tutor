"""AI Engine module for the AI-Powered Interactive Coding Tutor."""
import logging
from typing import List, Dict, Optional
from openai import OpenAI, OpenAIError
from src.core.config import settings

logger = logging.getLogger(__name__)


class AIEngine:
    """AI Engine for generating tutoring responses and code analysis."""
    
    def __init__(self):
        """Initialize the AI Engine with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature
        logger.info(f"AI Engine initialized with model: {self.model}")

    def generate_answer(self, question: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate an AI-powered answer to a user's question.
        
        Args:
            question: The user's question
            conversation_history: Optional list of previous messages for context
            
        Returns:
            AI-generated answer as a string
            
        Raises:
            OpenAIError: If the API request fails
        """
        try:
            messages = []
            
            # Add system message
            messages.append({
                "role": "system",
                "content": (
                    "You are an experienced and friendly coding tutor. Your goal is to help students "
                    "learn programming concepts effectively. Provide clear, concise explanations with "
                    "examples when appropriate. Encourage good coding practices and critical thinking."
                )
            })
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current question
            messages.append({
                "role": "user",
                "content": question
            })
            
            logger.info(f"Generating answer for question: {question[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info(f"Generated answer with {len(answer)} characters")
            
            return answer
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in generate_answer: {str(e)}")
            raise

    def analyze_code(self, code: str, language: str, context: Optional[str] = None) -> str:
        """
        Analyze submitted code and provide detailed feedback.
        
        Args:
            code: The code to analyze
            language: Programming language of the code
            context: Optional context about what the code should do
            
        Returns:
            Detailed feedback about the code
            
        Raises:
            OpenAIError: If the API request fails
        """
        try:
            prompt = f"""As a coding tutor, analyze the following {language} code and provide constructive feedback:

Code:
```{language}
{code}
```
"""
            if context:
                prompt += f"\nContext: {context}\n"
            
            prompt += """
Please provide:
1. What the code does (if it's correct)
2. Any bugs or errors you find
3. Code quality and best practices suggestions
4. Performance considerations (if relevant)
5. Suggestions for improvement

Keep your feedback encouraging and educational."""

            logger.info(f"Analyzing {language} code ({len(code)} characters)")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert coding tutor specializing in code review and analysis. "
                            "Provide thorough, educational feedback that helps students improve their coding skills."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            feedback = response.choices[0].message.content.strip()
            logger.info(f"Generated code feedback with {len(feedback)} characters")
            
            return feedback
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error in analyze_code: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in analyze_code: {str(e)}")
            raise

