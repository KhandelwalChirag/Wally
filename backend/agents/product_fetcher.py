from langchain_google_genai import ChatGoogleGenerativeAI
from agents.states import OverallState
from typing import Dict, Any, List, Literal
from langgraph.types import Command, interrupt
from langchain_tavily import TavilySearch
import json

def product_search_agent(state: OverallState) -> Command[Literal["budget_optimizer_agent"]]:
    categories = state.get("categories", {})
    products = []
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    tavily_search = TavilySearch(max_results=50)
    
    def fetch_products_for_item(item: str, category: str) -> List[Dict[str, Any]]:
        
        # Personalize the search query based on user preferences
        base_query = f"{item} {category} site:walmart.com price rating"
        search_results = tavily_search.invoke(base_query)
        
        prompt = f"""
You are a product information extractor. From the following search results about "{item}" from Walmart, 
extract exactly 5 different product options with these details:
- name: Product name
- price: Price as a number (extract from $X.XX format)
- rating: Rating out of 5 (if available, otherwise null)
- brand: Brand name
- category: Product category
- description: Brief description

Search Results:
{search_results}

Respond ONLY with a JSON array of exactly 5 product objects. If fewer than 5 products found, include what's available.
Example format:
[{{"name": "Product Name", "price": 12.99, "rating": 4.5, "brand": "Brand Name", "category": "{category}", "description": "Brief description"}}]
"""
        
        try:
            response = llm.invoke([{"role": "user", "content": prompt}])
            content = response.content.strip()
            
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            product_options = json.loads(content)
            
            valid_options = []
            for option in product_options:
                if isinstance(option, dict) and option.get('name') and option.get('price'):
                    # Ensure price is a number
                    try:
                        option['price'] = float(option['price'])
                        valid_options.append(option)
                    except (ValueError, TypeError):
                        continue
            
            return valid_options[:5]  # Limit to 5 options
            
        except Exception as e:
            print(f"Error extracting products for {item}: {e}")

            # Fallback: create mock products if extraction fails
            return [{
                "name": f"{item.title()} - Option 1",
                "price": 10.99,
                "rating": 4.0,
                "brand": "Generic",
                "category": category,
                "description": f"Quality {item} product"
            }]
    
    # Fetch products for each item
    for item, category in categories.items():
        product_options = fetch_products_for_item(item, category)
        
        products.append({
            "item": item,
            "category": category,
            "options": product_options
        })
    
    return Command(update={"products": products}, goto="budget_optimizer_agent")
