# Commerce AI Agent

An AI-powered shopping assistant for a commerce website, featuring general conversation, text-based product recommendations, and image-based product search. The agent integrates with Amazon's product catalog (simulated for this demo) to recommend real products.

## Features
- **General Conversation**: Responds to queries like "What's your name?" or "What can you do?".
- **Text-Based Product Recommendation**: Recommends products based on user input (e.g., "Recommend me a t-shirt for sports").
- **Image-Based Product Search**: Searches products by analyzing uploaded images (currently uses color detection).

## Architecture
- **Frontend**: React with Tailwind CSS for a responsive chat and image upload interface.
- **Backend**: FastAPI deployed on AWS Lambda via Serverless Framework for scalability.
- **AI**: OpenAI's GPT-4o-mini for natural language processing and conversation.
- **Product Search**: Simulated Amazon Product Advertising API integration (replace with real API for production).
- **Image Processing**: OpenCV with k-means clustering for color-based product matching.

## Tech Stack Choices
- **React**: Lightweight, component-based frontend for rapid development.
- **FastAPI**: High-performance, async-capable API framework for Python.
- **AWS Lambda**: Serverless deployment for cost-efficiency and scalability.
- **OpenAI**: Provides robust NLP capabilities for conversation and recommendations.
- **OpenCV**: Simple, effective image processing for color detection (CLIP could be added for advanced vision).
- **Amazon API**: Chosen for access to a vast product catalog (simulated here due to credential requirements).

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yng-nimish/agent.git
   cd commerce-ai-agent



