# Smart Cart Builder Backend

This is the backend component of the Smart Cart Builder project, a multi-agent system that helps users build optimized shopping carts based on natural language prompts.

## Architecture

The backend is built using a multi-agent architecture powered by LangGraph and LangChain, with FastAPI serving as the API framework.

### Agent Workflow

1. **Input Interpreter Agent** (`input_interpreter.py`)
   - Analyzes user input to extract task type, item list, and budget
   - Routes to Item Expansion Agent for goals/dishes or directly to Category Inference Agent for product lists

2. **Item Expansion Agent** (`item_extractor.py`)
   - Converts high-level goals/dishes into specific product needs
   - Example: "pasta dinner" → ["spaghetti", "tomato sauce", "ground beef", "onion", "garlic"]

3. **Category Inference Agent** (`category_assigner.py`)
   - Maps each item to appropriate Walmart category
   - Example: "milk" → "Dairy & Eggs"

4. **Product Search Agent** (`product_fetcher.py`)
   - Searches for each item within its category using Tavily Search API
   - Retrieves multiple options with price, rating, brand, etc.

5. **Budget Optimizer Agent** (`budget_optimizer.py`)
   - Selects the best combination of products within budget constraints
   - Balances price and quality/ratings

6. **Cart Builder Agent** (`cart_builder.py`)
   - Creates a virtual cart with selected products
   - Generates checkout URL

### State Management

The workflow is orchestrated using LangGraph's state management system:
- **States**: Defined in `agents/states.py`
- **Workflow**: Orchestrated in `agents/workflow.py`

## Technical Stack

- **FastAPI**: High-performance API framework
- **LangGraph**: Multi-agent orchestration framework
- **LangChain**: LLM application framework
- **Google Gemini**: LLM for natural language understanding and reasoning
- **Tavily API**: Web search for product information
- **Python 3.11+**: Core programming language

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file from template:
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

4. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /chat

Process a user's shopping request.

**Request:**
```json
{
  "message": "I want to make pasta for $20"
}
```

**Response:**
```json
{
  "optimized_products": [
    {
      "item": "spaghetti",
      "name": "Great Value Spaghetti Pasta",
      "price": 1.24,
      "rating": 4.7,
      "brand": "Great Value",
      "category": "Pasta & Noodles",
      "description": "16 oz, dried pasta"
    },
    ...
  ],
  "cart_url": "https://walmart.com/cart",
  "message": "Found 5 optimized products for $18.75"
}
```

### GET /

Health check endpoint.

**Response:**
```json
{
  "message": "Cart Builder API is running"
}
```

## Development

### Adding New Agents

1. Create a new agent file in the `agents` directory
2. Define the agent function with appropriate state handling
3. Add the agent to the workflow in `agents/workflow.py`

### Modifying Agent Behavior

To modify the behavior of an existing agent, edit the corresponding agent file:
- `agents/input_interpreter.py`
- `agents/item_extractor.py`
- `agents/category_assigner.py`
- `agents/product_fetcher.py`
- `agents/budget_optimizer.py`
- `agents/cart_builder.py`

## Notes

This is a demo implementation. The Walmart API integration uses mock data since the actual API is not publicly accessible. In a production environment, this would be replaced with official Walmart API calls.