from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langain_tavily import TavilySearch
from pydantic import BaseModel, Field
from typing import Optional, List

#search tool for combining online available recipies of Dishes

class RecipeResponse(BaseModel):
    dish_name: str = Field(description="Name of the dish")
    cuisine_type: Optional[str] = Field(description="Cuisine or origin of the dish")
    ItemList: List[str] = Field(description="List of ingredients with quantities")
    instructions: List[str] = Field(description="Step-by-step instructions to prepare the dish")
    tips_and_notes: Optional[str] = Field(description="Additional tips, variations, or serving suggestions")



search_tool = TavilySearch(
    max_results = 5,
    topic = "Food recepies"
)
prompt = """
You are an expert culinary assistant and recipe researcher. Your goal is to generate a complete, high-quality, and easy-to-follow recipe based on a dish name or description provided by another agent (the orchestrator).

You have access to a web search tool that retrieves relevant recipes and cooking guides from trusted culinary websites. Use it strategically to combine, validate, and enhance your recipe instructions.

Follow these steps meticulously:

1. **Understand the Request**: Identify the requested dish or cooking style. Determine if the user is asking for a particular cuisine, dietary preference, or preparation method.

2. **Search Strategically**: Use the search tool to retrieve up to 5 relevant and trustworthy recipe sources. Prioritize reputable websites like AllRecipes, Bon Appétit, NYT Cooking, Serious Eats, and Food Network.

3. **Synthesize a Single Recipe**:
   - Extract common and unique ingredients, quantities, cooking times, and preparation steps from the sources.
   - Consolidate the best elements into a unified, accurate recipe.
   - Ensure ingredients and instructions are complete, precise, and optimized for home cooking.

4. **Include Optional Enhancements**:
   - Mention common substitutions (e.g., dairy-free, vegan, gluten-free).
   - Include brief chef tips or notes that improve flavor, technique, or presentation.

5. **Return the Recipe in a Strictly Structured Format** matching this schema:
   - `dish_name`: Name of the dish
   - `cuisine_type`: Cuisine or origin (optional, if known)
   - `ItemList`: A list of ingredients with measurements (e.g., "2 tbsp olive oil")
   - `instructions`: A clear, numbered list of step-by-step instructions
   - `tips_and_notes`: Optional tips, variations, or warnings

**Tone and Style**:
Use a tone that is confident, informative, and encouraging—like a professional chef writing for an enthusiastic home cook. Be specific, never vague. Avoid filler phrases and always aim for clarity and precision.

Fact-check all key details, resolve contradictions in sources through reasoning, and prioritize usability and reliability of the final recipe.
"""

recipe_agent = create_react_agent(
    model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash"),
    tools = [search_tool],
    prompt = prompt
)