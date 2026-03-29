from mcp.server.fastmcp import FastMCP
from michelson_tools import (
    get_instruction_info,
    get_type_info,
    simulate_stack,
    validate_contract_structure,
    list_all_instructions,
    get_contract_template,
    MICHELSON_INSTRUCTIONS,
    MICHELSON_TYPES
)

from tezos_rpc import (
    get_network_info,
    get_account_info,
    get_balance,
    get_contract_storage,
    get_contract_code,
    get_contract_entrypoints,
    get_contract_big_map,
    get_contract_operations,
    get_operation_details,
    get_block_info,
    search_contracts,
    get_contract_metadata,
)


mcp = FastMCP("Michelson Language Server")

# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────

@mcp.tool()
def network_info(network: str = "ghostnet") -> dict:
    """
    Returns current Tezos network status: block level, protocol and timestamp.

    Args:
        network: Network to query. Options: mainnet, ghostnet (default: ghostnet)
    """
    return get_network_info(network)


@mcp.tool()
def block_info(block: str = "head", network: str = "ghostnet") -> dict:
    """
    Returns information about a specific block.

    Args:
        block: Block level or hash, use 'head' for the latest (default: head)
        network: Network to query (default: ghostnet)
    """
    return get_block_info(block, network)


# ─────────────────────────────────────────────
# ACCOUNT TOOLS
# ─────────────────────────────────────────────

@mcp.tool()
def account_info(address: str, network: str = "ghostnet") -> dict:
    """
    Returns balance and account info for any Tezos address (tz1... or KT1...).

    Args:
        address: Tezos address (tz1... implicit or KT1... contract)
        network: Network to query (default: ghostnet)
    """
    return get_account_info(address, network)


@mcp.tool()
def account_balance(address: str, network: str = "ghostnet") -> dict:
    """
    Returns the balance of a Tezos address in mutez and tez.

    Args:
        address: Tezos address
        network: Network to query (default: ghostnet)
    """
    return get_balance(address, network)


# ─────────────────────────────────────────────
# CONTRACT TOOLS
# ─────────────────────────────────────────────

@mcp.tool()
def contract_storage(address: str, network: str = "ghostnet") -> dict:
    """
    Returns the current storage of a deployed Tezos smart contract.

    Args:
        address: Contract address (KT1...)
        network: Network to query (default: ghostnet)
    """
    return get_contract_storage(address, network)


@mcp.tool()
def contract_code(address: str, network: str = "ghostnet") -> dict:
    """
    Returns the Micheline code of a deployed contract (parameter, storage type, code).

    Args:
        address: Contract address (KT1...)
        network: Network to query (default: ghostnet)
    """
    return get_contract_code(address, network)


@mcp.tool()
def contract_entrypoints(address: str, network: str = "ghostnet") -> dict:
    """
    Returns all entrypoints of a deployed contract with their types.

    Args:
        address: Contract address (KT1...)
        network: Network to query (default: ghostnet)
    """
    return get_contract_entrypoints(address, network)


@mcp.tool()
def contract_big_map(
    address: str,
    big_map_id: int,
    key: str = "",
    network: str = "ghostnet"
) -> dict:
    """
    Returns big_map data for a contract.

    Args:
        address: Contract address (KT1...)
        big_map_id: Numeric ID of the big_map
        key: Specific key to look up (optional, returns first 20 entries if empty)
        network: Network to query (default: ghostnet)
    """
    return get_contract_big_map(address, big_map_id, key or None, network)


@mcp.tool()
def contract_operations(
    address: str,
    limit: int = 10,
    network: str = "ghostnet"
) -> dict:
    """
    Returns the last N transactions involving a contract.

    Args:
        address: Contract address (KT1...)
        limit: Number of operations to return (default: 10, max: 50)
        network: Network to query (default: ghostnet)
    """
    return get_contract_operations(address, min(limit, 50), network)


@mcp.tool()
def contract_metadata(address: str, network: str = "ghostnet") -> dict:
    """
    Returns contract metadata: alias, creator, activity stats from TzKT explorer.

    Args:
        address: Contract address (KT1...)
        network: Network to query (default: ghostnet)
    """
    return get_contract_metadata(address, network)


# ─────────────────────────────────────────────
# OPERATION TOOLS
# ─────────────────────────────────────────────

