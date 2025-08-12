# Smart Cart Builder Enhancement Implementation Plan

This document outlines the step-by-step implementation process for adding three key enhancements to the Smart Cart Builder:

1. Human-in-the-loop functionality using LangGraph's interrupt mechanism
2. Hyper-personalization based on user history
3. User authentication and login

## 1. Human-in-the-Loop Functionality

### Backend Changes

#### Step 1: Set Up Checkpointing
Update `agents/workflow.py` to add checkpointing support:

```python
from langgraph.checkpoint.memory import InMemorySaver

# Create a checkpointer for saving graph state
checkpointer = InMemorySaver()

# Update graph compilation to use the checkpointer
graph = builder.compile(checkpointer=checkpointer)
```

#### Step 2: Add Interrupts to Key Agents
Modify the agents to include interrupt points for human review:

1. Update `agents/category_assigner.py`:

```python
from langgraph.types import interrupt

def category_inference_agent(state: OverallState):
    items = state.get("expanded_items") or state.get("item_list") or []
    
    if not items:
        return {"categories": {}}
    
    # Get categories using LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    # ... existing code to get categories ...
    
    # Add human review interrupt
    categories = interrupt({
        "type": "category_review",
        "items": items,
        "suggested_categories": categories,
        "message": "Please review the category assignments for these items."
    })
    
    print(f"Category inference result: {categories}")
    return {"categories": categories}
```

2. Update `agents/product_fetcher.py`:

```python
from langgraph.types import interrupt

def product_search_agent(state: OverallState):
    # ... existing code to fetch products ...
    
    # Add human review interrupt
    products = interrupt({
        "type": "product_review",
        "products": products,
        "message": "Please review the product options found for each item."
    })
    
    return {"products": products}
```

3. Update `agents/budget_optimizer.py`:

```python
from langgraph.types import interrupt

def budget_optimizer_agent(state: OverallState):
    # ... existing code to optimize products ...
    
    # Add human review interrupt
    optimized_products = interrupt({
        "type": "optimization_review",
        "optimized_products": optimized_products,
        "budget": state.get("budget"),
        "message": "Please review the optimized product selections."
    })
    
    return {"optimized_products": optimized_products}
```

#### Step 3: Update API Endpoint
Modify `main.py` to handle interrupts and resuming:

```python
import uuid
from langgraph.types import Command

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ResumeRequest(BaseModel):
    thread_id: str
    data: Dict[str, Any]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Generate thread_id if not provided
        thread_id = request.thread_id or str(uuid.uuid4())
        
        # Configure thread
        config = {"configurable": {"thread_id": thread_id}}
        
        # Invoke the multi-agent workflow
        result = graph.invoke({"user_input": request.message}, config=config)
        
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
        
        # Normal flow - return results
        return ChatResponse(
            thread_id=thread_id,
            optimized_products=result.get("optimized_products", []),
            cart_url=result.get("cart_url", ""),
            message=f"Found {len(result.get('optimized_products', []))} optimized products"
        )
    except Exception as e:
        # Error handling
        return ChatResponse(
            thread_id=request.thread_id or "",
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )

@app.post("/resume", response_model=ChatResponse)
async def resume_endpoint(request: ResumeRequest):
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
        
        # Normal flow - return results
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=result.get("optimized_products", []),
            cart_url=result.get("cart_url", ""),
            message=f"Found {len(result.get('optimized_products', []))} optimized products"
        )
    except Exception as e:
        # Error handling
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )
```

#### Step 4: Update Response Model
Update the `ChatResponse` model to include interrupt information:

```python
class ChatResponse(BaseModel):
    thread_id: str
    optimized_products: list
    cart_url: str
    message: str
    interrupt: Optional[Dict[str, Any]] = None
```

### Frontend Changes

#### Step 1: Update Chatbot Component
Modify `Chatbot.vue` to handle interrupts and provide feedback:

