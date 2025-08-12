from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, List
import json

def extract_user_preferences(purchase_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze purchase history to extract user preferences.
    Returns a dictionary of preferences.
    """
    if not purchase_history:
        return {}
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    prompt = (
        "You are an AI shopping assistant analyzing a user's purchase history. "
        "Based on the following purchase history, extract key preferences such as:\n"
        "- Preferred brands\n"
        "- Price sensitivity (budget, mid-range, premium)\n"
        "- Category preferences\n"
        "- Dietary preferences (if applicable)\n"
        "- Quality preferences (based on ratings)\n\n"
        "Respond ONLY with a JSON object containing these preferences.\n\n"
        f"Purchase History: {json.dumps(purchase_history, indent=2)}"
    )
    
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    try:
        content = response.content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        preferences = json.loads(content)
        return preferences
    except Exception as e:
        print(f"Error extracting preferences: {e}")
        return {}

def personalize_product_search(query: str, preferences: Dict[str, Any]) -> str:
    """
    Enhance search query with user preferences.
    """
    if not preferences:
        return query
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    prompt = (
        "You are an AI shopping assistant helping to personalize a product search. "
        "Given a basic search query and user preferences, enhance the query to include relevant preferences "
        "that would improve search results. Don't make the query too long.\n\n"
        f"Original Query: {query}\n"
        f"User Preferences: {json.dumps(preferences, indent=2)}\n\n"
        "Return ONLY the enhanced search query text."
    )
    
    response = llm.invoke([{"role": "user", "content": prompt}])
    enhanced_query = response.content.strip()
    
    # Remove quotes if the LLM added them
    if enhanced_query.startswith('"') and enhanced_query.endswith('"'):
        enhanced_query = enhanced_query[1:-1]
    
    return enhanced_query

def personalize_product_selection(products: List[Dict[str, Any]], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Rerank product options based on user preferences.
    """
    if not preferences or not products:
        return products
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    prompt = (
        "You are an AI shopping assistant helping to personalize product selections. "
        "Given a list of products and user preferences, rerank the products based on how well they match the preferences. "
        "Return the reranked products as a JSON array in the same format as the input.\n\n"
        f"Products: {json.dumps(products, indent=2)}\n"
        f"User Preferences: {json.dumps(preferences, indent=2)}\n\n"
        "Return ONLY the reranked products as a JSON array."
    )
    
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    try:
        content = response.content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        reranked_products = json.loads(content)
        if isinstance(reranked_products, list):
            return reranked_products
        return products
    except Exception as e:
        print(f"Error reranking products: {e}")
        return products