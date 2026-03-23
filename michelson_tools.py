# Instrucciones básicas del stack de Michelson con su descripción
MICHELSON_INSTRUCTIONS = {
    "PUSH": "Empuja un valor al tope del stack. Ej: PUSH int 5",
    "ADD": "Suma los dos valores en el tope del stack (int/nat/mutez)",
    "SUB": "Resta el segundo del primero en el stack",
    "MUL": "Multiplica los dos valores del tope del stack",
    "IF": "Consume un bool del stack; ejecuta primer bloque si True, segundo si False",
    "PAIR": "Combina los dos valores del tope en un par (a, b)",
    "CAR": "Extrae el primer elemento de un par",
    "CDR": "Extrae el segundo elemento de un par",
    "NIL": "Empuja una lista vacía al stack",
    "CONS": "Agrega un elemento al inicio de una lista",
    "TRANSFER_TOKENS": "Emite una operación de transferencia de tokens",
    "FAILWITH": "Falla el contrato con un mensaje de error",
    "DROP": "Elimina el elemento del tope del stack",
    "DUP": "Duplica el elemento del tope del stack",
    "SWAP": "Intercambia los dos elementos del tope del stack",
    "UNIT": "Empuja el valor Unit al stack",
    "LAMBDA": "Define una función anónima (clausura)",
    "EXEC": "Ejecuta una lambda del stack",
    "MAP": "Aplica una función a cada elemento de una lista/map",
    "ITER": "Itera sobre una colección ejecutando un bloque",
    "SIZE": "Retorna el tamaño de una lista, set, map o string",
    "GET": "Obtiene un valor de un big_map/map por llave",
    "UPDATE": "Actualiza o elimina una entrada en un map/big_map/set",
    "SOME": "Envuelve un valor en option (Some x)",
    "NONE": "Empuja None al stack para un tipo option",
    "IF_NONE": "Ramifica según si el option es None o Some",
    "CONTRACT": "Resuelve una dirección a un contrato tipado",
    "AMOUNT": "Empuja la cantidad de tez enviada en la transacción actual",
    "BALANCE": "Empuja el balance actual del contrato",
    "SENDER": "Empuja la dirección del llamador directo",
    "SOURCE": "Empuja la dirección del origen de la transacción",
    "NOW": "Empuja el timestamp del bloque actual",
    "SELF": "Empuja una referencia al contrato actual",
    "CHAIN_ID": "Empuja el identificador de la cadena actual",
    "CONCAT": "Concatena strings o bytes",
    "PACK": "Serializa un valor a bytes",
    "UNPACK": "Deserializa bytes a un tipo dado",
    "HASH_KEY": "Hashea una llave pública a key_hash",
    "BLAKE2B": "Aplica hash BLAKE2B a bytes",
    "SHA256": "Aplica hash SHA256 a bytes",
    "CHECK_SIGNATURE": "Verifica una firma criptográfica",
    "INT": "Convierte nat a int",
    "NAT": "Convierte int a nat (puede fallar si negativo)",
    "ABS": "Valor absoluto de un int",
    "NEG": "Negación de un int/nat",
    "ISNAT": "Convierte int a option nat",
    "AND": "AND lógico o bitwise",
    "OR": "OR lógico o bitwise",
    "XOR": "XOR lógico o bitwise",
    "NOT": "NOT lógico o bitwise",
    "LSL": "Desplazamiento de bits a la izquierda",
    "LSR": "Desplazamiento de bits a la derecha",
    "COMPARE": "Compara dos valores; retorna -1, 0 o 1",
    "EQ": "Verifica igualdad (igual a 0 tras COMPARE)",
    "NEQ": "Verifica desigualdad",
    "LT": "Menor que",
    "GT": "Mayor que",
    "LE": "Menor o igual",
    "GE": "Mayor o igual",
    "CAST": "Cambia el tipo estático de un valor",
    "RENAME": "Renombra una anotación de tipo (sin efecto en runtime)",
    "DIG": "Sube el n-ésimo elemento del stack al tope",
    "DUG": "Baja el tope del stack a la posición n",
    "EMPTY_MAP": "Crea un mapa vacío con tipos de llave y valor dados",
    "EMPTY_BIG_MAP": "Crea un big_map vacío",
    "EMPTY_SET": "Crea un set vacío",
    "MEM": "Verifica si un elemento existe en set/map/big_map",
    "IMPLICIT_ACCOUNT": "Convierte un key_hash a una cuenta implícita",
    "SET_DELEGATE": "Emite una operación para cambiar el delegado",
    "CREATE_CONTRACT": "Emite una operación para originar un nuevo contrato",
    "VOTING_POWER": "Retorna el poder de voto de un key_hash en el ciclo actual",
    "TOTAL_VOTING_POWER": "Retorna el poder de voto total del ciclo actual",
    "SAPLING_EMPTY_STATE": "Crea un estado Sapling vacío (privacidad)",
    "SAPLING_VERIFY_UPDATE": "Verifica y aplica una transición de estado Sapling",
    "TICKET": "Crea un ticket con un valor y cantidad",
    "READ_TICKET": "Lee el contenido de un ticket",
    "SPLIT_TICKET": "Divide un ticket en dos con cantidades especificadas",
    "JOIN_TICKETS": "Une dos tickets compatibles en uno",
    "OPEN_CHEST": "Abre un chest (timelocked value) usando una llave y tiempo",
}

