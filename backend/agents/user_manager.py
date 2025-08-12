from typing import Dict, Any, List, Optional
import hashlib
from sqlalchemy import text
from database import get_session
import json

class UserManager:
    """
    Manages user authentication and personalization data using PostgreSQL.
    """
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate a user and return their user_id if successful."""
        session = get_session()
        try:
            result = session.execute(
                text("SELECT username FROM users WHERE username = :username AND password_hash = :password_hash"),
                {"username": username, "password_hash": self._hash_password(password)}
            ).fetchone()
            return result[0] if result else None
        finally:
            session.close()
    
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user."""
        session = get_session()
        try:
            # Check if user exists
            existing = session.execute(
                text("SELECT id FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            
            if existing:
                return False
            
            # Create new user
            session.execute(
                text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)"),
                {"username": username, "password_hash": self._hash_password(password)}
            )
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_user_data(self, username: str) -> Dict[str, Any]:
        """Get user preferences and purchase history."""
        session = get_session()
        try:
            # Get user preferences
            user_result = session.execute(
                text("SELECT id, preferences FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            
            if not user_result:
                return {"preferences": {}, "purchase_history": []}
            
            user_id, preferences = user_result
            
            # Get purchase history
            history_results = session.execute(
                text("SELECT product_data FROM purchase_history WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 50"),
                {"user_id": user_id}
            ).fetchall()
            
            purchase_history = [row[0] for row in history_results]
            
            return {
                "preferences": preferences or {},
                "purchase_history": purchase_history
            }
        finally:
            session.close()
    
    def update_preferences(self, username: str, preferences: Dict[str, Any]):
        """Update user preferences."""
        session = get_session()
        try:
            # Get current preferences
            current = session.execute(
                text("SELECT preferences FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            
            if current:
                current_prefs = current[0] or {}
                updated_prefs = {**current_prefs, **preferences}
                
                session.execute(
                    text("UPDATE users SET preferences = :preferences, updated_at = CURRENT_TIMESTAMP WHERE username = :username"),
                    {"username": username, "preferences": json.dumps(updated_prefs)}
                )
                session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
    
    def add_to_purchase_history(self, username: str, products: List[Dict[str, Any]]):
        """Add products to user's purchase history."""
        session = get_session()
        try:
            # Get user ID
            user_result = session.execute(
                text("SELECT id FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            
            if user_result:
                user_id = user_result[0]
                
                # Add each product to history
                for product in products:
                    session.execute(
                        text("INSERT INTO purchase_history (user_id, product_data) VALUES (:user_id, :product_data)"),
                        {"user_id": user_id, "product_data": json.dumps(product)}
                    )
                
                session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

# Create a singleton instance
user_manager = UserManager()