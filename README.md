Free AI Commerce Agent Project
Overview
This is a cost-optimized version of an AI-powered commerce agent, similar to Amazon Rufus, offering general conversation, text-based product recommendations, and image-based product search. It’s designed to stay within AWS Free Tier limits and uses no paid third-party services.
Tech Stack

Frontend: React with Tailwind CSS for a responsive interface.
Backend: AWS Lambda (Python) with FastAPI, served via API Gateway.
AI Models:
Conversation: Hugging Face facebook/blenderbot-400M-distill.
Text Recommendations: Sentence Transformers (all-MiniLM-L6-v2).
Image Search: CLIP (openai/clip-vit-base-patch32).


Vector Search: FAISS for local embedding storage and search.
Storage: AWS S3 for image uploads.
Deployment: AWS Lambda for backend, AWS Amplify for frontend, AWS API Gateway for API routing.

Why This Stack?

AWS Lambda: Free tier offers 1M requests/month, ideal for low-traffic apps.
FAISS: Free, lightweight alternative to Pinecone for vector search.
S3: Free tier provides 5GB storage, sufficient for image uploads.
Amplify: Free hosting for static React apps.
Hugging Face Models: Open-source and free, optimized for small-scale use.
FastAPI: Lightweight, works well in Lambda with minimal overhead.

Project Structure
free-ai-commerce-agent/
├── backend/
│   ├── main.py              # FastAPI Lambda handler
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── chat.py          # Conversation logic
│   │   ├── recommendation.py # Text-based recommendation
│   │   ├── image_search.py  # Image-based search
│   ├── requirements.txt      # Python dependencies
│   ├── serverless.yml       # Serverless framework config
│   └── faiss_index/         # FAISS index storage
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── components/      # UI components
│   │   ├── assets/          # Static assets
│   ├── public/              # Static files
│   ├── package.json         # Node dependencies
│   └── tailwind.config.js   # Tailwind CSS config
├── README.md                # Project documentation
└── scripts/
    └── deploy.sh            # Deployment script

Setup Instructions
Prerequisites

Python 3.10+
Node.js 18+
AWS CLI configured with Free Tier account credentials
Serverless Framework CLI (npm install -g serverless)
Git and GitHub CLI (gh) installed

Local Setup

Clone the Repository (after creating it, see GitHub section below):
git clone https://github.com/your-username/free-ai-commerce-agent.git
cd free-ai-commerce-agent


Backend Setup:
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Create a .env file in backend/:
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET=your-s3-bucket-name

Run locally (requires mangum for Lambda simulation):
uvicorn main:app --reload


Frontend Setup:
cd frontend
npm install
npm start

The frontend runs at http://localhost:3000.

Initialize FAISS Index:

Run backend/services/recommendation.py to generate a sample FAISS index with product data.
Store the index in backend/faiss_index/ (included in Lambda deployment).



GitHub Repository Setup

Create the Repository:
gh repo create free-ai-commerce-agent --public --source=. --remote=origin


Push Code to GitHub:
git init
git add .
git commit -m "Initial commit: Free AI Commerce Agent"
git push -u origin main


Add .gitignore:Create .gitignore in the root:
# Python
venv/
__pycache__/
*.pyc
.env

# Node
node_modules/
build/

# AWS
.serverless/



Deployment

Backend (AWS Lambda via Serverless Framework):
cd backend
serverless deploy


This deploys the Lambda function and API Gateway.
Set environment variables in serverless.yml or AWS Console:
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
S3_BUCKET


Note: Ensure the Lambda function has an S3 access policy (see serverless.yml).


Frontend (AWS Amplify):

Connect the frontend directory to AWS Amplify via the AWS Console.
Configure build settings:version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm install
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*


Deploy via Amplify.


API Gateway:

