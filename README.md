# Browser AI Copilot

An AI-powered Chrome extension that lets you interact with webpages using natural language. Extract webpage content, ask questions, and get context-aware answers powered by Groq and a FastAPI backend.

## Overview

Browser AI Copilot is a browser-based AI assistant designed to help users understand and interact with web content without manually copying and pasting information into an AI chatbot.

The extension extracts readable text from the active webpage and sends it, along with the user's question, to a FastAPI backend. The backend uses a Groq-hosted language model to generate an answer based on the supplied webpage content.

Conversations are stored in an SQLite database for persistence.

## Features

- **Webpage Content Extraction:** Extract readable text from the currently active browser tab.
- **Context-Aware Question Answering:** Ask questions about the extracted webpage content.
- **LLM Integration:** Generate responses using Groq's API.
- **Conversation Persistence:** Store conversations in SQLite.
- **Chat Retrieval:** Retrieve individual conversations or all saved conversations through API endpoints.
- **Chrome Extension Interface:** Interact with the AI assistant through a lightweight popup interface.
- **Error Handling:** Handle AI service and database failures through structured API responses.
- **Suggested Prompts:** Use predefined prompts to quickly ask questions about webpage content.

## Architecture

The application follows a simple client-server architecture.

```text
              Chrome Browser
                    |
                    v
          Browser AI Copilot
             Extension
                    |
          Extract webpage text
                    |
          User enters a question
                    |
                    v
             FastAPI Backend
                    |
                    v
              Groq API
                    |
           Generate AI Response
                    |
                    v
             SQLite Database
                    |
             Save Conversation
                    |
                    v
           Return JSON Response
                    |
                    v
          Display Answer in Popup
```

## Technology Stack

| Component | Technology |
|---|---|
| Browser Extension | Chrome Extension Manifest V3 |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| LLM Integration | Groq API |
| Language Model | OpenAI GPT-OSS 120B via Groq |
| Database | SQLite |
| Data Validation | Pydantic |
| API Testing | Scalar / FastAPI API documentation |

## Project Structure

```text
Browser_AI_Copilot/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── chat.py
│   │   │
│   │   ├── db/
│   │   │   └── database.py
│   │   │
│   │   ├── schema/
│   │   │   └── chat.py
│   │   │
│   │   ├── services/
│   │   │   └── llm.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or later
- Google Chrome
- Git
- A Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/Nagakrishnachaitanya1/Browser_AI_Copilot.git

cd Browser_AI_Copilot
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:

https://console.groq.com/keys

**Important:** Never commit your `.env` file or expose your API key in the Chrome extension.

### 4. Start the FastAPI Backend

From the `backend` directory, run:

```bash
fastapi dev
```

The backend will run locally at:

```text
http://127.0.0.1:8000
```

API documentation:

- Scalar: http://127.0.0.1:8000/scalar
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

### 5. Install the Chrome Extension

1. Open Google Chrome.
2. Navigate to `chrome://extensions`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the `extension` folder from the cloned repository.
6. Pin Browser AI Copilot to your Chrome toolbar.

The extension is now ready to use with your locally running backend.

## How to Use

1. Start the FastAPI backend.
2. Open any regular webpage in Chrome.
3. Click the Browser AI Copilot extension.
4. Select **Read page** to extract webpage content.
5. Enter a question or choose a suggested prompt.
6. Click **Ask AI**.
7. View the generated response in the extension popup.

The AI response is generated using the extracted webpage content and the user's question.

## API Endpoints

The backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check backend health |
| POST | `/chat` | Generate an AI response and save the conversation |
| GET | `/chat?id=1` | Retrieve an individual conversation |
| GET | `/chats` | Retrieve all saved conversations |

### Example: POST /chat

Request:

```json
{
    "question": "What is this webpage about?",
    "page_content": "This webpage contains information about artificial intelligence."
}
```

Response:

```json
{
    "id": 1,
    "question": "What is this webpage about?",
    "answer": "The webpage discusses artificial intelligence..."
}
```

The generated answer is returned by the backend, and the conversation is stored in SQLite.

## Implementation Details

### Webpage Extraction

The extension uses Chrome's scripting API to access the active webpage and extract readable text using the page's `document.body.innerText`.

The current implementation limits extraction to 12,000 characters to keep the initial requests manageable.

### AI Response Generation

The backend sends the extracted webpage content and user question to Groq using the `openai/gpt-oss-120b` model.

The system prompt instructs the model to answer using the provided webpage content and acknowledge when the answer is not available in that content.

### Database

SQLite is used to persist conversations.

Each conversation contains:

- `id`
- `question`
- `page_content`
- `answer`

The database supports saving conversations and retrieving individual or multiple records.

## Error Handling

The backend includes handling for important failure scenarios:

- AI service failures are translated into HTTP `502 Bad Gateway` responses.
- SQLite save failures are translated into HTTP `500 Internal Server Error` responses.
- Missing conversation IDs are handled through HTTP `404 Not Found` responses.

## Current Project Status

**Version:** 1.0.0 — Initial MVP

The current implementation supports local Chrome extension usage with a locally running FastAPI backend.

Public deployment, authentication, multi-user data isolation, and production-level security are not yet part of this MVP.

## Future Improvements

- Persistent cloud database and backend deployment.
- User authentication and individual conversation histories.
- Conversation history interface.
- Improved Markdown response rendering.
- Automated backend testing using pytest.
- Better webpage content extraction and handling of long webpages.
- Chrome Web Store publication.
- Additional AI-powered webpage interaction features.

## Security Notes

- Keep Groq API keys exclusively on the backend.
- Do not commit `.env` files or other secrets.
- The current local MVP is not intended for unrestricted public API access.
- Add authentication, request limits, and user-level database isolation before public deployment.

## Author

**Dharmisetty Naga Krishna Chaitanya**

GitHub: [Nagakrishnachaitanya1](https://github.com/Nagakrishnachaitanya1)

Project Repository: [Browser AI Copilot](https://github.com/Nagakrishnachaitanya1/Browser_AI_Copilot)

---

Built with Python, FastAPI, Groq, SQLite, and JavaScript.
