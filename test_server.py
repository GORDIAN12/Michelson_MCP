import pytest
import json
from fastmcp import Client
from server import mcp

@pytest.fixture
async def client():
    async with Client(mcp) as c:
        yield c

def parse_result(result):
    return json.loads(result.content[0].text)  # ← único cambio

@pytest.mark.asyncio
async def test_tools_registered(client):
    tools = await client.list_tools()
    names = [t.name for t in tools]
    assert "explain_instruction" in names
    assert "run_stack_simulation" in names
    assert "validate_contract" in names

@pytest.mark.asyncio
async def test_explain_push(client):
    data = parse_result(await client.call_tool("explain_instruction", {"instruction": "PUSH"}))
    assert data["found"] == True

@pytest.mark.asyncio
async def test_stack_add(client):
    data = parse_result(await client.call_tool("run_stack_simulation", {
        "operations": ["PUSH int 3", "PUSH int 7", "ADD"]
    }))
    assert data["final_stack"][0][1] == 10

@pytest.mark.asyncio
async def test_validate_valid_contract(client):
    data = parse_result(await client.call_tool("validate_contract", {
        "michelson_code": "parameter unit; storage unit; code { DROP; UNIT; NIL operation; PAIR }"
    }))
    assert data["valid"] == True

@pytest.mark.asyncio
async def test_validate_invalid_contract(client):
    data = parse_result(await client.call_tool("validate_contract", {
        "michelson_code": "code { DROP }"
    }))
    assert data["valid"] == False
