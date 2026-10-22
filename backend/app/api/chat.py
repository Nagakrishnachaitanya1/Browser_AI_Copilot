from fastapi import APIRouter

from app.services.llm import generate_response
from app.schema.chat import ChatRequest

router = APIRouter()

data = {1: {"question": "what is ai", "page_content": "lorem100", "answer": "answer"}}


@router.post("/chat")
def chat(body: ChatRequest):

    new_id = max(data.keys()) + 1
    answer = generate_response(page_content=body.page_content, question=body.question)

    data[new_id] = {
        **body.model_dump(),
        "answer": answer,
    }

    return {
        "id": new_id,
        "question": body.question,
        "answer": answer,
    }


@router.get("/chat")
def get(id: int):
    return data[id]
