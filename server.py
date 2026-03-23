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

mcp = FastMCP("Michelson Language Server")

# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────

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
    """
    Genera un prompt para crear un contrato Michelson desde una descripción.
    
    Args:
        description: Descripción en lenguaje natural del contrato deseado
    """
    return f"""Eres un experto desarrollador de contratos inteligentes en Michelson para Tezos.

Crea un contrato Michelson que implemente lo siguiente:
{description}

Recuerda:
- La estructura obligatoria: parameter, storage, code
- El contrato comienza con [ (parameter, storage) : [] ]
- Debe terminar con [ (list operation, storage) : [] ]
- Usa anotaciones %nombre para los entrypoints
- Incluye comentarios con # explicando cada sección importante

Proporciona el código completo y funcional."""


if __name__ == "__main__":
    mcp.run()
