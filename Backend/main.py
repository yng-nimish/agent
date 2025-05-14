from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import CommerceAgent
from image_processor import process_image_search
from mangum import Mangum

app = FastAPI()

# Allow CORS for frontend and API Gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://commerce-ai-agent-frontend.s3-website-<region>.amazonaws.com",
        "http://localhost:3000",
        "https://cwxb04pos2.execute-api.us-east-1.amazonaws.com/prod"  # Replace with your API Gateway URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CommerceAgent()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = await agent.handle_message(request.message)
    return {"response": response}

@app.post("/image-search")
async def image_search(file: UploadFile = File(...)):
    products = await process_image_search(file)
    return {"products": products}

# Lambda handler
handler = Mangum(app)