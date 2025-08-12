# Smart Cart Builder - Walmart Sparkathon

A multi-agent system that helps users build optimized shopping carts based on simple prompts.

## Architecture

- **Backend**: FastAPI + LangGraph multi-agent system
- **Frontend**: Vue 3 + TypeScript + Tailwind CSS browser extension
- **Agents**: Input interpreter, item expander, category assigner, product fetcher, budget optimizer, cart builder

## Setup

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

## Usage

1. Start the backend server
2. Open the browser extension
3. Type your shopping request (e.g., "I want to make pasta for $20")
4. View optimized product recommendations
5. Click "Go to Cart" to proceed

## Features

- Natural language input processing
- Goal/dish expansion into specific items
- Product category inference
- Real-time product search
- Budget-based optimization
- Simple, intuitive chat interface

## Note

This is a demo implementation. The Walmart API integration uses mock data since the actual API is not publicly accessible.