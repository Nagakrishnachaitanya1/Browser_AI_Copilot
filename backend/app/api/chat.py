import sqlite3

from fastapi import APIRouter, HTTPException, status

from app.services.llm import generate_response
from app.schema.chat import ChatRequest
from app.db.database import initialize_db, save, retrive, retriveAll


router = APIRouter()


initialize_db()


@router.post("/chat")
def chat(body: ChatRequest):

    try:
        answer = generate_response(
            page_content=body.page_content, question=body.question
        )
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service is temporarily unavailable",
        )

    try:
        id = save(**body.model_dump(), answer=answer)

    except sqlite3.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the conversation.",
        )

    return {
        "id": id,
        "question": body.question,
        "answer": answer,
    }


@router.get("/chat")
def get(id: int):

    ans = retrive(id)

    if ans is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given ID is not valid !"
        )

    return {
        "id": ans[0],
        "question": ans[1],
        "page_content": ans[2],
        "answer": ans[3],
    }


@router.get("/chats")
def get_all():

    records = retriveAll()

    records_dics = []

    for record in records:
        record_dics = {
            "id": record[0],
            "question": record[1],
            "page_content": record[2],
            "answer": record[3],
        }

        records_dics.append(record_dics)

    return records_dics
