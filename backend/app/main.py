from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api import health, chat

app = FastAPI(title="AI powered assistent", version="1.0.0")

app.include_router(health.router)
app.include_router(chat.router)



@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="test")