@mcp.tool()
def operation_details(op_hash: str, network: str = "ghostnet") -> dict:
    """
    Returns full details of a specific operation by its hash.

    Args:
        op_hash: Operation hash (o...)
        network: Network to query (default: ghostnet)
    """
    return get_operation_details(op_hash, network)


# ─────────────────────────────────────────────
# SEARCH TOOLS
# ─────────────────────────────────────────────

@mcp.tool()
def search_deployed_contracts(
    keyword: str,
    network: str = "ghostnet",
    limit: int = 10
) -> dict:
    """
    Searches deployed contracts by alias or address keyword.

    Args:
        keyword: Search term (contract alias or partial address)
        network: Network to query (default: ghostnet)
        limit: Max number of results (default: 10)
    """
    return search_contracts(keyword, network, limit)


@mcp.tool()
def explain_instruction(instruction: str) -> dict:
    """
    Explica una instrucción Michelson: qué hace, cómo afecta el stack.
    
    Args:
        instruction: Nombre de la instrucción (ej: PUSH, ADD, PAIR, IF_LEFT)
    """
    return get_instruction_info(instruction)


@mcp.tool()
def explain_type(type_name: str) -> dict:
    """
    Explica un tipo de dato Michelson.
    
    Args:
        type_name: Nombre del tipo (ej: int, nat, address, big_map, ticket)
    """
    return get_type_info(type_name)


@mcp.tool()
def run_stack_simulation(operations: list[str]) -> dict:
    """
    Simula la ejecución del stack de Michelson paso a paso.
    Soporta: PUSH int/nat/string/bool, ADD, SUB, MUL, DUP, DROP, SWAP, PAIR, CAR, CDR.
    
    Args:
        operations: Lista de instrucciones Michelson a simular.
                    Ejemplo: ["PUSH int 5", "PUSH int 3", "ADD"]
    """
    return simulate_stack(operations)


@mcp.tool()
def validate_contract(michelson_code: str) -> dict:
    """
    Valida la estructura básica de un contrato Michelson.
    Verifica secciones obligatorias (parameter, storage, code) y balance de llaves.
    
    Args:
        michelson_code: Código Michelson completo del contrato
    """
    return validate_contract_structure(michelson_code)


@mcp.tool()
def list_instructions() -> dict:
    """
    Lista todas las instrucciones Michelson disponibles, organizadas por categoría.
    """
    return list_all_instructions()


@mcp.tool()
def get_template(template_name: str) -> dict:
    """
    Obtiene una plantilla de contrato Michelson lista para usar.
    
    Args:
        template_name: Nombre de la plantilla. Opciones: counter, hello_world,
                       token_transfer, multisig, escrow
    """
    return get_contract_template(template_name)


@mcp.tool()
def search_instructions(keyword: str) -> dict:
    """
    Busca instrucciones o tipos de Michelson por palabra clave.
    
    Args:
        keyword: Término de búsqueda (ej: 'transfer', 'hash', 'list')
    """
    keyword = keyword.upper()
    matched_instructions = {
        k: v for k, v in MICHELSON_INSTRUCTIONS.items() if keyword in k or keyword in v.upper()
    }
    matched_types = {
        k: v for k, v in MICHELSON_TYPES.items() if keyword.lower() in k or keyword.lower() in v.lower()
    }
    return {
        "keyword": keyword,
        "instructions_found": matched_instructions,
        "types_found": matched_types,
        "total_matches": len(matched_instructions) + len(matched_types)
    }


# ─────────────────────────────────────────────
# RESOURCES
# ─────────────────────────────────────────────
@mcp.resource("michelson://instructions")
def michelson_instructions_resource() -> str:
    """Recurso con todas las instrucciones Michelson y sus descripciones."""
    lines = ["# Instrucciones Michelson\n"]
    for instr, desc in MICHELSON_INSTRUCTIONS.items():
        lines.append(f"## {instr}\n{desc}\n")
    return "\n".join(lines)


@mcp.resource("michelson://types")
def michelson_types_resource() -> str:
    """Recurso con todos los tipos de dato Michelson."""
    lines = ["# Tipos de Dato en Michelson\n"]
    for typ, desc in MICHELSON_TYPES.items():
        lines.append(f"## {typ}\n{desc}\n")
    return "\n".join(lines)