```vue
<template>
  <!-- Existing template code... -->
  
  <!-- Add interrupt handling UI -->
  <div v-if="currentInterrupt" class="bg-yellow-50 border border-yellow-200 rounded-xl p-4 my-4">
    <h3 class="font-bold text-lg mb-2">{{ currentInterrupt.message }}</h3>
    
    <!-- Category review interrupt -->
    <div v-if="currentInterrupt.type === 'category_review'" class="space-y-4">
      <div v-for="(category, item) in currentInterrupt.suggested_categories" :key="item" class="flex items-center">
        <span class="font-medium w-1/3">{{ item }}:</span>
        <input 
          v-model="interruptResponses[item]" 
          :placeholder="category"
          class="flex-1 border rounded-lg px-3 py-2"
        />
      </div>
      <button @click="submitInterruptResponse('category_review')" class="bg-blue-600 text-white px-4 py-2 rounded-lg">
        Submit Changes
      </button>
    </div>
    
    <!-- Product review interrupt -->
    <div v-else-if="currentInterrupt.type === 'product_review'" class="space-y-4">
      <!-- Product review UI -->
      <div v-for="(product, index) in currentInterrupt.products" :key="index" class="border-b pb-4">
        <h4 class="font-medium">{{ product.item }}</h4>
        <p>Category: {{ product.category }}</p>
        <p class="text-sm text-gray-600 mb-2">{{ product.options.length }} options found</p>
        <button @click="toggleProductOptions(index)" class="text-blue-600 text-sm">
          {{ expandedProducts.includes(index) ? 'Hide options' : 'Show options' }}
        </button>
        <div v-if="expandedProducts.includes(index)" class="mt-2 space-y-2">
          <div v-for="(option, optIndex) in product.options" :key="optIndex" class="pl-4 border-l-2 border-gray-200">
            <p>{{ option.name }} - ${{ option.price }}</p>
          </div>
        </div>
      </div>
      <button @click="submitInterruptResponse('product_review')" class="bg-blue-600 text-white px-4 py-2 rounded-lg">
        Accept Products
      </button>
    </div>
    
    <!-- Optimization review interrupt -->
    <div v-else-if="currentInterrupt.type === 'optimization_review'" class="space-y-4">
      <p class="text-sm text-gray-600">Budget: ${{ currentInterrupt.budget }}</p>
      <div v-for="(product, index) in currentInterrupt.optimized_products" :key="index" class="border-b pb-4">
        <div class="flex justify-between">
          <span>{{ product.name }}</span>
          <span class="font-bold">${{ product.price }}</span>
        </div>
        <p class="text-sm text-gray-600">{{ product.brand }} | Rating: {{ product.rating }}</p>
      </div>
      <div class="flex space-x-4">
        <button @click="submitInterruptResponse('optimization_review')" class="bg-green-600 text-white px-4 py-2 rounded-lg">
          Accept Selections
        </button>
        <button @click="rejectOptimization()" class="bg-red-600 text-white px-4 py-2 rounded-lg">
          Reject & Restart
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Add new state variables
const threadId = ref('')
const currentInterrupt = ref(null)
const interruptResponses = ref({})
const expandedProducts = ref([])

// Toggle product options visibility
const toggleProductOptions = (index: number) => {
  if (expandedProducts.value.includes(index)) {
    expandedProducts.value = expandedProducts.value.filter(i => i !== index)
  } else {
    expandedProducts.value.push(index)
  }
}

// Submit response to an interrupt
const submitInterruptResponse = async (type: string) => {
  try {
    isLoading.value = true
    
    let responseData = {}
    
    if (type === 'category_review') {
      // Merge original categories with user changes
      const originalCategories = currentInterrupt.value.suggested_categories
      const updatedCategories = {...originalCategories}
      
      // Apply user changes
      Object.entries(interruptResponses.value).forEach(([item, category]) => {
        if (category && category !== originalCategories[item]) {
          updatedCategories[item] = category
        }
      })
      
      responseData = updatedCategories
    } 
    else if (type === 'product_review') {
      // Accept products as is
      responseData = currentInterrupt.value.products
    }
    else if (type === 'optimization_review') {
      // Accept optimized products as is
      responseData = currentInterrupt.value.optimized_products
    }
    
    const response = await fetch('http://localhost:8000/resume', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        thread_id: threadId.value,
        data: responseData
      })
    })
    
    const data = await response.json()
    
    // Handle response
    if (data.interrupt) {
      // We hit another interrupt
      currentInterrupt.value = data.interrupt
      interruptResponses.value = {}
    } else {
      // Process completed
      currentInterrupt.value = null
      optimizedProducts.value = data.optimized_products
      cartUrl.value = data.cart_url
      
      messages.value.push({
        id: messageId++,
        text: data.message,
        isUser: false
      })
    }
  } catch (error) {
    messages.value.push({
      id: messageId++,
      text: "Error processing your feedback. Please try again.",
      isUser: false
    })
  } finally {
    isLoading.value = false
  }
}

// Reject optimization and restart
const rejectOptimization = () => {
  currentInterrupt.value = null
  messages.value.push({
    id: messageId++,
    text: "Let's try again. Please provide a new request.",
    isUser: false
  })
}

// Update sendMessage to handle thread_id
const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return
  
  const userMessage = inputMessage.value.trim()
  messages.value.push({ id: messageId++, text: userMessage, isUser: true })
  inputMessage.value = ''
  isLoading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message: userMessage,
        thread_id: threadId.value
      })
    })
    
    const data = await response.json()
    
    // Save thread_id for future requests
    if (data.thread_id) {
      threadId.value = data.thread_id
    }
    
    if (data.interrupt) {
      // We hit an interrupt
      currentInterrupt.value = data.interrupt
      interruptResponses.value = {}
    } else {
      // Normal flow
      optimizedProducts.value = data.optimized_products
      cartUrl.value = data.cart_url
      
      messages.value.push({
        id: messageId++,
        text: data.message,
        isUser: false
      })
    }
  } catch (error) {
    messages.value.push({
      id: messageId++,
      text: "Sorry, I'm having trouble connecting to the server. Please try again.",
      isUser: false
    })
  } finally {
    isLoading.value = false
  }
}
</script>
```

