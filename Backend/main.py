import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import CommerceAgent
from image_processor import process_image_search
from mangum import Mangum
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Commerce AI Agent API")

# CORS configuration
region = os.getenv("AWS_REGION", "us-east-1")
frontend_url = os.getenv(
    "FRONTEND_URL",
    f"http://commerce-ai-agent-frontend.s3-website-{region}.amazonaws.com"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "http://localhost:3000",
        f"https://cwxb04pos2.execute-api.{region}.amazonaws.com/prod",
        f"https://cwxb04pos2.execute-api.{region}.amazonaws.com/dev"
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
    try:
        logger.info(f"Received chat request: {request.message}")
        response = await agent.handle_message(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/image-search")
async def image_search(file: UploadFile = File(...)):
    try:
        logger.info(f"Received image search request: {file.filename}")
        products = await process_image_search(file)
        return {"products": products}
    except Exception as e:
        logger.error(f"Image search endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# Lambda handler
handler = Mangum(app)