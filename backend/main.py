import argparse
import asyncio
import json
from agents.workflow import graph # Import the compiled graph

async def run_agent_cli(user_input: str, user_id: str | None = None):
    """
    Asynchronously runs the agent graph with the given user input and prints the steps.
    """
    # The input to the graph must match the InputInterpreterInputState schema
    inputs = {"user_input": user_input}
    
    print("\n--- Invoking Agent ---")
    print(f"Input: {user_input}\n")
    
    final_state = None
    try:
        # Using .astream() lets you see each step of the agent's process.
        async for s in graph.astream(inputs):
            # The key is the name of the node that just ran
            node_name = list(s.keys())[0]
            node_output = s[node_name]
            
            # Print the output of each step in a readable format
            print(f"--- Step: {node_name} ---")
            print(json.dumps(node_output, indent=2))
            print("\n")
            final_state = s

        print("--- Agent Finished ---")
        
        if final_state is None:
            print("Agent did not produce a final state.")
            return
        
    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(f"An error occurred during agent invocation: {e}")


def main():
    """
    Parses command-line arguments and runs the agent.
    """
    parser = argparse.ArgumentParser(description="Run the Smart Cart Agent from the command line.")
    
    # The main argument for the user's shopping request
    parser.add_argument("user_input", type=str, help="The user's request (e.g., 'I want to make pasta for $20').")
    
    # Optional argument for user ID
    parser.add_argument("--user-id", type=str, help="An optional user ID.", default=None)
    
    args = parser.parse_args()
    
    # Run the asynchronous agent function
    asyncio.run(run_agent_cli(args.user_input, args.user_id))


if __name__ == '__main__':
    main()
