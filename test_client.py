import asyncio
from fastmcp import Client
from server import mcp  # importa tu instancia FastMCP

async def main():
    async with Client(mcp) as client:
        # Ver todos los tools registrados
        tools = await client.list_tools()
        print("Tools disponibles:", [t.name for t in tools])

        # Probar explain_instruction
        result = await client.call_tool("explain_instruction", {"instruction": "PUSH"})
        print("PUSH:", result)

        # Probar el simulador de stack
        result = await client.call_tool("run_stack_simulation", {
            "operations": ["PUSH int 10", "PUSH int 5", "ADD"]
        })
        print("Stack simulation:", result)

        # Probar validación de contrato
        code = """
parameter unit;
storage unit;
code {
  DROP;
  UNIT;
  NIL operation;
  PAIR
}"""
        result = await client.call_tool("validate_contract", {"michelson_code": code})
        print("Validación:", result)

        # Probar recursos
        resources = await client.list_resources()
        print("Resources:", [r.uri for r in resources])

asyncio.run(main())
