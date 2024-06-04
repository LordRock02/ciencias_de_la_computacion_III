import re

# Listas para los diferentes tipos de tokens en Javascript
operators = [
    '++', '--', '==', '!=', '>=', '<=', '&&', '||', '+=', 
    '-=', '*=', '/=', '%=', '&=', '|=', '^=', '!',
    '^', '+', '-', '*', '=', '/', '%', '>', '<'
]
literals = [
    'true', 'false', '""', "''", "``", 'null', 'undefined', 'NaN', 'Infinity'
]
delimiters = [
    '(', ')', '{', '}', '[', ']', '"', "'", "`", ',', ';', ':', '.', '?', '=>'
]
keyWords = [
    'if', 'else', 'let', 'const', 'var', 'console', 'log', 'alert'
]
otherKeyWords = [
    'switch', 'case', 'default', 'while', 'do', 'for',
    'break', 'continue', 'return', 'function', 'new',
    'delete', 'in', 'instanceof', 'typeof', 'void', 'this', 'super', 'class',
    'extends', 'import', 'export', 'async', 'await', 'try', 'catch', 'finally',
    'throw', 'with', 'debugger', 'arguments', 'yield'
]

# Expresiones regulares para los diferentes tipos de tokens
identifierRegex = r"\b[a-zA-Z_$][a-zA-Z0-9_$]*\b"
numberRegex = r"\b\d+(\.\d+)?\b"
stringRegex = r'"[^"]*"|\'[^\']*\'|`[^`]*`'
operatorRegex = r"|".join(re.escape(op) for op in operators)
literalRegex = r"\b" + r"\b|\b".join(literals) + r"\b"
delimiterRegex = r"|".join(re.escape(delim) for delim in delimiters)
keywordRegex = r"\b" + r"\b|\b".join(keyWords) + r"\b"


commentRegex = r"//.*|/\*[\s\S]*?\*/"

# Regex para capturar todos los tokens válidos
validTokensRegex = (
    f"({literalRegex})|({commentRegex})|({stringRegex})|({numberRegex})|({identifierRegex})|"
    f"({operatorRegex})|({delimiterRegex})|({keywordRegex})"
)

# Función para clasificar tokens
def clasificar_token(token, esValido):
    tipo = "NAN" if not esValido else determinar_tipo(token)
    return {"valor": token, "tipo": tipo, "esValido": esValido}

tipos_tokens = {
    "cadena": stringRegex,
    "keyWord": keywordRegex,
    "operador": operatorRegex,
    "delimitador": delimiterRegex,
    "numero": numberRegex,
    "identificador": identifierRegex,
    "literal": literalRegex,
}

def determinar_tipo(token):
    for tipo, regex in tipos_tokens.items():
        if re.match(regex, token):
            return tipo
    return "NAN"

# Función para analizar léxicamente el código
def analizarLexico(code):
    # Elimina los espacios en blanco al inicio y al final del código
    code = code.strip()
    lineas = code.split('\n')
    codigoPorLineas = []

    for linea in lineas:
        tokensObjetos = []
        index = 0
        while index < len(linea):
            if linea[index].isspace():
                index += 1
                continue

            # Encuentra el próximo token válido o el final de la línea
            match = re.search(validTokensRegex, linea[index:], re.MULTILINE | re.DOTALL)
            if match:
                start, end = match.span()
                # Si hay texto antes del token válido, es un token no válido
                if start > 0:
                    token_no_valido = linea[index:index+start]
                    tokensObjetos.append(clasificar_token(token_no_valido, False))
                # Agrega el token válido
                token_valido = linea[index+start:index+end]
                tokensObjetos.append(clasificar_token(token_valido, True))
                index += end
            else:
                # Si no hay más tokens válidos, procesa el resto de la línea como token no válido
                token_no_valido = linea[index:]
                tokensObjetos.append(clasificar_token(token_no_valido, False))
                break

        # Agrega la lista de objetos de tokens a la lista de líneas
        codigoPorLineas.append(tokensObjetos)

    # Retorna la lista de listas de objetos de tokens
    return codigoPorLineas

def generarReporteLexico(codigoAnalizado):
    errores = ""
    tokens = ""
    numeroLinea = 1

    for linea in codigoAnalizado:
        # Variables para almacenar los errores y tokens de la línea actual
        erroresLinea = []
        tokensLinea = []

        for tokenObj in linea:
            # Construye la lista de tokens con su tipo
            tokensLinea.append(f"{tokenObj['valor']}: {tokenObj['tipo']}")

            # Si el token no es válido, agrega un mensaje de error
            if not tokenObj['esValido']:
                erroresLinea.append(f"LEXIC_ERROR there is a lexic error in line {numeroLinea} due to the token {tokenObj['valor']}")

        # Agrega los errores y tokens de la línea al reporte general
        if erroresLinea:
            errores += "\n".join(erroresLinea) + "\n"
        tokens += "\n".join(tokensLinea) + "\n"

        numeroLinea += 1

    # Construye el reporte final
    reporteFinal = "----ERRORES----\n" + errores + "\n----TOKENS----\n" + tokens
    return reporteFinal
    
# # Ejemplo de uso
# codigo_js = """
# let x = '';
# if (x > 10) {
#   console.log('X es mayor o igual a 10');
# } else if (x < 10){
#     console.log('X es menor a 10');
# } else {
#     console.log('X es igual a 10');
# }
# """

# codigoAnalizado = analizarLexico(codigo_js)
# print(generarReporteLexico(codigoAnalizado))
