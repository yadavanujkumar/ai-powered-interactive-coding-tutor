# AI-Powered Interactive Coding Tutor

## System Architecture

The system is designed using a clean, modular architecture to ensure scalability, maintainability, and testability. The key components are:

1. **API Layer**: Handles HTTP requests and routes them to the appropriate services.
2. **Service Layer**: Contains the business logic for processing user input and generating AI-powered responses.
3. **Repository Layer**: Manages data storage and retrieval (e.g., user sessions, code snippets).
4. **Core AI Engine**: Implements the core logic for code analysis and AI-driven tutoring using OpenAI's GPT models.

### Directory Structure

- `src/api/`: Contains the API routes and request handling logic.
- `src/services/`: Contains the business logic and orchestration of AI responses.
- `src/repositories/`: Handles data persistence and retrieval.
- `src/core/`: Implements the AI engine and utility functions.
- `tests/`: Contains unit tests for all major components.

### Tech Stack

- **Backend**: Python (FastAPI)
- **AI Engine**: OpenAI GPT API
- **Containerization**: Docker

### How to Run

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn src.api.app:app --reload`
4. Run tests: `pytest tests/`

### API Endpoints

- `POST /api/ask`: Accepts user input and returns an AI-generated response.
- `POST /api/submit_code`: Accepts code snippets and provides feedback.

---

## Future Enhancements

- Add user authentication and authorization.
- Implement a frontend interface using React or Vue.js.
- Extend AI capabilities to support more programming languages.