@mcp.resource("michelson://rules")
def michelson_rules() -> str:
    """Critical Michelson syntax rules for modern Tezos protocols (Mumbai+)."""
    return """# Critical Michelson Rules — Modern Tezos Protocols

## Rule 1: SUB is DEPRECATED
- NEVER use `SUB` to subtract integers (int/nat).
- SUB was removed in modern Tezos protocols (Mumbai onwards).
- Always use: SWAP ; NEG ; ADD
  Example: to compute (storage - param) with stack [ param : storage ]:
    SWAP   -> [ storage : param ]
    NEG    -> [ storage : -param ]
    ADD    -> [ storage - param ]

## Rule 2: Stack balance in IF_LEFT / IF / IF_NONE branches
- ALL branches of a conditional MUST end with exactly the same stack.
- Count stack elements at entry and exit of every branch.
- Reset branch example receiving [ unit : int ] and leaving [ int ]:
    DROP        -> removes unit -> [ int ]
    DROP        -> removes int  -> []
    PUSH int 0  -> [ int ]      ← final stack is [ int ] in all branches

## Rule 3: Braces and semicolons syntax
- The `code { ... }` block does NOT have a semicolon at the end.
- IF_LEFT branches do NOT have a semicolon between them:
    CORRECT: IF_LEFT { instruction_a } { instruction_b }
    WRONG:   IF_LEFT { instruction_a } ; { instruction_b }
- Instructions inside a block are separated by ` ; `
- The LAST instruction in a block does NOT have ` ; ` before `}`

## Rule 4: Mandatory contract structure
- Every contract MUST have exactly:
    parameter <type> ;
    storage <type> ;
    code { <instructions> }
- Initial stack is always: [ (parameter, storage) ]
- Final stack MUST always be: [ (list operation, new_storage) ]
- Standard closing pattern:
    NIL operation ;
    PAIR

## Rule 5: UNPAIR instead of manual CAR/CDR
- Use UNPAIR to split the initial (parameter, storage) pair:
    CORRECT: UNPAIR  -> [ parameter : storage ]
    VERBOSE: CAR / CDR (still work but less idiomatic)

## Rule 6: Valid arithmetic in modern protocols
- int + int  -> ADD
- int - int  -> SWAP ; NEG ; ADD  (do NOT use SUB)
- int * int  -> MUL
- abs(int)   -> ABS  (returns nat)
- neg(int)   -> NEG
- nat -> int -> INT
- int -> nat -> ISNAT  (returns option nat)

## Correct Contract Example (Counter: add, subtract, reset)

parameter (or int (or int unit)) ;
storage int ;
code { UNPAIR ;
       IF_LEFT { ADD }
               { IF_LEFT { SWAP ; NEG ; ADD }
                         { DROP ; DROP ; PUSH int 0 } } ;
       NIL operation ;
       PAIR }

Entrypoints:
- Left <n>           -> adds n to storage
- Right (Left <n>)   -> subtracts n from storage
- Right (Right Unit) -> resets storage to 0
"""



@mcp.resource("michelson://cheatsheet")
def michelson_cheatsheet() -> str:
    """Cheat sheet rápida de Michelson para contratos Tezos."""
    return """# Michelson Quick Reference

## Estructura de un Contrato

## Estructura de un Contrato
parameter <tipo>;
storage <tipo>;
code { <instrucciones> }

## Stack Tips
- El stack siempre comienza con: [ (parameter, storage) : [] ]
- El contrato DEBE terminar con: [ (list operation, storage) : [] ]
- Usa UNPAIR para separar (parameter, storage)
- Usa PAIR al final para recombinar resultado

## Tipos Más Usados
- int / nat / mutez  → números
- string / bytes     → texto y datos
- address            → cuentas Tezos
- bool               → condicionales
- option             → valores opcionales
- pair               → estructuras
- or                 → tipos suma (entrypoints)
- list / set / map / big_map  → colecciones

## Patrón Entrypoints

parameter (or (tipo1%entrypoint1) (tipo2%entrypoint2));
code {
UNPAIR;
IF_LEFT
{ # manejar entrypoint1
}
{ # manejar entrypoint2
};
...
}

"""

# PROMPTS

