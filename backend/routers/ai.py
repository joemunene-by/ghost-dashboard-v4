from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
AI_NAME = os.getenv("AI_NAME", "Ghost AI")

class ChatMessage(BaseModel):
    message: str
    context: str = ""

@router.post("/chat")
def chat(msg: ChatMessage):
    try:
        system_prompt = f"""You are {AI_NAME}, an intelligent assistant built into Ghost Dashboard v4.0.
You help developers analyze their code, understand their repositories, review commits, and provide insights.
You have a sharp, technical personality with a hacker aesthetic.
{f'Context: {msg.context}' if msg.context else ''}"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg.message}
            ],
            max_tokens=1024,
        )
        return {
            "response": response.choices[0].message.content,
            "model": response.model,
            "ai": AI_NAME
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/review")
def review_code(msg: ChatMessage):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are {AI_NAME}, an expert code reviewer. Be concise, technical, and actionable."},
                {"role": "user", "content": f"Review this code:\n\n{msg.message}"}
            ],
            max_tokens=1024,
        )
        return {"review": response.choices[0].message.content, "ai": AI_NAME}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/commit-message")
def generate_commit_message(msg: ChatMessage):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are {AI_NAME}. Generate a concise, conventional commit message. Return only the commit message, nothing else."},
                {"role": "user", "content": f"Generate a commit message for these changes:\n\n{msg.message}"}
            ],
            max_tokens=100,
        )
        return {"commit_message": response.choices[0].message.content.strip(), "ai": AI_NAME}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
