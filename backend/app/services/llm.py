import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key is not loaded sucessfully! ")

llm = Groq(api_key=api_key)


def generate_response(page_content: str, question: str):

    response = llm.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using the provided webpage content. "
                    "If the answer isn't in the content, say so."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Webpage content:\n{page_content}\n\nQuestion:\n{question}"
                ),
            },
        ],
    )

    return response.choices[0].message.content

# page_content = """
# FastAPI is a modern Python web framework used to build APIs.
# It is built on standard Python type hints and supports automatic
# request validation using Pydantic.

# FastAPI provides automatic interactive API documentation through
# Swagger UI and ReDoc. It supports asynchronous programming using
# async and await, making it suitable for building high-performance
# web applications.

# Pydantic is used to define data models and validate incoming data.
# Uvicorn is an ASGI server commonly used to run FastAPI applications.
# """
# question = "What database does this webpage recommend?"

# answer = generate_response(page_content,question)

# print(answer)
