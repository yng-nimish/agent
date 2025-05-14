from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class RecommendRequest(BaseModel):
    query: str