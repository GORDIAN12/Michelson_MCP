## What will we build?

An MCP server exposes **tools**, **resources**, and **prompts** to AI agents (such as Claude or Cursor) in a standardized way.

In this case, the server will give any LLM capabilities to work with Michelson:

- Parse contracts  
- Validate types  
- Explain stack instructions  

# create virtual enviroment
python -m venv ./venv
source ./venv/bin/activate

pip install mcp fastmcp pytezos

# Run the server directly
python server.py

# Test with MCP Inspector (oficial debugging tool)