## 2. Hyper-Personalization

### Backend Changes

#### Step 1: Create User Preferences Schema
Create `models/user.py`:

```python
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class UserPreference(BaseModel):
    category_preferences: Dict[str, float] = {}  # Category -> weight
    brand_preferences: Dict[str, float] = {}     # Brand -> weight
    price_sensitivity: float = 0.5               # 0-1 scale, higher = more sensitive
    quality_preference: float = 0.5              # 0-1 scale, higher = prefers quality
    
class PurchaseHistory(BaseModel):
    item: str
    product_name: str
    brand: str
    category: str
    price: float
    rating: Optional[float] = None
    purchase_date: str
    
class UserProfile(BaseModel):
    user_id: str
    preferences: UserPreference = UserPreference()
    purchase_history: List[PurchaseHistory] = []
```

#### Step 2: Create User Database Interface
Create `db/user_db.py`:

```python
from models.user import UserProfile, PurchaseHistory, UserPreference
from typing import Dict, Optional, List
import json
import os
from datetime import datetime

# Simple file-based DB for demo purposes
# In production, use a real database

class UserDB:
    def __init__(self, db_path="./data/users"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
    
    def get_user(self, user_id: str) -> Optional[UserProfile]:
        file_path = f"{self.db_path}/{user_id}.json"
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            return UserProfile(**data)
    
    def save_user(self, user: UserProfile) -> None:
        file_path = f"{self.db_path}/{user.user_id}.json"
        with open(file_path, 'w') as f:
            json.dump(user.dict(), f)
    
    def add_purchase(self, user_id: str, purchase: PurchaseHistory) -> None:
        user = self.get_user(user_id)
        if not user:
            user = UserProfile(user_id=user_id)
        
        user.purchase_history.append(purchase)
        self._update_preferences(user)
        self.save_user(user)
    
    def _update_preferences(self, user: UserProfile) -> None:
        """Update user preferences based on purchase history"""
        if not user.purchase_history:
            return
            
        # Simple preference calculation
        # In production, use more sophisticated algorithms
        
        # Category preferences
        category_counts = {}
        for purchase in user.purchase_history:
            category_counts[purchase.category] = category_counts.get(purchase.category, 0) + 1
        
        total = sum(category_counts.values())
        user.preferences.category_preferences = {k: v/total for k, v in category_counts.items()}
        
        # Brand preferences
        brand_counts = {}
        for purchase in user.purchase_history:
            brand_counts[purchase.brand] = brand_counts.get(purchase.brand, 0) + 1
        
        total = sum(brand_counts.values())
        user.preferences.brand_preferences = {k: v/total for k, v in brand_counts.items()}
        
        # Price sensitivity (lower prices = higher sensitivity)
        prices = [p.price for p in user.purchase_history]
        if prices:
            # Normalize to 0-1 scale
            avg_price = sum(prices) / len(prices)
            # Inverse relationship - lower avg price = higher sensitivity
            user.preferences.price_sensitivity = min(1.0, max(0.1, 1.0 - (avg_price / 100)))
        
        # Quality preference (higher ratings = higher quality preference)
        ratings = [p.rating for p in user.purchase_history if p.rating is not None]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            # Direct relationship - higher avg rating = higher quality preference
            user.preferences.quality_preference = min(1.0, max(0.1, avg_rating / 5.0))
```