@mcp.prompt()
def explain_michelson_code(code: str) -> str:
    """
    Genera un prompt para que el LLM explique código Michelson.
    
    Args:
        code: Código Michelson a explicar
    """
    return f"""Eres un experto en el lenguaje Michelson de Tezos.
    
Analiza el siguiente contrato Michelson y explica:
1. Qué hace el contrato en términos de negocio
2. Cómo funciona el stack paso a paso
3. Los tipos de parámetros y storage que usa
4. Posibles vulnerabilidades o mejoras

Código Michelson:

{code}


Proporciona una explicación clara y detallada."""


@mcp.prompt()
def generate_michelson_contract(description: str) -> str:
    return f"""Eres un experto desarrollador de contratos inteligentes en Michelson para Tezos.

Crea un contrato Michelson que implemente lo siguiente:
{description}


PROHIBICIONES ABSOLUTAS — NO NEGOCIABLES

1. NUNCA escribas la instrucción `SUB`. Está ELIMINADA del protocolo.
   - Para restar SIEMPRE escribe: `SWAP ; NEG ; ADD`
   - No hay excepciones. Aunque parezca correcto, SUB causará error fatal.

2. NUNCA termines el bloque `code {{ ... }}` con punto y coma.

3. NUNCA pongas punto y coma entre ramas de IF_LEFT:
IF_LEFT {{ A }} ; {{ B }}
IF_LEFT {{ A }} {{ B }}


REGLAS OBLIGATORIAS

- Estructura: parameter <tipo> ; / storage <tipo> ; / code {{ ... }}
- Stack inicial: [ (parameter, storage) ] — usa UNPAIR para separar
- Stack final SIEMPRE: [ (list operation, storage) ] — cierra con NIL operation ; PAIR
- En ramas IF_LEFT: TODAS deben terminar con el mismo stack
  - Si una rama recibe [ unit : int ], necesita DROP ; DROP ; PUSH int <val> para dejar [ int ]
  - Si una rama recibe [ int : int ], ADD o SWAP ; NEG ; ADD deja [ int ] ✓


PATRÓN DE RESTA — COPIA EXACTAMENTE

Para restar el parámetro del storage con stack [ param : storage ]:
  SWAP       → [ storage : param ]
  NEG        → [ storage : -param ]
  ADD        → [ (storage - param) ]   ← resultado correcto


EJEMPLO VALIDADO Y FUNCIONAL

parameter (or int (or int unit)) ;
storage int ;
code {{ UNPAIR ;
       IF_LEFT {{ ADD }}
               {{ IF_LEFT {{ SWAP ; NEG ; ADD }}
                          {{ DROP ; DROP ; PUSH int 0 }} }} ;
       NIL operation ;
       PAIR }}

Este contrato fue verificado con octez-client. Úsalo como referencia exacta.

Proporciona ÚNICAMENTE el código completo. Antes de responder, verifica mentalmente
que no aparece la palabra SUB en ningún lugar del código generado."""


@mcp.prompt()
def fix_michelson_bug(code: str, error: str) -> str:
    """
    Prompt to guide the LLM to fix a bug in a Michelson contract.

    Args:
        code: Michelson code containing the bug
        error: Error description or failure message
    """
    return f"""You are an expert in Michelson and Tezos smart contracts.

The following contract has a bug or incorrect behavior:

```michelson
{code}
Reported error:
{error}

CRITICAL RULES to apply in the fix:

NEVER use SUB — replace with SWAP ; NEG ; ADD

ALL branches of IF_LEFT / IF / IF_NONE must end with the same stack shape

No semicolon between IF_LEFT branches: IF_LEFT {{ ... }} {{ ... }}

Final stack MUST be: [ (list operation, storage) ]

Please:

Identify the root cause of the problem

Explain why it occurs in terms of the stack

Provide the complete corrected code

Explain what changed and why it now works"""

## 4. Agrega un tool para validar estas reglas específicamente
@mcp.tool()
def lint_contract(michelson_code: str) -> dict:
    """
    Checks a Michelson contract against modern protocol rules:
    deprecated instructions, stack balance, syntax issues.

    Args:
        michelson_code: Full Michelson contract code
    """
    from michelson_tools import lint_modern_rules
    return lint_modern_rules(michelson_code)


if __name__ == "__main__":
    mcp.run()