The serverless deploy command creates an API Gateway endpoint.
Copy the endpoint URL (e.g., https://xyz.execute-api.us-east-1.amazonaws.com/dev) and update the frontend API calls.



API Documentation
Base URL
https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev
Endpoints

General Conversation

POST /chat
Request:{
  "message": "What's your name?"
}


Response:{
  "response": "I'm CommerceBot, your shopping assistant!"
}




Text-Based Product Recommendation

POST /recommend
Request:{
  "query": "t-shirt for sports"
}


Response:{
  "products": [
    {"id": "1", "name": "Sports T-Shirt", "price": 29.99},
    ...
  ]
}




Image-Based Product Search

POST /image-search
Request: Form-data with image (file)
Response:{
  "products": [
    {"id": "2", "name": "Blue Sneakers", "price": 59.99},
    ...
  ]
}





Backend Code
backend/main.py
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

backend/models.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class RecommendRequest(BaseModel):
    query: str

backend/services/chat.py
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

def get_chat_response(message: str) -> str:
    inputs = tokenizer(message, return_tensors="pt")
    reply_ids = model.generate(**inputs)
    response = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    return response

backend/services/recommendation.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # Dimension for all-MiniLM-L6-v2

# Sample product data
products = [
    {"id": "1", "name": "Sports T-Shirt", "price": 29.99},
    {"id": "2", "name": "Blue Sneakers", "price": 59.99},
]

# Initialize FAISS index
embeddings = model.encode([p["name"] for p in products])
index.add(np.array(embeddings))

def get_recommendations(query: str):
    query_embedding = model.encode([query])[0]
    D, I = index.search(np.array([query_embedding]), k=5)
    return [products[i] for i in I[0]]

backend/services/image_search.py
from transformers import CLIPProcessor, CLIPModel
import boto3
import faiss
import numpy as np
import os
from PIL import Image

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
index = faiss.IndexFlatL2(512)  # Dimension for CLIP

s3_client = boto3.client('s3')

# Sample product data (same as recommendation.py)
products = [
    {"id": "1", "name": "Sports T-Shirt", "price": 29.99},
    {"id": "2", "name": "Blue Sneakers", "price": 59.99},
]

# Initialize FAISS index for images (using text embeddings for simplicity)
embeddings = model.get_text_features(**processor(text=[p["name"] for p in products], return_tensors="pt")).detach().numpy()
index.add(embeddings)

def search_by_image(s3_path: str):
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    local_path = f"/tmp/{key.split('/')[-1]}"
    s3_client.download_file(bucket, key, local_path)
    
    image = Image.open(local_path)
    inputs = processor(images=image, return_tensors="pt")
    image_embedding = model.get_image_features(**inputs).detach().numpy()
    
    D, I = index.search(image_embedding, k=5)
    return [products[i] for i in I[0]]

backend/requirements.txt
fastapi==0.95.1
mangum==0.17.0
pydantic==1.10.7
transformers==4.28.1
sentence-transformers==2.2.2
faiss-cpu==1.7.4
boto3==1.26.100
pillow==9.5.0

backend/serverless.yml
service: free-ai-commerce-agent

provider:
  name: aws
  runtime: python3.10
  region: us-east-1
  environment:
    AWS_ACCESS_KEY_ID: ${env:AWS_ACCESS_KEY_ID}
    AWS_SECRET_ACCESS_KEY: ${env:AWS_SECRET_ACCESS_KEY}
    AWS_REGION: ${env:AWS_REGION}
    S3_BUCKET: ${env:S3_BUCKET}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - s3:PutObject
            - s3:GetObject
          Resource: "arn:aws:s3:::${env:S3_BUCKET}/*"

functions:
  api:
    handler: main.handler
    events:
      - http:
          path: /
          method: ANY
          cors: true
      - http:
          path: /{proxy+}
          method: ANY
          cors: true

package:
  patterns:
    - '!venv/**'
    - '!__pycache__/**'
    - '*.py'
    - 'faiss_index/**'

Frontend Code
frontend/src/App.jsx
import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import Recommendation from './components/Recommendation';
import ImageSearch from './components/ImageSearch';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-6">Free AI Commerce Agent</h1>
      <div className="w-full max-w-2xl">
        <div className="flex mb-4">
          <button
            className={`px-4 py-2 ${activeTab === 'chat' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
          <button
            className={`px-4 py-2 ${activeTab === 'recommend' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveTab('recommend')}
          >
            Recommend
          </button>
          <button
            className={`px-4 py-2 ${activeTab === 'image' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveTab('image')}
          >
            Image Search
          </button>
        </div>
        {activeTab === 'chat' && <ChatBox />}
        {activeTab === 'recommend' && <Recommendation />}
        {activeTab === 'image' && <ImageSearch />}
      </div>
    </div>
  );
}

export default App;

frontend/src/components/ChatBox.jsx
import React, { useState } from 'react';

function ChatBox() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    const res = await fetch('https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="text"
        className="w-full p-2 border rounded mb-2"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSubmit}>
        Send
      </button>
      {response && <p className="mt-2">Response: {response}</p>}
    </div>
  );
}

export default ChatBox;

frontend/src/components/Recommendation.jsx
import React, { useState } from 'react';

function Recommendation() {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);

  const handleSubmit = async () => {
    const res = await fetch('https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setProducts(data.products);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="text"
        className="w-full p-2 border rounded mb-2"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="e.g., t-shirt for sports"
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSubmit}>
        Search
      </button>
      <div className="mt-4">
        {products.map((product) => (
          <div key={product.id} className="border p-2 mb-2">
            <p>{product.name}</p>
            <p>${product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recommendation;

frontend/src/components/ImageSearch.jsx
import React, { useState } from 'react';

function ImageSearch() {
  const [file, setFile] = useState(null);
  const [products, setProducts] = useState([]);

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('image', file);
    const res = await fetch('https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev/image-search', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setProducts(data.products);
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <input
        type="file"
        accept="image/*"
        className="mb-2"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSubmit}>
        Search
      </button>
      <div className="mt-4">
        {products.map((product) => (
          <div key={product.id} className="border p-2 mb-2">
            <p>{product.name}</p>
            <p>${product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ImageSearch;

frontend/package.json
{
  "name": "free-ai-commerce-agent-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "tailwindcss": "^3.3.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}

frontend/tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};

Deployment Script
scripts/deploy.sh
#!/bin/bash

# Backend
cd backend
serverless deploy

# Frontend
cd ../frontend
npm run build
amplify publish

How to Use

General Conversation:
Navigate to the "Chat" tab.
Ask questions like "What's your name?" or "What can you do?".


Text-Based Recommendations:
Go to the "Recommend" tab.
Enter queries like "t-shirt for sports".
View matching products.


Image-Based Search:
Select the "Image Search" tab.
Upload an image of a product.
See similar products.



Notes

Replace https://your-api-gateway-id.execute-api.us-east-1.amazonaws.com/dev in frontend code with the actual API Gateway URL after deployment.
The FAISS index is in-memory and small-scale. For production, persist to S3 or use a database.
Monitor AWS Free Tier usage (Lambda, S3, Amplify) to avoid unexpected charges.
Create an S3 bucket manually before deployment and grant Lambda access via IAM.
The GitHub repository is public; use a private repo if needed (requires GitHub Pro).

Cost Considerations

Lambda: 1M requests/month free; keep requests low during testing.
API Gateway: 1M requests/month free; monitor usage.
S3: 5GB storage free; clean up unused images.
Amplify: 5GB hosting free; avoid frequent rebuilds.
FAISS: Free, but memory-limited in Lambda (increase Lambda memory if needed, within free tier).

Future Improvements

Persist FAISS index to S3 for larger catalogs.
Add rate limiting to API Gateway to prevent overuse.
Optimize Lambda memory for faster model inference.
Integrate a free database (e.g., DynamoDB Free Tier) for product data.