#### Step 3: Update State Schema
Modify `agents/states.py` to include user information:

```python
class OverallState(TypedDict):
    # Existing fields...
    
    # User fields
    user_id: NotRequired[str]
    user_preferences: NotRequired[Dict[str, Any]]
```

#### Step 4: Modify Budget Optimizer Agent
Update `agents/budget_optimizer.py` to use user preferences:

```python
from langgraph.types import interrupt

def budget_optimizer_agent(state: OverallState):
    """
    Uses LLM to select the best set of products under the user's budget.
    Incorporates user preferences if available.
    """
    products: List[Dict[str, Any]] = state.get("products", [])
    budget: Optional[float] = state.get("budget")
    user_id: Optional[str] = state.get("user_id")
    
    # Get user preferences if user_id is available
    user_preferences = state.get("user_preferences", None)
    if user_id and not user_preferences:
        from db.user_db import UserDB
        db = UserDB()
        user = db.get_user(user_id)
        if user:
            user_preferences = user.preferences.dict()
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    # Prepare a summary of product options for the LLM
    items_summary = []
    for prod in products:
        # ... existing code to prepare items_summary ...
    
    prompt = (
        "You are a smart shopping assistant. "
        "Given a list of items, each with several product options (with name, price, rating, brand, category, and description), "
        f"and a total budget of ${budget}, select the best combination of products so that the total price does not exceed the budget. "
    )
    
    # Include user preferences in the prompt if available
    if user_preferences:
        prompt += (
            f"\nUser Preferences:\n"
            f"- Category preferences: {user_preferences.get('category_preferences', {})}\n"
            f"- Brand preferences: {user_preferences.get('brand_preferences', {})}\n"
            f"- Price sensitivity: {user_preferences.get('price_sensitivity', 0.5)} (higher = more price sensitive)\n"
            f"- Quality preference: {user_preferences.get('quality_preference', 0.5)} (higher = prefers higher quality)\n"
            f"Prioritize products that match these preferences while staying within budget.\n"
        )
    
    prompt += (
        "Respond ONLY as a JSON array of selected product objects (with item, name, price, rating, brand, category, and description). "
        "Example:\n"
        '[{"item": "milk", "name": "Great Value Milk", "price": 3.5, "rating": 4.2, "brand": "Great Value", "category": "dairy", "description": "1 gallon whole milk"}, ...]\n\n'
        f"Items and options: {items_summary}"
    )
    
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    # ... existing code to parse response ...
    
    # Add human review interrupt with personalization context
    optimized_products = interrupt({
        "type": "optimization_review",
        "optimized_products": optimized_products,
        "budget": budget,
        "user_preferences": user_preferences,
        "message": "Please review the personalized product selections."
    })
    
    return {"optimized_products": optimized_products}
```

#### Step 5: Add Purchase Recording Endpoint
Update `main.py` to add an endpoint for recording purchases:

