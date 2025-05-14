from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from models import ChatRequest, RecommendRequest
from services.chat import get_chat_response
from services.recommendation import get_recommendations
from services.image_search import search_by_image
import boto3
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

@app.post("/chat")
async def chat(request: ChatRequest):
    response = get_chat_response(request.message)
    return {"response": response}

@app.post("/recommend")
async def recommend(request: RecommendRequest):
    products = get_recommendations(request.query)
    return {"products": products}

@app.post("/image-search")
async def image_search(file: UploadFile = File(...)):
    bucket = os.getenv('S3_BUCKET')
    file_name = f"uploads/{file.filename}"
    s3_client.upload_fileobj(file.file, bucket, file_name)
    products = search_by_image(f"s3://{bucket}/{file_name}")
    return {"products": products}

# Lambda handler
handler = Mangum(app)