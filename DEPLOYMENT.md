# Smart Cart Builder - Deployment Guide

## Database Setup

**Production Implementation**: PostgreSQL with LangGraph checkpointing
- **Database**: PostgreSQL 12+
- **Features**: ACID compliance, session management, thread-safe operations
- **Checkpointing**: Native LangGraph PostgresSaver support
- **Suitable for**: Production deployment, scalable applications

## Prerequisites

1. **Python 3.11+** installed
2. **Node.js 16+** and npm installed
3. **PostgreSQL 12+** installed and running
4. **Google Gemini API Key** (get from Google AI Studio)
5. **Tavily API Key** (get from Tavily.com)

## Step-by-Step Deployment

### 1. Database Setup

#### Windows:
```bash
cd backend
setup_db.bat
```

#### Linux/Mac:
```bash
cd backend
chmod +x setup_db.sh
./setup_db.sh
```

### 2. Backend Setup

#### Windows:
```bash
cd backend
start.bat
```

#### Linux/Mac:
```bash
cd backend
chmod +x start.sh
./start.sh
```

#### Manual Setup:
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your API keys:
# GOOGLE_API_KEY=your_google_api_key_here
# TAVILY_API_KEY=your_tavily_api_key_here
# DATABASE_URL=postgresql://smart_cart_user:smart_cart_password@localhost:5432/smart_cart_db

# Start server
python main.py
```

### 2. Frontend Setup

#### Windows:
```bash
cd extension
build.bat
```

#### Linux/Mac:
```bash
cd extension
chmod +x build.sh
./build.sh
```

#### Manual Setup:
```bash
cd extension

# Install dependencies
npm install

# Build extension
npm run build
```

### 3. Chrome Extension Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension` folder
5. The Smart Cart Builder extension should now appear in your extensions

### 4. Testing the Application

1. **Start Backend**: Ensure backend is running on `http://localhost:8000`
2. **Test API**: Visit `http://localhost:8000` - should show "Cart Builder API is running"
3. **Open Extension**: Click the extension icon in Chrome
4. **Test Features**:
   - Register a new user
   - Login with credentials
   - Send a chat message like "pasta dinner for $20"
   - Review category assignments when prompted
   - Review product options when prompted
   - Accept or reject optimization results

## API Endpoints

- `GET /` - Health check
- `POST /register` - User registration
- `POST /token` - User login
- `POST /chat` - Start conversation
- `POST /resume` - Resume after human review
- `GET /user/preferences` - Get user preferences
- `POST /user/preferences` - Update user preferences

## Database Management

### PostgreSQL Implementation:
- **Users**: Stored in `users` table with JSONB preferences
- **Purchase History**: Separate `purchase_history` table with JSONB product data
- **Session Management**: LangGraph PostgresSaver for conversation threads
- **Security**: SHA-256 password hashing, SQL injection protection
- **Backup**: Standard PostgreSQL backup tools (pg_dump)

### Database Schema:
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Purchase history table
CREATE TABLE purchase_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LangGraph checkpointer tables (auto-created)
-- checkpoints, checkpoint_blobs, checkpoint_writes
```

## Production Considerations

For production deployment, consider:

1. **Database Migration**: Replace file storage with PostgreSQL/MongoDB
2. **Authentication**: Implement JWT tokens with expiration
3. **Security**: Add HTTPS, rate limiting, input validation
4. **Scaling**: Use Redis for session management
5. **Monitoring**: Add logging and error tracking
6. **Deployment**: Use Docker containers

## Troubleshooting

### Common Issues:

1. **API Keys Missing**: Ensure `.env` file has valid API keys
2. **Port 8000 in use**: Change port in `main.py` or kill existing process
3. **Extension not loading**: Check Chrome developer console for errors
4. **CORS errors**: Ensure backend is running on localhost:8000

### Logs:
- Backend logs appear in terminal where you started the server
- Frontend logs in Chrome DevTools console

## File Structure
```
Walmart-Sparkathon/
├── backend/
│   ├── agents/
│   ├── user_data/          # Database files
│   ├── .env               # API keys
│   ├── main.py           # FastAPI server
│   ├── start.sh/.bat     # Startup scripts
│   └── requirements.txt
└── extension/
    ├── src/
    ├── dist/             # Built files
    ├── build.sh/.bat     # Build scripts
    └── package.json
```