```python
from models.user import PurchaseHistory
from db.user_db import UserDB
from datetime import datetime

class PurchaseRequest(BaseModel):
    user_id: str
    purchases: List[Dict[str, Any]]

@app.post("/record_purchase")
async def record_purchase(request: PurchaseRequest):
    try:
        db = UserDB()
        
        for purchase_data in request.purchases:
            purchase = PurchaseHistory(
                item=purchase_data.get("item", ""),
                product_name=purchase_data.get("name", ""),
                brand=purchase_data.get("brand", ""),
                category=purchase_data.get("category", ""),
                price=purchase_data.get("price", 0.0),
                rating=purchase_data.get("rating"),
                purchase_date=datetime.now().isoformat()
            )
            db.add_purchase(request.user_id, purchase)
        
        return {"status": "success", "message": "Purchase recorded"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

#### Step 6: Update Chat Endpoint to Include User Preferences
Modify the chat endpoint in `main.py` to load user preferences:

```python
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Generate thread_id if not provided
        thread_id = request.thread_id or str(uuid.uuid4())
        
        # Configure thread
        config = {"configurable": {"thread_id": thread_id}}
        
        # Prepare input with user information if authenticated
        input_data = {"user_input": request.message}
        
        if request.user_id:
            input_data["user_id"] = request.user_id
            
            # Load user preferences if available
            db = UserDB()
            user = db.get_user(request.user_id)
            if user:
                input_data["user_preferences"] = user.preferences.dict()
        
        # Invoke the multi-agent workflow
        result = graph.invoke(input_data, config=config)
        
        # Rest of the function...
    except Exception as e:
        # Error handling...
```

### Frontend Changes

#### Step 1: Add Purchase Recording
Update `Chatbot.vue` to record purchases when checking out:

```typescript
// Add to script setup
const recordPurchase = async () => {
  if (!optimizedProducts.value.length || !userId.value) return
  
  try {
    await fetch('http://localhost:8000/record_purchase', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        user_id: userId.value,
        purchases: optimizedProducts.value
      })
    })
    
    // Show confirmation message
    messages.value.push({
      id: messageId++,
      text: "Your purchase has been recorded. Future recommendations will be personalized based on your preferences!",
      isUser: false
    })
  } catch (error) {
    console.error("Failed to record purchase:", error)
  }
}

// Modify goToCart to record purchase
const goToCart = () => {
  if (cartUrl.value) {
    recordPurchase()
    window.open(cartUrl.value, '_blank')
  }
}
```

#### Step 2: Update Chat Request to Include User ID
Modify the sendMessage function in `Chatbot.vue`:

```typescript
const sendMessage = async () => {
  // ... existing code ...
  
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ 
        message: userMessage,
        thread_id: threadId.value,
        user_id: userId.value  // Include user ID for personalization
      })
    })
    
    // ... rest of the function ...
  }
  // ... catch and finally blocks ...
}
```

#### Step 3: Add Personalization Indicator
Add a UI element to show when recommendations are personalized:

```vue
<!-- Add this near the product display -->
<div v-if="currentInterrupt?.user_preferences" class="bg-purple-100 text-purple-800 px-4 py-2 rounded-lg mb-4">
  <div class="flex items-center">
    <span class="material-icons mr-2">person</span>
    <span>Recommendations personalized based on your preferences</span>
  </div>
</div>
```

## 3. User Authentication

### Backend Changes

#### Step 1: Add Authentication Dependencies
Update `requirements.txt`:

```
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

