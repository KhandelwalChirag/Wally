# Smart Cart Builder - Enhanced Version

This is an enhanced version of the Smart Cart Builder project with the following additional features:

## New Features

### 1. Human-in-the-Loop Functionality
- Category review: Users can review and modify AI-suggested categories for products
- Product review: Users can review product options found by the AI
- Optimization review: Users can accept or reject the AI's budget optimization

### 2. User Authentication
- User registration and login
- Secure token-based authentication
- User profile management

### 3. Hyper-Personalization
- Personalized product recommendations based on user history
- Preference-based search query enhancement
- Product ranking based on user preferences

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

## API Endpoints

### Authentication Endpoints
- `POST /register`: Register a new user
- `POST /token`: Login and get access token
- `GET /user/preferences`: Get user preferences
- `POST /user/preferences`: Update user preferences

### Chat Endpoints
- `POST /chat`: Process a user's shopping request
- `POST /resume`: Resume a conversation after human review

## Usage Guide

1. Register or login to enable personalization
2. Type your shopping request in the chat interface
3. Review and modify AI suggestions when prompted
4. Accept the final optimized cart
5. Click "Proceed to Walmart Cart" to continue to checkout