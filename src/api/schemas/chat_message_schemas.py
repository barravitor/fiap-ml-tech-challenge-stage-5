# app/schemas/chat_message_schemas.py
from pydantic import BaseModel

class ChatMessageSchema(BaseModel):
    question: str