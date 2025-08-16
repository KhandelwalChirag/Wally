import argparse
import asyncio
import json
import os
import shutil
from agents.workflow import graph
from langgraph.types import Command
from dotenv import load_dotenv

def setup_api_keys():
    """
    Checks for a .env file and prompts the user for API keys if it doesn't exist.
    """
    if not os.path.exists(".env"):
        print("API keys not found. Please enter your API keys.")
        google_api_key = input("Enter your GOOGLE_API_KEY: ").strip()
        tavily_api_key = input("Enter your TAVILY_API_KEY: ").strip()

        # Create a .env file from the example
        shutil.copy(".env.example", ".env")

        with open(".env", "w") as f:
            f.write(f"GOOGLE_API_KEY={google_api_key}\n")
            f.write(f"TAVILY_API_KEY={tavily_api_key}\n")

        print(".env file created successfully.")
    
    # Load the .env file
    load_dotenv()


async def run_agent_cli(user_input: str, user_id: str | None = None):
    """
    Asynchronously runs the agent graph with the given user input,
    handling human-in-the-loop interruptions.
    """
    inputs = {"user_input": user_input}
    thread_id = user_id or "cli_user_1"
    config = {"configurable": {"thread_id": thread_id}}

    print("\n--- Invoking Agent ---")
    print(f"Input: {user_input}\n")

    result = graph.invoke(inputs, config=config)

    while result.get('__interrupt__'):
        interrupt_info = result['__interrupt__'][0].value
        print("\n--- [!] Human Review Required ---")
        print(f"Task: {interrupt_info.get('task')}")
        print(f"Current Item List: {json.dumps(interrupt_info.get('current_list'), indent=2)}")

        user_action = ""
        while user_action not in ["accept", "edit"]:
            user_action = input("Do you want to 'accept' or 'edit' the list? > ").strip().lower()

        if user_action == "accept":
            resume_payload = {"action": "accept"}
            result = graph.invoke(Command(resume=resume_payload), config=config)

        elif user_action == "edit":
            print("Please provide the new list as a valid JSON array (e.g., [\"pasta\", \"sauce\", \"cheese\"])")
            while True:
                try:
                    new_list_str = input("Enter new list: > ")
                    new_list = json.loads(new_list_str)
                    if isinstance(new_list, list):
                        resume_payload = {"action": "edit", "editedList": new_list}
                        result = graph.invoke(Command(resume=resume_payload), config=config)
                        break
                    else:
                        print("Invalid input. The JSON must be an array (e.g., [\"item1\"]).")
                except json.JSONDecodeError:
                    print("Invalid JSON format. Please try again.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

    print("\n--- Agent Finished ---")
    print("Final State:")
    print(json.dumps(result, indent=2, default=str))


def main():
    """
    Sets up API keys, prompts for user input, and runs the agent.
    """
    setup_api_keys()
    
    parser = argparse.ArgumentParser(description="Run the Smart Cart Agent from the command line.")
    parser.add_argument("--user-id", type=str, help="An optional user ID to maintain state.", default=None)
    args = parser.parse_args()

    while True:
        user_input = input("Please enter your request (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break
        
        asyncio.run(run_agent_cli(user_input, args.user_id))

if __name__ == '__main__':
    main()