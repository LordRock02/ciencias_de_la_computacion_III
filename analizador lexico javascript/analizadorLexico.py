import re

# Listas para los diferentes tipos de tokens en Javascript
operators = [
    '+', '-', '*', '=', '/', '%', '++', '--', '==', '!=', '>', '<', '>=', '<=',
    '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '>>>', '+=', '-=', '*=',
    '/=', '%=', '<<=', '>>=', '>>>=', '&=', '|=', '^='
]
literals = [
    'true', 'false', 'NULL', 'undefined', 'NaN', 'Infinity', '""', "''", "``"
]
delimiters = [
    '(', ')', '{', '}', '[', ']', '"', "'", "`", ',', ';', ':', '.', '?', '=>'
]
keyWords = [
    'if', 'else', 'else if', 'switch', 'case', 'default', 'while', 'do', 'for',
    'break', 'continue', 'return', 'function', 'var', 'let', 'const', 'new',
    'delete', 'in', 'instanceof', 'typeof', 'void', 'this', 'super', 'class',
    'extends', 'import', 'export', 'async', 'await', 'try', 'catch', 'finally',
    'throw', 'with', 'debugger', 'arguments', 'yield', "console", "log", "alert"
]

# Expresiones regulares para los diferentes tipos de tokens
identifierRegex = r"\b[a-zA-Z_$][a-zA-Z0-9_$]*\b"
numberRegex = r"\b\d+(\.\d+)?\b"
stringRegex = r'"[^"]*"|\'[^\']*\'|`[^`]*`'
operatorRegex = r"|".join(re.escape(op) for op in operators)
delimiterRegex = r"|".join(re.escape(delim) for delim in delimiters)
keywordRegex = r"\b" + r"\b|\b".join(keyWords) + r"\b"
commentRegex = r"//.*|/\*[\s\S]*?\*/"

# Regex para capturar todos los tokens válidos
validTokensRegex = (
    f"({commentRegex})|({stringRegex})|({numberRegex})|({identifierRegex})|"
    f"({operatorRegex})|({delimiterRegex})|({keywordRegex})"
)

# Función para analizar léxicamente el código
def analizarLexico(code):
    # Elimina los espacios en blanco al inicio y al final del código
    code = code.strip()
    # Encuentra todos los tokens válidos
    validTokens = re.findall(validTokensRegex, code, re.MULTILINE | re.DOTALL)
    # Filtra los grupos vacíos
    validTokens = [t for ts in validTokens for t in ts if t]

    # Inicializa una lista para guardar los tokens no válidos
    invalidTokens = []

    # Índice para seguir la posición en el código
    index = 0

    while index < len(code):
        # Encuentra el próximo token válido o el final del código
        match = re.search(validTokensRegex, code[index:], re.MULTILINE | re.DOTALL)
        if match:
            start, end = match.span()
            # Agrega el texto antes del token válido a los tokens no válidos
            if start > 0:
                invalidTokens.append(code[index:index+start])
            # Actualiza el índice para continuar después del token válido
            index += end
        else:
            # Si no hay más tokens válidos, agrega el resto del código a los tokens no válidos
            invalidTokens.append(code[index:])
            break

    tokens = []
    # Imprime los tokens válidos y crea un diccionario con la información
    for c in validTokens:
        if c in operators:
            tokens.append({"tipo": "Operador", "valor": c})
            print(f'Operador: {c}')
        elif c in literals:
            tokens.append({"tipo": "Literal", "valor": c})
            print(f'Literal: {c}')
        elif c in delimiters:
            tokens.append({"tipo": "Delimitador", "valor": c})
            print(f'Delimitador: {c}')
        elif c in keyWords:
            tokens.append({"tipo": "Palabra clave", "valor": c})
            print(f'Palabra clave: {c}')
        elif re.fullmatch(commentRegex, c):
            tokens.append({"tipo": "Comentario", "valor": c})
            print(f'Comentario: {c}')
        elif re.fullmatch(numberRegex, c):
            tokens.append({"tipo": "Número", "valor": c})
            print(f'Número: {c}')
        elif re.fullmatch(identifierRegex, c):
            tokens.append({"tipo": "Identificador", "valor": c})
            print(f'Identificador: {c}')
        elif re.fullmatch(stringRegex, c):
            tokens.append({"tipo": "String", "valor": c})
            print(f'String: {c}')

    # Imprime los tokens no válidos
    for c in invalidTokens:
        if c.strip():
            print(f'Token no válido: {c}')
            
    # Si es un espacio en blanco, lo sacamos del arreglo de tokens no válidos
    invalidTokens = [c for c in invalidTokens if c.strip()]
   
	# Retorna True si no hay tokens no válidos, False en caso contrario
    return {"isValid": not bool(invalidTokens), "tokensList": tokens}

# Ejemplo de uso
# codigo_js = "123asd // Esto es un 12comentario"
# print(analizarLexico(codigo_js))
