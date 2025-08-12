from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.workflow import graph
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Cart Builder API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    optimized_products: list
    cart_url: str
    message: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        print(f"Received request: {request.message}")
        
        # Invoke the multi-agent workflow
        result = graph.invoke({"user_input": request.message})
        print(f"Graph result: {result}")
        
        # Extract optimized products and cart URL
        optimized_products = result.get("optimized_products", [])
        cart_url = result.get("cart_url", "")
        
        print(f"Optimized products: {optimized_products}")
        print(f"Cart URL: {cart_url}")
        
        # Create response message
        if optimized_products:
            total_price = sum(product.get("price", 0) for product in optimized_products)
            message = f"Found {len(optimized_products)} optimized products for ${total_price:.2f}"
        else:
            message = "No products found. Please try a different request."
        
        return ChatResponse(
            optimized_products=optimized_products,
            cart_url=cart_url,
            message=message
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )

@app.get("/")
def root():
    return {"message": "Cart Builder API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)