# test_rpc.py
import asyncio
import json
from fastmcp import Client
from server import mcp

async def main():
    async with Client(mcp) as client:
        def parse(r):
            return json.loads(r.content[0].text)

        # Network status
        r = parse(await client.call_tool("network_info", {"network": "ghostnet"}))
        print(f"Block level: {r['level']} | Protocol: {r['protocol'][:20]}...")

        # Account balance
        address = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
        r = parse(await client.call_tool("account_balance", {
            "address": address,
            "network": "ghostnet"
        }))
        print(f"Balance: {r['balance_tez']} tez")

        # Find a real contract first
        r = parse(await client.call_tool("search_deployed_contracts", {
            "keyword": "fa2",
            "network": "ghostnet",
            "limit": 3
        }))
        print(f"Contracts found: {json.dumps(r, indent=2)}")

        # Use first result if available
        if r.get("results") and len(r["results"]) > 0:
            contract = r["results"][0]["address"]
            print(f"\n→ Testing contract: {contract}")

            storage = parse(await client.call_tool("contract_storage", {
                "address": contract,
                "network": "ghostnet"
            }))
            print(f"Storage: {storage}")

            entrypoints = parse(await client.call_tool("contract_entrypoints", {
                "address": contract,
                "network": "ghostnet"
            }))
            print(f"Entrypoints: {entrypoints.get('names')}")

        # Latest block
        r = parse(await client.call_tool("block_info", {
            "block": "head",
            "network": "ghostnet"
        }))
        print(f"Latest block: {r['level']} at {r['timestamp']}")

asyncio.run(main())