MICHELSON_TYPES = {
    "int": "Entero con signo de precisión arbitraria",
    "nat": "Entero sin signo (≥ 0)",
    "string": "Cadena de texto UTF-8",
    "bool": "Valor booleano: True o False",
    "bytes": "Secuencia de bytes crudos",
    "unit": "Tipo unitario, solo tiene el valor Unit",
    "address": "Dirección de cuenta Tezos (tz1... o KT1...)",
    "key": "Llave pública criptográfica",
    "key_hash": "Hash de llave pública (tz1...)",
    "signature": "Firma criptográfica",
    "timestamp": "Marca de tiempo Unix",
    "mutez": "Micro-tez: unidad mínima de tez (1 tez = 1,000,000 mutez)",
    "tez": "Moneda nativa de Tezos",
    "operation": "Operación de blockchain emitida por el contrato",
    "chain_id": "Identificador único de la cadena",
    "option": "Tipo opcional: Some(x) o None",
    "list": "Lista ordenada de elementos del mismo tipo",
    "set": "Conjunto sin duplicados de elementos comparables",
    "map": "Tabla clave-valor en memoria",
    "big_map": "Tabla clave-valor con lazy loading (más eficiente para datos grandes)",
    "pair": "Par ordenado de dos valores (a, b)",
    "or": "Tipo suma: Left(a) o Right(b)",
    "lambda": "Función de primera clase: tipo_entrada -> tipo_salida",
    "contract": "Referencia a un contrato con su tipo de parámetro",
    "ticket": "Token no fungible nativo de Tezos (Michelson 008+)",
    "sapling_state": "Estado de transacciones privadas Sapling",
    "sapling_transaction": "Transacción Sapling verificable",
    "chest": "Valor con timelock criptográfico",
    "chest_key": "Llave para abrir un chest tras el tiempo especificado",
    "bls12_381_g1": "Punto en la curva BLS12-381 G1 (criptografía avanzada)",
    "bls12_381_g2": "Punto en la curva BLS12-381 G2",
    "bls12_381_fr": "Escalar del campo Fr de BLS12-381",
    "tx_rollup_l2_address": "Dirección de capa 2 para rollups de transacciones",
}

def get_instruction_info(instruction: str) -> dict:
    """Retorna info de una instrucción Michelson."""
    instruction = instruction.upper().strip()
    if instruction in MICHELSON_INSTRUCTIONS:
        return {
            "instruction": instruction,
            "description": MICHELSON_INSTRUCTIONS[instruction],
            "found": True
        }
    # Búsqueda parcial
    matches = [k for k in MICHELSON_INSTRUCTIONS if instruction in k]
    return {
        "instruction": instruction,
        "found": False,
        "similar": matches,
        "message": f"Instrucción '{instruction}' no encontrada. Similares: {matches}"
    }

def get_type_info(type_name: str) -> dict:
    """Retorna info sobre un tipo de Michelson."""
    type_name = type_name.lower().strip()
    if type_name in MICHELSON_TYPES:
        return {"type": type_name, "description": MICHELSON_TYPES[type_name], "found": True}
    matches = [k for k in MICHELSON_TYPES if type_name in k]
    return {
        "type": type_name,
        "found": False,
        "similar": matches,
        "message": f"Tipo '{type_name}' no encontrado. Similares: {matches}"
    }

def simulate_stack(operations: list[str]) -> dict:
    """
    Simula el stack de Michelson para operaciones simples.
    Soporta: PUSH int/nat/string, ADD, SUB, MUL, DUP, DROP, SWAP, PAIR, CAR, CDR
    """
    stack = []
    log = []

    for op in operations:
        op = op.strip()
        parts = op.split()
        cmd = parts[0].upper()

        try:
            if cmd == "PUSH" and len(parts) >= 3:
                typ = parts[1].lower()
                val_str = " ".join(parts[2:])
                if typ in ("int", "nat"):
                    val = int(val_str)
                elif typ == "string":
                    val = val_str.strip('"')
                elif typ == "bool":
                    val = val_str == "True"
                else:
                    val = val_str
                stack.append((typ, val))
                log.append(f"PUSH → stack: {stack}")

            elif cmd == "ADD":
                if len(stack) < 2:
                    return {"error": "ADD requiere al menos 2 elementos en el stack"}
                b = stack.pop()
                a = stack.pop()
                result = a[1] + b[1]
                typ = "nat" if isinstance(result, int) and result >= 0 else "int"
                stack.append((typ, result))
                log.append(f"ADD {a[1]} + {b[1]} = {result} → stack: {stack}")

            elif cmd == "SUB":
                if len(stack) < 2:
                    return {"error": "SUB requiere al menos 2 elementos en el stack"}
                b = stack.pop()
                a = stack.pop()
                result = a[1] - b[1]
                stack.append(("int", result))
                log.append(f"SUB {a[1]} - {b[1]} = {result} → stack: {stack}")

            elif cmd == "MUL":
                if len(stack) < 2:
                    return {"error": "MUL requiere al menos 2 elementos en el stack"}
                b = stack.pop()
                a = stack.pop()
                result = a[1] * b[1]
                stack.append(("int", result))
                log.append(f"MUL {a[1]} * {b[1]} = {result} → stack: {stack}")

            elif cmd == "DUP":
                if not stack:
                    return {"error": "DUP requiere al menos 1 elemento"}
                stack.append(stack[-1])
                log.append(f"DUP → stack: {stack}")

            elif cmd == "DROP":
                if not stack:
                    return {"error": "DROP requiere al menos 1 elemento"}
                removed = stack.pop()
                log.append(f"DROP eliminó {removed} → stack: {stack}")

            elif cmd == "SWAP":
                if len(stack) < 2:
                    return {"error": "SWAP requiere al menos 2 elementos"}
                stack[-1], stack[-2] = stack[-2], stack[-1]
                log.append(f"SWAP → stack: {stack}")

            elif cmd == "PAIR":
                if len(stack) < 2:
                    return {"error": "PAIR requiere al menos 2 elementos"}
                b = stack.pop()
                a = stack.pop()
                stack.append(("pair", (a, b)))
                log.append(f"PAIR ({a}, {b}) → stack: {stack}")

            elif cmd == "CAR":
                if not stack or stack[-1][0] != "pair":
                    return {"error": "CAR requiere un par en el tope del stack"}
                pair = stack.pop()
                stack.append(pair[1][0])
                log.append(f"CAR → {pair[1][0]} → stack: {stack}")

            elif cmd == "CDR":
                if not stack or stack[-1][0] != "pair":
                    return {"error": "CDR requiere un par en el tope del stack"}
                pair = stack.pop()
                stack.append(pair[1][1])
                log.append(f"CDR → {pair[1][1]} → stack: {stack}")

            else:
                log.append(f"'{cmd}' no soportado en el simulador básico (instrucción conocida: {cmd in MICHELSON_INSTRUCTIONS})")

        except Exception as e:
            return {"error": str(e), "log": log, "stack_at_error": stack}

    return {
        "final_stack": stack,
        "steps": log,
        "stack_depth": len(stack)
    }

def validate_contract_structure(code: str) -> dict:
    """
    Valida la estructura básica de un contrato Michelson.
    Verifica que contenga las secciones obligatorias: parameter, storage, code.
    """
    issues = []
    suggestions = []
    
    code_lower = code.lower()
    
    has_parameter = "parameter" in code_lower
    has_storage = "storage" in code_lower
    has_code = "code" in code_lower
    
    if not has_parameter:
        issues.append("Falta la sección 'parameter'")
        suggestions.append("Agrega: parameter <tipo>;")
    if not has_storage:
        issues.append("Falta la sección 'storage'")
        suggestions.append("Agrega: storage <tipo>;")
    if not has_code:
        issues.append("Falta la sección 'code'")
        suggestions.append("Agrega: code { ... };")
    
    # Verificar balance de llaves
    open_braces = code.count("{")
    close_braces = code.count("}")
    if open_braces != close_braces:
        issues.append(f"Llaves desbalanceadas: {open_braces} '{{' vs {close_braces} '}}'")
    
    # Verificar balance de paréntesis
    open_parens = code.count("(")
    close_parens = code.count(")")
    if open_parens != close_parens:
        issues.append(f"Paréntesis desbalanceados: {open_parens} '(' vs {close_parens} ')'")
    
    is_valid = len(issues) == 0
    
    return {
        "valid": is_valid,
        "has_parameter": has_parameter,
        "has_storage": has_storage,
        "has_code": has_code,
        "issues": issues,
        "suggestions": suggestions,
        "summary": "Estructura válida" if is_valid else f"Se encontraron {len(issues)} problema(s)"
    }

def list_all_instructions() -> dict:
    """Lista todas las instrucciones Michelson disponibles."""
    return {
        "total": len(MICHELSON_INSTRUCTIONS),
        "instructions": list(MICHELSON_INSTRUCTIONS.keys()),
        "categories": {
            "stack": ["PUSH", "DROP", "DUP", "SWAP", "DIG", "DUG"],
            "arithmetic": ["ADD", "SUB", "MUL", "INT", "NAT", "ABS", "NEG", "ISNAT"],
            "comparison": ["COMPARE", "EQ", "NEQ", "LT", "GT", "LE", "GE"],
            "logical": ["AND", "OR", "XOR", "NOT", "LSL", "LSR"],
            "pairs": ["PAIR", "CAR", "CDR"],
            "control_flow": ["IF", "IF_NONE", "FAILWITH", "EXEC", "LAMBDA"],
            "collections": ["NIL", "CONS", "MAP", "ITER", "SIZE", "MEM",
                          "EMPTY_MAP", "EMPTY_BIG_MAP", "EMPTY_SET", "GET", "UPDATE"],
            "options": ["SOME", "NONE", "IF_NONE"],
            "blockchain": ["TRANSFER_TOKENS", "AMOUNT", "BALANCE", "SENDER", "SOURCE",
                          "NOW", "SELF", "CHAIN_ID", "CONTRACT", "IMPLICIT_ACCOUNT",
                          "SET_DELEGATE", "CREATE_CONTRACT", "VOTING_POWER", "TOTAL_VOTING_POWER"],
            "crypto": ["HASH_KEY", "BLAKE2B", "SHA256", "CHECK_SIGNATURE",
                      "PACK", "UNPACK", "CONCAT"],
            "tickets": ["TICKET", "READ_TICKET", "SPLIT_TICKET", "JOIN_TICKETS"],
            "sapling": ["SAPLING_EMPTY_STATE", "SAPLING_VERIFY_UPDATE"],
            "timelocks": ["OPEN_CHEST"],
            "bls12_381": ["bls12_381_g1", "bls12_381_g2", "bls12_381_fr"],
            "type_ops": ["CAST", "RENAME", "UNIT"],
        }
    }

def get_contract_template(template_name: str) -> dict:
    """Retorna plantillas de contratos Michelson comunes."""
    templates = {
        "counter": {
            "name": "Counter Contract",
            "description": "Contrato simple que incrementa/decrementa un contador",
            "code": """parameter (or (unit %increment) (unit %decrement));
storage int;
code {
  UNPAIR;
  IF_LEFT
    { DROP; PUSH int 1; ADD }
    { DROP; PUSH int 1; SWAP; SUB };
  NIL operation;
  PAIR
}"""
        },
        "hello_world": {
            "name": "Hello World",
            "description": "El contrato más simple: acepta unit, devuelve unit",
            "code": """parameter unit;
storage unit;
code {
  DROP;
  UNIT;
  NIL operation;
  PAIR
}"""
        },
        "token_transfer": {
            "name": "Simple Token Transfer",
            "description": "Transfiere tez a una dirección especificada",
            "code": """parameter (pair address mutez);
storage unit;
code {
  CAR;
  UNPAIR;
  CONTRACT unit;
  IF_NONE { FAILWITH } {};
  SWAP;
  UNIT;
  TRANSFER_TOKENS;
  NIL operation;
  SWAP;
  CONS;
  UNIT;
  PAIR
}"""
        },
        "multisig": {
            "name": "Basic Multisig",
            "description": "Contrato multifirma básico con contador de nonce",
            "code": """parameter (pair
  (pair nat (lambda unit (list operation)))
  (list signature));
storage (pair nat (set key_hash));
code {
  UNPAIR;
  # Verificar nonce y firmas
  # ... (implementación completa requiere más lógica)
  FAILWITH
}"""
        },
        "escrow": {
            "name": "Simple Escrow",
            "description": "Contrato de depósito en garantía entre dos partes",
            "code": """parameter (or
  (unit %release)
  (unit %refund));
storage (pair
  (pair address %buyer address %seller)
  mutez %amount);
code {
  UNPAIR;
  IF_LEFT
    {
      DROP;
      CDR; # obtener amount
      # ... enviar al vendedor
      FAILWITH  # placeholder
    }
    {
      DROP;
      # ... reembolsar al comprador
      FAILWITH  # placeholder
    }
}"""
        }
    }
    
    template_name = template_name.lower()
    if template_name in templates:
        return {"found": True, **templates[template_name]}
    
    return {
        "found": False,
        "available_templates": list(templates.keys()),
        "message": f"Plantilla '{template_name}' no encontrada."
    }
