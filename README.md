## What will we build?

An MCP server exposes **tools**, **resources**, and **prompts** to AI agents (such as Claude or Cursor) in a standardized way.

In this case, the server will give any LLM capabilities to work with Michelson:

- Parse contracts  
- Validate types  
- Explain stack instructions  

# create virtual enviroment
```python -m venv ./venv
source ./venv/bin/activate


pip install mcp fastmcp pytezos

# Run the server directly
python server.py

# Test with MCP Inspector (oficial debugging tool)
npx @modelcontextprotocol/inspector python server.py
```

|Tool               |Function                                   |
|-------------------|-------------------------------------------|
|explain_instruction|Explain any instruction Michelson          |
|explain_type       |Describe data types (int,nat,big_map,etc)  |
|run_stack_simulation| simulate stack execution step by step    |
|validate_contract   | valdate the structure basic of a contract|  	
|list_instructions   | List all instructions by category        |
|get_template        | Return ready-to-use contract templates   | 
|search_instructions |search instructions by keywords           |
|create contract from description |	Prompt create_contract_from_scratch|
|fix a specific bug	|Tool fix_contract + Prompt fix_michelson_bug|
|improve existing code	|Tool improve_contract + Prompt improve_michelson_code|
|deep bug/warnings analysis |	Tool analyze_contract|
|security audit|	Prompt review_contract_security |


cursor

```
{
  "mcpServers": {
    "michelson": {
      "command": "/home/david/Documentos/projects/DEV_MCP_ASSISTANT/venv/bin/python",
      "args": ["/home/david/Documentos/projects/DEV_MCP_ASSISTANT/server.py"]
    }
  }
}
```

### proof with michelson Tezos with docker

```
docker run -it --rm --entrypoint /bin/sh -v $PWD:/work tezos/tezos:latest
```
## Testing with language michelson

### Product
```
octez-client --mode mockup --base-dir /tmp/mockup \
  run script /work/product.tz \
  on storage 0 \
  and input '(Pair 3 4)'
```

### Substract

``` 
octez-client --mode mockup --base-dir /tmp/mockup run script /work/substract.tz on storage 10 and input '5'
```

### Addition

```
octez-client --mode mockup --base-dir /tmp/mockup run script /work/counter.tz on storage 10 and input 'Left 5'
```

<!--
Source - https://stackoverflow.com/q/41604263
Posted by zjffdu, modified by community. See post 'Timeline' for change history
Retrieved 2026-03-24, License - CC BY-SA 4.0
-->

![image](screens/prod.png)