#### Step 2: Create Authentication Models
Create `models/auth.py`:

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str
```

#### Step 3: Create Authentication Logic
Create `auth/auth.py`:

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.auth import TokenData, User, UserInDB

# Configuration
SECRET_KEY = "YOUR_SECRET_KEY"  # In production, use a secure key and store in environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock user database - replace with real DB in production
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

#### Step 4: Add Authentication Endpoints
Update `main.py` to add authentication endpoints:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
)
from models.auth import Token, User

# Add authentication endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Update chat endpoint to use authentication
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Generate thread_id if not provided
        thread_id = request.thread_id or str(uuid.uuid4())
        
        # Configure thread
        config = {"configurable": {"thread_id": thread_id}}
        
        # Prepare input with user information
        input_data = {"user_input": request.message, "user_id": current_user.username}
        
        # Load user preferences if available
        db = UserDB()
        user = db.get_user(current_user.username)
        if user:
            input_data["user_preferences"] = user.preferences.dict()
        
        # Invoke the multi-agent workflow
        result = graph.invoke(input_data, config=config)
        
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
        
        # Normal flow - return results
        return ChatResponse(
            thread_id=thread_id,
            optimized_products=result.get("optimized_products", []),
            cart_url=result.get("cart_url", ""),
            message=f"Found {len(result.get('optimized_products', []))} optimized products"
        )
    except Exception as e:
        # Error handling
        return ChatResponse(
            thread_id=request.thread_id or "",
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )
```

#### Step 5: Update Resume Endpoint to Use Authentication
Modify the resume endpoint to require authentication:

```python
@app.post("/resume", response_model=ChatResponse)
async def resume_endpoint(
    request: ResumeRequest,
    current_user: User = Depends(get_current_active_user)
):
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
        
        # Normal flow - return results
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=result.get("optimized_products", []),
            cart_url=result.get("cart_url", ""),
            message=f"Found {len(result.get('optimized_products', []))} optimized products"
        )
    except Exception as e:
        # Error handling
        return ChatResponse(
            thread_id=request.thread_id,
            optimized_products=[],
            cart_url="",
            message=f"Error processing request: {str(e)}"
        )
```

### Frontend Changes

#### Step 1: Add Login Component
Create `src/components/Login.vue`:

```vue
<template>
  <div class="flex flex-col h-[700px] w-[450px] bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 border-0 rounded-3xl shadow-2xl overflow-hidden animate-fade-in">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 text-white p-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>
      <div class="flex items-center space-x-4 relative z-10">
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center animate-bounce-slow">
          🛒
        </div>
        <div>
          <h2 class="text-2xl font-bold bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent">Wally</h2>
          <p class="text-blue-100 text-sm animate-pulse">Your Walmart Ally for best shopping Experience</p>
        </div>
      </div>
    </div>

    <!-- Login Form -->
    <div class="flex-1 flex items-center justify-center p-8">
      <form @submit.prevent="login" class="w-full max-w-md space-y-6">
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>
        
        <div class="space-y-2">
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input 
            v-model="username" 
            type="text" 
            id="username"
            class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <div class="space-y-2">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input 
            v-model="password" 
            type="password" 
            id="password"
            class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <button 
          type="submit"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 text-white py-4 px-8 rounded-2xl hover:from-blue-700 hover:via-purple-700 hover:to-indigo-800 font-bold text-lg shadow-2xl transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
        >
          <span v-if="isLoading">Logging in...</span>
          <span v-else>Login</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const emit = defineEmits(['login-success'])

const login = async () => {
  if (!username.value || !password.value) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password', password.value)
    
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Login failed')
    }
    
    const data = await response.json()
    
    // Store token in localStorage
    localStorage.setItem('token', data.access_token)
    
    // Emit success event with username
    emit('login-success', data.username)
  } 
  catch (err) {
    error.value = err.message || 'Login failed'
  }
  finally {
    isLoading.value = false
  }
}
</script>
```

#### Step 2: Update App.vue to Handle Authentication
Update `App.vue`:

```vue
<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <Login v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
    <Chatbot v-else :userId="userId" @logout="handleLogout" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Chatbot from './components/Chatbot.vue'
import Login from './components/Login.vue'

const isLoggedIn = ref(false)
const userId = ref('')

onMounted(() => {
  // Check if user is already logged in
  const token = localStorage.getItem('token')
  if (token) {
    // Validate token by fetching user info
    validateToken()
  }
})

const validateToken = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/users/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const userData = await response.json()
      userId.value = userData.username
      isLoggedIn.value = true
    } else {
      // Token invalid, clear it
      localStorage.removeItem('token')
      isLoggedIn.value = false
    }
  } catch (error) {
    console.error('Token validation failed:', error)
    localStorage.removeItem('token')
    isLoggedIn.value = false
  }
}

const handleLoginSuccess = (username: string) => {
  userId.value = username
  isLoggedIn.value = true
}

const handleLogout = () => {
  localStorage.removeItem('token')
  isLoggedIn.value = false
  userId.value = ''
}
</script>
```

