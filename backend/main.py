<<<<<<< HEAD
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from agents.workflow import graph
from agents.user_manager import user_manager
from database import init_database
from langgraph.types import Command
import os
import uuid
from dotenv import load_dotenv
=======
from flask import Flask
>>>>>>> parent of 288dd3f (extra changes - might work might not)

app = Flask(__name__)

<<<<<<< HEAD
# Initialize database on startup
init_database()

app = FastAPI(title="Cart Builder API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # In a real app, you would verify the token
    # For this demo, we'll just use the token as the username
    return token

# Optional authentication dependency
async def get_current_user_optional(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]  # Remove "Bearer " prefix
    return None

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str

# Chat models
class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
    user_id: Optional[str] = None

class ResumeRequest(BaseModel):
    thread_id: str
    data: Dict[str, Any]
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    thread_id: Optional[str] = None
    optimized_products: list
    cart_url: str
    message: str
    interrupt: Optional[Dict[str, Any]] = None

@app.post("/register")
async def register(user: UserCreate):
    success = user_manager.register_user(user.username, user.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_id = user_manager.authenticate(form_data.username, form_data.password)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user_id, "token_type": "bearer"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: Optional[str] = Depends(get_current_user_optional)):
    try:
        print(f"Received request: {request.message} from user: {user_id}")
        
        # Generate thread_id if not provided
        thread_id = request.thread_id or str(uuid.uuid4())
        
        # Configure thread
        config = {"configurable": {"thread_id": thread_id}}
        
        # Invoke the multi-agent workflow
        result = graph.invoke({"user_input": request.message, "user_id": user_id}, config=config)
        print(f"Graph result: {result}")
        
        # Check if we hit an interrupt
        if "__interrupt__" in result:
            interrupts = result["__interrupt__"]
            return ChatResponse(
                thread_id=thread_id,
                optimized_products=[],
                cart_url="",
                message="Waiting for your input",
                interrupt=interrupts[0].value if interrupts else None
            )
        
        # Extract optimized products and cart URL
        optimized_products = result.get("optimized_products", [])
        cart_url = result.get("cart_url", "")
        
        print(f"Optimized products: {optimized_products}")
        print(f"Cart URL: {cart_url}")
        
        # Create response message
        if optimized_products:
            total_price = sum(product.get("price", 0) for product in optimized_products)
            message = f"Found {len(optimized_products)} optimized products for ${total_price:.2f}"
            
            # Add to user's purchase history if authenticated
            if user_id:
                user_manager.add_to_purchase_history(user_id, optimized_products)
        else:
            message = "No products found. Please try a different request."
        
        return ChatResponse(
            thread_id=thread_id,
            optimized_products=optimized_products,
            cart_url=cart_url,
            message=message
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )

@app.post("/resume", response_model=ChatResponse)
async def resume_endpoint(request: ResumeRequest, user_id: Optional[str] = Depends(get_current_user_optional)):
    try:
        # Configure thread
        config = {"configurable": {"thread_id": request.thread_id}}
        
        # Resume the workflow with human input
        result = graph.invoke(Command(resume=request.data), config=config)
        
        # Check if we hit another interrupt
        if "__interrupt__" in result:
            interrupts = result["__interrupt__"]
            return ChatResponse(
                thread_id=request.thread_id,
                optimized_products=[],
                cart_url="",
                message="Waiting for your input",
                interrupt=interrupts[0].value if interrupts else None
            )
        
        # Extract optimized products and cart URL
        optimized_products = result.get("optimized_products", [])
        cart_url = result.get("cart_url", "")
        
        # Create response message
        if optimized_products:
            total_price = sum(product.get("price", 0) for product in optimized_products)
            message = f"Found {len(optimized_products)} optimized products for ${total_price:.2f}"
            
            # Add to user's purchase history if authenticated
            if user_id and cart_url:
                user_manager.add_to_purchase_history(user_id, optimized_products)
        else:
            message = "No products found. Please try a different request."
        
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=optimized_products,
            cart_url=cart_url,
            message=message
        )
    except Exception as e:
        print(f"Error in resume endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )

@app.get("/user/preferences")
async def get_preferences(user_id: str = Depends(get_current_user)):
    user_data = user_manager.get_user_data(user_id)
    return {"preferences": user_data.get("preferences", {})}

@app.post("/user/preferences")
async def update_preferences(preferences: Dict[str, Any], user_id: str = Depends(get_current_user)):
    user_manager.update_preferences(user_id, preferences)
    return {"message": "Preferences updated successfully"}

@app.get("/")
def root():
    return {"message": "Cart Builder API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
=======
@app.route("/")
def hello_world():
    return "<p> Hello World ! </p>"
>>>>>>> parent of 288dd3f (extra changes - might work might not)
