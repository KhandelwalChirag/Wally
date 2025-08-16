# Wally: Your Smart Shopping Assistant

Wally is an intelligent command-line shopping assistant that helps you build a Walmart shopping cart based on your goals, dishes, or specific item lists, all while adhering to your budget. It uses AI to expand your requests, find the best products, and optimize your cart for price and quality.

## Features ✨

  * **Natural Language Understanding:** Simply tell Wally what you want to buy, whether it's a list of items or a dish you want to make (e.g., "I need to buy milk, bread, and eggs for under $20" or "I want to make spaghetti for dinner").
  * **Intelligent Item Expansion:** If you provide a dish or a goal, Wally will expand it into a list of necessary ingredients.
  * **Automated Category Assignment:** Wally automatically assigns the most relevant Walmart.com category to each item on your list.
  * **Comprehensive Product Search:** It searches for the best product options on Walmart.com for each item, considering price, rating, and brand.
  * **Budget Optimization:** Wally selects the best combination of products to fit your budget, balancing cost and quality.
  * **Human-in-the-Loop Verification:** Before searching for products, you get to review and edit the generated item list to ensure it's exactly what you want.
  * **Automated Cart Generation:** Once the final product list is ready, Wally generates a pre-filled Walmart cart URL for you.
  * **Interactive API Key Setup:** If you haven't provided your API keys, the application will prompt you to enter them, creating a `.env` file for you.

## Project Structure

```
Wally-main/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── budget_optimizer.py
│   │   ├── cart_builder.py
│   │   ├── category_assigner.py
│   │   ├── input_interpreter.py
│   │   ├── item_extractor.py
│   │   ├── product_fetcher.py
│   │   ├── states.py
│   │   └── workflow.py
│   ├── .env.example
│   ├── .gitignore
│   ├── .python-version
│   ├── main.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── uv.lock
├── .gitignore
└── README.md
```

## Setup and Installation 🚀

Setting up Wally is easy\! Just follow the steps below. This project uses `uv` for fast and efficient Python package management.

### Prerequisites

  * **Python 3.11** or higher.
  * **uv**: If you don't have `uv` installed, you can install it with:
    ```bash
    pip install uv
    ```

### Installation

I've created setup scripts to make the installation process seamless.

**For macOS and Linux:**

1.  Open your terminal and navigate to the `backend` directory.

2.  Run the `setup.sh` script:

    ```bash
    sh setup.sh
    ```

**For Windows:**

1.  Open Command Prompt or PowerShell and navigate to the `backend` directory.

2.  Run the `setup.bat` script:

    ```bat
    setup.bat
    ```

These scripts will automatically create a virtual environment, activate it, and install all the required packages using `uv`.

## Usage

Once the setup is complete, you can run Wally with a simple command.

**For macOS and Linux:**

```bash
sh run.sh
```

**For Windows:**

```bat
run.bat
```

The application will then prompt you for your request. Here are a few examples of what you can ask Wally:

  * "I need milk, eggs, and bread for under $15"
  * "I want to make pasta for $20"
  * "Get me some cereal and yogurt"

Type `exit` when you're done to quit the application.

## API Key Setup

The first time you run Wally, it will check for a `.env` file. If it's not found, you'll be prompted to enter your `GOOGLE_API_KEY` and `TAVILY_API_KEY`. The application will then create a `.env` file for you automatically.

## Dependencies

Wally relies on a set of powerful libraries to function, including:

  * **LangGraph and LangChain:** For building the agentic workflow.
  * **Google Generative AI:** To power the AI agents.
  * **Tavily:** For comprehensive web searches.
  * **uv:** For Python package management.

All dependencies are listed in the `pyproject.toml` file and are installed automatically by the setup scripts.

-----
