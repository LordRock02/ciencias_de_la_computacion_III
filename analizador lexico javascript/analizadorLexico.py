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
    'throw', 'with', 'debugger', 'arguments', 'yield'
]
comments = ['//', '/*', '*/']

# Expresiones regulares para los diferentes tipos de tokens
identifierRegex = r"[a-zA-Z_$][a-zA-Z0-9_$]*"
numberRegex = r"\b\d+(\.\d+)?\b"
stringRegex = r'"[^"]*"|\'[^\']*\'|`[^`]*`'
operatorRegex = r"|".join(re.escape(op) for op in operators)
delimiterRegex = r"|".join(re.escape(delim) for delim in delimiters)
keywordRegex = r"\b" + r"\b|\b".join(keyWords) + r"\b"
commentRegex = r"//.*?$|/\*[\s\S]*?\*/"

# Regex para capturar todos los tokens
tokensRegex = (
    f"({stringRegex})|({numberRegex})|({identifierRegex})|"
    f"({operatorRegex})|({delimiterRegex})|({keywordRegex})|({commentRegex})"
)

def analizarLexico(code):
    # Elimina los espacios en blanco al inicio y al final del código
    code = code.strip()
    # Encuentra todos los tokens
    tokens = re.findall(tokensRegex, code, re.MULTILINE | re.DOTALL)
    # Filtra los grupos vacíos
    tokens = [t for ts in tokens for t in ts if t]

    for c in tokens:
        if c in operators:
            print(f'Operador: {c}')
        elif c in literals:
            print(f'Literal: {c}')
        elif c in delimiters:
            print(f'Delimitador: {c}')
        elif c in keyWords:
            print(f'Palabra clave: {c}')
        elif c in comments:
            print(f'Comentario: {c}')
        elif re.fullmatch(identifierRegex, c):
            print(f'Identificador: {c}')
        elif re.fullmatch(stringRegex, c):
            print(f'String: {c}')
        elif re.fullmatch(numberRegex, c):
            print(f'Número: {c}')
        else:
            print(f'Token no reconocido: {c}')

    return True

# print('code : ')
# code = input()
# print(f'resultado analisis: {analizarLexico(code)}')
