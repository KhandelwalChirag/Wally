# Smart Cart Builder - Walmart Sparkathon

A multi-agent AI system that helps users build optimized shopping carts based on simple prompts. The system processes natural language requests, expands them into specific items, searches for products, and optimizes selections based on budget constraints.

![Smart Cart Builder](https://github.com/your-username/Walmart-Sparkathon/raw/main/docs/images/smart-cart-builder.png)

## Features

### Core Capabilities
- **Natural Language Input Processing**: Understand user requests like "I want to make pasta for $20"
- **Goal/Dish Expansion**: Convert high-level goals into specific shopping items
- **Product Category Inference**: Automatically assign appropriate Walmart categories to items
- **Real-time Product Search**: Find relevant products using Tavily search API
- **Budget-based Optimization**: Select the best combination of products within budget constraints
- **Cart Generation**: Create a virtual shopping cart with optimized products

### User Experience
- **Simple Chat Interface**: Easy-to-use conversational UI
- **Product Cards**: Visual display of recommended products with details
- **Price Tracking**: Real-time calculation of total cart cost
- **One-click Checkout**: Direct link to Walmart cart for seamless checkout

## Architecture

### System Overview
The Smart Cart Builder uses a multi-agent architecture powered by LangGraph and LangChain:

```
User Input → Input Interpreter → Item Expander → Category Assigner → Product Fetcher → Budget Optimizer → Cart Builder → UI Display
```

### Components

#### Backend (FastAPI + LangGraph)
- **Input Interpreter Agent**: Analyzes user input to extract task type, item list, and budget
- **Item Expansion Agent**: Converts high-level goals into specific product needs
- **Category Assignment Agent**: Maps items to Walmart product categories
- **Product Search Agent**: Fetches product options using Tavily search API
- **Budget Optimizer Agent**: Selects optimal products within budget constraints
- **Cart Builder Agent**: Generates final cart and checkout URL

#### Frontend (Vue 3 + TypeScript + Tailwind CSS)
- **Browser Extension**: Chrome extension for easy access
- **Chatbot Interface**: Conversational UI for natural interaction
- **Product Display**: Visual cards showing optimized product selections
- **Responsive Design**: Works across different screen sizes
- **Animated UI**: Smooth transitions and loading states

## Technical Stack

### Backend
- **FastAPI**: High-performance API framework
- **LangGraph**: Multi-agent orchestration framework
- **LangChain**: LLM application framework
- **Google Gemini**: LLM for natural language understanding and reasoning
- **Tavily API**: Web search for product information
- **Python 3.11+**: Core programming language

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Next-generation frontend tooling
- **Chrome Extension API**: Browser integration

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from template:
```bash
cp .env.example .env
```

4. Add your API keys to `.env`:
```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

5. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to extension directory:
```bash
cd extension
```

2. Install dependencies:
```bash
npm install
```

3. Build the extension:
```bash
npm run build
```

4. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension` folder

## Usage Guide

1. Click on the Smart Cart Builder extension icon in your browser
2. Type your shopping request in the chat interface (examples):
   - "I need ingredients for spaghetti dinner for $25"
   - "Help me buy office supplies under $50"
   - "I want to make a birthday cake for $30"
3. Wait for the AI to process your request and display optimized product recommendations
4. Review the suggested products and total cost
5. Click "Proceed to Walmart Cart" to continue to checkout

## Agent Workflow

1. **Input Interpreter**:
   - Analyzes user input
   - Determines if input is a direct product list or a goal/dish
   - Extracts budget information

2. **Item Expansion** (for goals/dishes):
   - Converts high-level goals into specific items
   - Example: "pasta dinner" → ["spaghetti", "tomato sauce", "ground beef", "onion", "garlic"]

3. **Category Assignment**:
   - Maps each item to appropriate Walmart category
   - Example: "milk" → "Dairy & Eggs"

4. **Product Search**:
   - Searches for each item within its category
   - Retrieves multiple options with price, rating, brand, etc.

5. **Budget Optimization**:
   - Selects the best combination of products within budget
   - Balances price and quality/ratings

6. **Cart Building**:
   - Creates a virtual cart with selected products
   - Generates checkout URL

## Development

### Backend Development

The backend uses a state-based graph architecture with the following components:

- **States**: Defined in `agents/states.py`
- **Workflow**: Orchestrated in `agents/workflow.py`
- **Agent Nodes**: Individual agent implementations in separate files

To modify the agent behavior, edit the corresponding agent file:
- `agents/input_interpreter.py`
- `agents/item_extractor.py`
- `agents/category_assigner.py`
- `agents/product_fetcher.py`
- `agents/budget_optimizer.py`
- `agents/cart_builder.py`

### Frontend Development

The frontend is a Vue 3 application structured as a Chrome extension:

- **Main Component**: `src/components/Chatbot.vue`
- **Styling**: Tailwind CSS with custom animations
- **API Integration**: Fetch calls to backend endpoints

To run the development server:
```bash
npm run dev
```

## Notes

This is a demo implementation. The Walmart API integration uses mock data since the actual API is not publicly accessible. In a production environment, this would be replaced with official Walmart API calls.

## License

[MIT License](LICENSE)

## Contributors

- Your Name
- Team Members

## Acknowledgments

- Walmart for hosting the Sparkathon
- LangChain and LangGraph teams for the agent frameworks
- Google for Gemini API access