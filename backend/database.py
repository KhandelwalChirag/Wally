import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/smart_cart_db")

def get_database_engine():
    """Get SQLAlchemy engine for database operations"""
    return create_engine(DATABASE_URL)

def get_session():
    """Get database session"""
    engine = get_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_postgres_checkpointer():
    """Get PostgreSQL checkpointer for LangGraph"""
    checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
    checkpointer.setup()  # Create tables if they don't exist
    return checkpointer

def init_database():
    """Initialize database tables"""
    engine = get_database_engine()
    
    # Create user management tables
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                preferences JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS purchase_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                product_data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            CREATE INDEX IF NOT EXISTS idx_purchase_history_user_id ON purchase_history(user_id);
            CREATE INDEX IF NOT EXISTS idx_purchase_history_created_at ON purchase_history(created_at);
        """))
        
        conn.commit()
    
    print("Database initialized successfully")