#### Step 3: Update Chatbot.vue to Include User ID and Token
Update `Chatbot.vue`:

```vue
<template>
  <!-- Add logout button to header -->
  <div class="flex flex-col h-[700px] w-[450px] bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 border-0 rounded-3xl shadow-2xl overflow-hidden animate-fade-in">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700 text-white p-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>
      <div class="flex items-center justify-between relative z-10">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center animate-bounce-slow">
            🛒
          </div>
          <div>
            <h2 class="text-2xl font-bold bg-gradient-to-r from-white to-blue-100 bg-clip-text text-transparent">Wally</h2>
            <p class="text-blue-100 text-sm animate-pulse">Your Walmart Ally for best shopping Experience</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <span class="text-white text-sm bg-white/20 px-3 py-1 rounded-full">{{ userId }}</span>
          <button @click="logout" class="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg text-sm">
            Logout
          </button>
        </div>
      </div>
    </div>
    
    <!-- Rest of the template... -->
  </div>
</template>

<script setup lang="ts">
// Add props and emits
const props = defineProps<{
  userId: string
}>()

const emit = defineEmits(['logout'])

// Add logout function
const logout = () => {
  emit('logout')
}

// Modify API calls to include authorization header
const sendMessage = async () => {
  // ...existing code...
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ 
        message: userMessage,
        thread_id: threadId.value,
        user_id: props.userId
      })
    })
    
    // ...rest of the function...
  }
  // ...catch and finally blocks...
}

// Update submitInterruptResponse to include authorization
const submitInterruptResponse = async (type: string) => {
  try {
    // ...existing code...
    
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/resume', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        thread_id: threadId.value,
        data: responseData
      })
    })
    
    // ...rest of the function...
  }
  // ...catch and finally blocks...
}
</script>
```

## Implementation Timeline

### Phase 1: Human-in-the-Loop with LangGraph Interrupts (2 weeks)
1. Week 1: Backend implementation
   - Set up checkpointing
   - Add interrupts to key agents
   - Update API endpoints for interrupt handling

2. Week 2: Frontend implementation
   - Add interrupt handling UI components
   - Implement resume functionality
   - Test and refine the interrupt flow

### Phase 2: User Authentication (1 week)
1. Days 1-2: Backend implementation
   - Set up authentication models and logic
   - Add authentication endpoints
   - Secure existing endpoints

2. Days 3-5: Frontend implementation
   - Create login component
   - Update App.vue for authentication flow
   - Modify API calls to include authentication
   - Test and debug

### Phase 3: Hyper-Personalization (2 weeks)
1. Week 1: Backend implementation
   - Create user preferences schema
   - Implement user database interface
   - Modify budget optimizer agent

2. Week 2: Frontend implementation
   - Add purchase recording
   - Test personalization features
   - Refine algorithms based on testing

### Phase 4: Integration and Testing (1 week)
1. Days 1-3: Integration testing
   - Test all features together
   - Fix integration issues

2. Days 4-5: User testing and refinement
   - Gather feedback
   - Make final adjustments

## Conclusion

This implementation plan outlines the steps needed to add human-in-the-loop functionality using LangGraph's interrupt mechanism, hyper-personalization based on user history, and user authentication to the Smart Cart Builder project. These enhancements will significantly improve the user experience by allowing for real-time feedback, learning from user preferences, and providing secure access to personalized recommendations.

Key benefits:
- Users can review and modify AI recommendations at multiple stages of the workflow
- System learns from user preferences and purchase history to provide personalized recommendations
- Secure authentication protects user data and enables personalization
- Enhanced user experience with real-time interaction and personalized product selections

The implementation leverages LangGraph's powerful interrupt mechanism to create a truly interactive shopping assistant that can pause, get human feedback, and continue processing based on that feedback.