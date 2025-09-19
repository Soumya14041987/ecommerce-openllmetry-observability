from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from traceloop.sdk import Traceloop
from openai import OpenAI
import time
import random
from pydantic import BaseModel
from typing import List, Optional

# Initialize OpenLLMetry
Traceloop.init(
    app_name="ecommerce-app",
    disable_batch=True,
    resource_attributes={
        "service.name": "ecommerce-service",
        "service.version": "1.0.0"
    }
)

app = FastAPI(title="E-commerce OpenLLMetry Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "demo-key"))

# Sample product data
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "name": "Smartphone", "price": 699.99, "category": "Electronics"},
    {"id": 3, "name": "Headphones", "price": 199.99, "category": "Electronics"},
    {"id": 4, "name": "Book", "price": 19.99, "category": "Books"},
    {"id": 5, "name": "Coffee Mug", "price": 12.99, "category": "Home"},
]

class ChatMessage(BaseModel):
    message: str

class ProductQuery(BaseModel):
    query: str
    budget: Optional[float] = None

@app.get("/")
async def root():
    return {"message": "E-commerce OpenLLMetry Demo", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/products")
async def get_products():
    """Get all products"""
    # Simulate some processing time
    time.sleep(random.uniform(0.1, 0.3))
    return {"products": PRODUCTS}

@app.post("/recommendations")
async def get_recommendations(query: ProductQuery):
    """Get AI-powered product recommendations"""
    try:
        prompt = f"""
        Based on the user query: "{query.query}"
        Budget: ${query.budget if query.budget else 'No limit'}
        
        Available products:
        {PRODUCTS}
        
        Recommend the most suitable products and explain why.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        return {
            "query": query.query,
            "recommendations": response.choices[0].message.content,
            "token_usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")

@app.post("/chatbot")
async def chatbot(message: ChatMessage):
    """Customer support chatbot"""
    try:
        prompt = f"""
        You are a helpful e-commerce customer support assistant.
        Customer message: "{message.message}"
        
        Provide a helpful response about our products, shipping, returns, or general support.
        Keep responses concise and friendly.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.5
        )
        
        return {
            "user_message": message.message,
            "bot_response": response.choices[0].message.content,
            "token_usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@app.post("/search")
async def semantic_search(query: ProductQuery):
    """Semantic product search"""
    try:
        prompt = f"""
        Search query: "{query.query}"
        
        Available products:
        {PRODUCTS}
        
        Find products that match the search intent and rank them by relevance.
        Return a JSON list of matching product IDs with relevance scores.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.3
        )
        
        # Simulate search results
        matching_products = [p for p in PRODUCTS if query.query.lower() in p["name"].lower()]
        
        return {
            "query": query.query,
            "results": matching_products,
            "ai_analysis": response.choices[0].message.content,
            "token_usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """Expose custom metrics"""
    return {
        "total_products": len(PRODUCTS),
        "active_sessions": random.randint(10, 100),
        "avg_response_time": random.uniform(0.1, 0.5),
        "error_rate": random.uniform(0.01, 0.05)
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )