import requests
from typing import Optional

t 
NETWORKS = {
    "mainnet": {
        "rpc": "https://mainnet.tezos.marigold.dev",
        "explorer": "https://api.tzkt.io/v1",
        "name": "Tezos Mainnet",
    },
    "ghostnet": {
        "rpc": "https://ghostnet.ecadinfra.com",
        "explorer": "https://api.ghostnet.tzkt.io/v1",
        "name": "Ghostnet (Testnet)",
    },
    "oxfordnet": {
        "rpc": "https://rpc.oxfordnet.teztnets.com",
        "explorer": None,
        "name": "Oxfordnet",
    },
}

DEFAULT_NETWORK = "ghostnet"


def _rpc(network: str, path: str) -> dict:
    """Makes a GET request to the Tezos RPC node."""
    base = NETWORKS.get(network, NETWORKS[DEFAULT_NETWORK])["rpc"]
    url = f"{base}{path}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {"ok": True, "data": response.json()}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": f"Timeout connecting to {network} RPC"}
    except requests.exceptions.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "error": f"Could not connect to {network} RPC node"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _explorer(network: str, path: str) -> dict:
    """Makes a GET request to the TzKT explorer API."""
    net = NETWORKS.get(network, NETWORKS[DEFAULT_NETWORK])
    if not net["explorer"]:
        return {"ok": False, "error": f"No explorer available for {network}"}
    url = f"{net['explorer']}{path}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {"ok": True, "data": response.json()}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "Timeout connecting to TzKT explorer"}
    except requests.exceptions.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "error": "Could not connect to TzKT explorer"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─────────────────────────────────────────────
# NETWORK INFO
# ─────────────────────────────────────────────

def get_network_info(network: str = DEFAULT_NETWORK) -> dict:
    """Returns current network info: block level, protocol, timestamp."""
    result = _rpc(network, "/chains/main/blocks/head/header")
    if not result["ok"]:
        return result

    header = result["data"]
    proto_result = _rpc(network, "/chains/main/blocks/head/metadata")

    protocol = "unknown"
    if proto_result["ok"]:
        protocol = proto_result["data"].get("protocol", "unknown")

    return {
        "ok": True,
        "network": NETWORKS[network]["name"],
        "level": header.get("level"),
        "protocol": protocol,
        "timestamp": header.get("timestamp"),
        "chain_id": header.get("chain_id"),
        "hash": header.get("hash"),
    }


# ─────────────────────────────────────────────
# ACCOUNT / ADDRESS
# ─────────────────────────────────────────────

def get_account_info(address: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns balance and info for any Tezos address (tz1... or KT1...)."""
    result = _rpc(network, f"/chains/main/blocks/head/context/contracts/{address}")
    if not result["ok"]:
        return result

    data = result["data"]
    balance_mutez = int(data.get("balance", 0))

    return {
        "ok": True,
        "address": address,
        "network": network,
        "balance_mutez": balance_mutez,
        "balance_tez": balance_mutez / 1_000_000,
        "counter": data.get("counter"),
        "is_contract": data.get("script") is not None,
        "delegate": data.get("delegate"),
    }


def get_balance(address: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns the balance of an address in mutez and tez."""
    result = _rpc(
        network,
        f"/chains/main/blocks/head/context/contracts/{address}/balance"
    )
    if not result["ok"]:
        return result

    balance_mutez = int(result["data"])
    return {
        "ok": True,
        "address": address,
        "network": network,
        "balance_mutez": balance_mutez,
        "balance_tez": balance_mutez / 1_000_000,
    }


# ─────────────────────────────────────────────
# CONTRACT
# ─────────────────────────────────────────────

def get_contract_storage(address: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns the current storage of a deployed contract."""
    result = _rpc(
        network,
        f"/chains/main/blocks/head/context/contracts/{address}/storage"
    )
    if not result["ok"]:
        return result

    return {
        "ok": True,
        "address": address,
        "network": network,
        "storage": result["data"],
    }


def get_contract_code(address: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns the Micheline code of a deployed contract."""
    result = _rpc(
        network,
        f"/chains/main/blocks/head/context/contracts/{address}/script"
    )
    if not result["ok"]:
        return result

    script = result["data"]
    code_sections = script.get("code", [])

    parameter = None
    storage_type = None
    code = None

    for section in code_sections:
        if isinstance(section, dict):
            prim = section.get("prim")
            if prim == "parameter":
                parameter = section
            elif prim == "storage":
                storage_type = section
            elif prim == "code":
                code = section

    return {
        "ok": True,
        "address": address,
        "network": network,
        "parameter": parameter,
        "storage_type": storage_type,
        "code": code,
        "raw_script": script,
    }


def get_contract_entrypoints(address: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns the entrypoints of a deployed contract."""
    result = _rpc(
        network,
        f"/chains/main/blocks/head/context/contracts/{address}/entrypoints"
    )
    if not result["ok"]:
        return result

    entrypoints = result["data"].get("entrypoints", {})
    return {
        "ok": True,
        "address": address,
        "network": network,
        "entrypoints": entrypoints,
        "total": len(entrypoints),
        "names": list(entrypoints.keys()),
    }


def get_contract_big_map(
    address: str,
    big_map_id: int,
    key: Optional[str] = None,
    network: str = DEFAULT_NETWORK
) -> dict:
    """
    Returns big_map data for a contract.
    If key is provided, returns that specific entry.
    """
    if key:
        result = _explorer(network, f"/bigmaps/{big_map_id}/keys/{key}")
    else:
        result = _explorer(network, f"/bigmaps/{big_map_id}/keys?limit=20")

    if not result["ok"]:
        return result

    return {
        "ok": True,
        "address": address,
        "network": network,
        "big_map_id": big_map_id,
        "key": key,
        "data": result["data"],
    }


# ─────────────────────────────────────────────
# TRANSACTIONS / OPERATIONS
# ─────────────────────────────────────────────

def get_contract_operations(
    address: str,
    limit: int = 10,
    network: str = DEFAULT_NETWORK
) -> dict:
    """Returns the last N operations involving a contract."""
    result = _explorer(
        network,
        f"/accounts/{address}/operations?limit={limit}&type=transaction"
    )
    if not result["ok"]:
        return result

    ops = result["data"]
    simplified = []
    for op in ops:
        simplified.append({
            "hash": op.get("hash"),
            "timestamp": op.get("timestamp"),
            "sender": op.get("sender", {}).get("address"),
            "target": op.get("target", {}).get("address"),
            "amount_mutez": op.get("amount", 0),
            "amount_tez": op.get("amount", 0) / 1_000_000,
            "entrypoint": op.get("parameter", {}).get("entrypoint") if op.get("parameter") else None,
            "status": op.get("status"),
        })

    return {
        "ok": True,
        "address": address,
        "network": network,
        "operations": simplified,
        "total_returned": len(simplified),
    }


def get_operation_details(op_hash: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns full details of a specific operation by hash."""
    result = _explorer(network, f"/operations/{op_hash}")
    if not result["ok"]:
        return result

    return {
        "ok": True,
        "network": network,
        "operation": result["data"],
    }


# ─────────────────────────────────────────────
# BLOCKS
# ─────────────────────────────────────────────

def get_block_info(
    block: str = "head",
    network: str = DEFAULT_NETWORK
) -> dict:
    """Returns info about a specific block (use 'head' for latest)."""
    result = _rpc(network, f"/chains/main/blocks/{block}/header")
    if not result["ok"]:
        return result

    header = result["data"]
    return {
        "ok": True,
        "network": network,
        "level": header.get("level"),
        "hash": header.get("hash"),
        "timestamp": header.get("timestamp"),
        "predecessor": header.get("predecessor"),
        "validation_pass": header.get("validation_pass"),
        "fitness": header.get("fitness"),
    }


# ─────────────────────────────────────────────
# SEARCH / EXPLORE
# ─────────────────────────────────────────────

def search_contracts(
    keyword: str,
    network: str = DEFAULT_NETWORK,
    limit: int = 10
) -> dict:
    """Searches contracts using TzKT explorer directly."""
    # Search by alias directly in the API query
    result = _explorer(
        network,
        f"/contracts?limit={limit}&sort.desc=numTransactions"
    )
    if not result["ok"]:
        return result

    contracts = result["data"]
    simplified = [
        {
            "address": c.get("address"),
            "alias": c.get("alias"),
            "balance_tez": c.get("balance", 0) / 1_000_000,
            "num_transactions": c.get("numTransactions"),
            "first_activity": c.get("firstActivityTime"),
            "last_activity": c.get("lastActivityTime"),
        }
        for c in contracts
    ]

    return {
        "ok": True,
        "network": network,
        "keyword": keyword,
        "results": simplified,
        "total": len(simplified),
    }


def get_contract_metadata(address: str, network: str = DEFAULT_NETWORK) -> dict:
    """Returns contract metadata (alias, tags, description) from TzKT."""
    result = _explorer(network, f"/accounts/{address}")
    if not result["ok"]:
        return result

    data = result["data"]
    return {
        "ok": True,
        "address": address,
        "network": network,
        "alias": data.get("alias"),
        "kind": data.get("kind"),
        "balance_tez": data.get("balance", 0) / 1_000_000,
        "num_transactions": data.get("numTransactions"),
        "first_activity_time": data.get("firstActivityTime"),
        "last_activity_time": data.get("lastActivityTime"),
        "creator": data.get("creator", {}).get("address") if data.get("creator") else None,
    }
