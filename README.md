# AI-Powered Interactive Coding Tutor

An intelligent, AI-powered coding tutor that provides personalized programming assistance, code reviews, and maintains conversation context for enhanced learning experiences.

## 🌟 Features

- **Interactive Q&A**: Ask coding questions and receive detailed, educational explanations
- **Code Analysis**: Submit code for comprehensive feedback and improvement suggestions
- **Conversation History**: Maintains context across multiple interactions for better understanding
- **Session Management**: Track learning progress and conversation history per user
- **Multi-Language Support**: Works with any programming language
- **Modern API**: RESTful API with comprehensive OpenAPI documentation
- **Robust Error Handling**: Detailed error messages and validation
- **Configurable AI Parameters**: Customize AI behavior through environment variables

## 🏗️ System Architecture

The system is designed using a clean, modular architecture to ensure scalability, maintainability, and testability. The key components are:

1. **API Layer**: Handles HTTP requests and routes them to the appropriate services.
2. **Service Layer**: Contains the business logic for processing user input and generating AI-powered responses.
3. **Repository Layer**: Manages data storage and retrieval (e.g., user sessions, code snippets).
4. **Core AI Engine**: Implements the core logic for code analysis and AI-driven tutoring using OpenAI's GPT models.
5. **Configuration**: Environment-based configuration management for secure and flexible deployment.

### Directory Structure

```
.
├── src/
│   ├── api/           # API routes and FastAPI application
│   ├── services/      # Business logic and orchestration
│   ├── repositories/  # Data persistence layer
│   └── core/          # AI engine and configuration
├── tests/             # Comprehensive unit tests
├── requirements.txt   # Python dependencies
├── Dockerfile        # Container configuration
└── .env.example      # Environment configuration template
```

### Tech Stack

- **Backend**: Python 3.10+ with FastAPI
- **AI Engine**: OpenAI GPT-3.5-turbo (configurable)
- **API Framework**: FastAPI with automatic OpenAPI documentation
- **Testing**: pytest with comprehensive coverage
- **Containerization**: Docker

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/ai-powered-interactive-coding-tutor.git
   cd ai-powered-interactive-coding-tutor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the application**
   ```bash
   uvicorn src.api.app:app --reload
   ```

5. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t coding-tutor .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here coding-tutor
   ```

## 📝 Configuration

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7

# Application Configuration
APP_NAME=AI-Powered Interactive Coding Tutor
APP_VERSION=1.0.0
DEBUG=false

# API Configuration
API_RATE_LIMIT=100
```

## 🔌 API Endpoints

### Health Check
```http
GET /api/health
```
Verify the service is running.

### Ask a Question
```http
POST /api/ask
Content-Type: application/json

{
  "question": "What is a Python list?",
  "user_id": "user123",
  "use_history": true
}
```

**Response:**
```json
{
  "answer": "A Python list is a mutable, ordered collection...",
  "user_id": "user123"
}
```

### Submit Code for Review
```http
POST /api/submit_code
Content-Type: application/json

{
  "code": "def add(a, b):\n    return a + b",
  "language": "Python",
  "context": "Simple addition function",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "feedback": "Your code is correct! Here are some observations...",
  "user_id": "user123"
}
```

### Get Session Summary
```http
GET /api/session/{user_id}/summary
```

**Response:**
```json
{
  "user_id": "user123",
  "total_questions": 5,
  "total_code_submissions": 2,
  "has_active_session": true
}
```

### Clear Session
```http
POST /api/session/clear
Content-Type: application/json

{
  "user_id": "user123"
}
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tutor_service.py -v
```

## 📚 Usage Examples

### Python Example

```python
import requests

# Ask a question
response = requests.post("http://localhost:8000/api/ask", json={
    "question": "How do I use list comprehensions in Python?",
    "user_id": "student123",
    "use_history": True
})
print(response.json()["answer"])

# Submit code for review
code_response = requests.post("http://localhost:8000/api/submit_code", json={
    "code": "numbers = [x**2 for x in range(10)]",
    "language": "Python",
    "context": "Squaring numbers using list comprehension",
    "user_id": "student123"
})
print(code_response.json()["feedback"])
```

### cURL Example

```bash
# Ask a question
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is recursion?", "user_id": "user1"}'

# Submit code for review
curl -X POST "http://localhost:8000/api/submit_code" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)",
    "language": "Python",
    "user_id": "user1"
  }'
```

## 🎯 Key Improvements

This enhanced version includes:

- ✅ **Modern OpenAI API**: Updated from deprecated Completion API to ChatCompletion API
- ✅ **Environment Configuration**: Secure API key management with `.env` support
- ✅ **Conversation Context**: Maintains conversation history for multi-turn interactions
- ✅ **Session Management**: Track user progress and maintain state
- ✅ **Input Validation**: Comprehensive request validation with detailed error messages
- ✅ **Comprehensive Logging**: Debug and monitor application behavior
- ✅ **Enhanced Documentation**: Detailed API documentation with examples
- ✅ **Better AI Prompts**: Improved system prompts for more educational responses
- ✅ **Extended Tests**: Comprehensive test coverage with mocking
- ✅ **CORS Support**: Ready for frontend integration

## 🔒 Security Considerations

- Never commit `.env` files with real API keys
- Use environment variables for sensitive configuration
- Implement rate limiting in production
- Add authentication/authorization for production deployments
- Validate and sanitize all user inputs

## 🚧 Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement a frontend interface using React or Vue.js
- [ ] Add persistent database storage (PostgreSQL/MongoDB)
- [ ] Implement rate limiting and request throttling
- [ ] Add support for code execution in sandboxed environments
- [ ] Create learning paths and progress tracking
- [ ] Add support for multiple AI models
- [ ] Implement caching for common questions
- [ ] Add analytics and usage metrics

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
