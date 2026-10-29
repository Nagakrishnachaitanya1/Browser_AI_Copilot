import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key is not loaded sucessfully! ")

llm = Groq(api_key=api_key)


def generate_response(page_content: str, question: str):
    try:
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

    except Exception as exc:
        raise RuntimeError("Failed to generate an LLM response") from exc
