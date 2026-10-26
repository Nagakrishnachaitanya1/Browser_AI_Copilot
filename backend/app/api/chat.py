from fastapi import APIRouter, HTTPException, status

from app.services.llm import generate_response
from app.schema.chat import ChatRequest
from app.db.database import initialize_db, save, retrive, retriveAll


router = APIRouter()


initialize_db()



@router.post("/chat")
def chat(body: ChatRequest):

    answer = generate_response(page_content=body.page_content, question=body.question)

    id = save(**body.model_dump(), answer=answer)

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
    return retriveAll()
