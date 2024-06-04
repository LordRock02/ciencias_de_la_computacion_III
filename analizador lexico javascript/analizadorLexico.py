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
    f"({keywordRegex})|({commentRegex})|({stringRegex})|({literalRegex})|"
    f"({operatorRegex})|({delimiterRegex})|({numberRegex})|({identifierRegex})"
)

# Función para clasificar tokens
def clasificar_token(token):
    tipo = determinar_tipo(token)
    return {"valor": token, "tipo": tipo, "esValido": tipo != "NAN"}

tipos_tokens = {
    "cadena": stringRegex,
    "keyWord": keywordRegex,
    "comentario": commentRegex,
    "literal": literalRegex,
    "operador": operatorRegex,
    "delimitador": delimiterRegex,
    "numero": numberRegex,
    "identificador": identifierRegex,
}

def determinar_tipo(token):
    for tipo, regex in tipos_tokens.items():
        if re.match(regex, token):
            return tipo
    return "NAN"

# Definición de los diferentes tipos de operadores
arithmeticOperators = ['+', '-', '*', '/']
assignmentOperators = ['=']
comparisonOperators = ['>=', '<=', '==', '!=', '>', '<']
logicalOperators = ['&&', '||', '!']
incrementDecrementOperators = ['++', '--']
compoundAssignmentOperators = ['+=', '-=', '*=', '/=', '%=', '^=']

# Definición de los diferentes tipos de literales
booleanLiterals = ['true', 'false']
stringLiterals = ['""', "''", "``"]
arrayLiterals = ['[]']

# Definición de los diferentes tipos de delimitadores
delimitertipos = {
    '=>': 'ARROW_FUNCTION',
    '(': 'OPENING_PARENTHESIS',
    ')': 'CLOSING_PARENTHESIS',
    '{': 'OPENING_CURLY_BRACE',
    '}': 'CLOSING_CURLY_BRACE',
    '[': 'OPENING_SQUARE_BRACKET',
    ']': 'CLOSING_SQUARE_BRACKET',
    '"': 'STRING_DELIMITER',
    "'": 'STRING_DELIMITER',
    '`': 'STRING_DELIMITER',
    ',': 'PARAMETER_DELIMITER',
    ';': 'STATEMENT_TERMINATOR',
    '.': 'OBJECT_PROPERTY_ACCESSOR',
    '?': 'TERNARY_OPERATOR',
    ':': 'COLON'
}

# Definición de los diferentes tipos de palabras clave
keywordCategories = {
    'if': 'IF_KEYWORD',
    'else': 'ELSE_KEYWORD',
    'console': 'CONSOLE_KEYWORD',
    'log': 'LOG_KEYWORD',
    'alert': 'ALERT_KEYWORD',
    'let': 'VARIABLE_DECLARATION_KEYWORD',
    'const': 'VARIABLE_DECLARATION_KEYWORD',
    'var': 'VARIABLE_DECLARATION_KEYWORD',
}

# Funcion para clasificar tokens
def clasificarTokens(tokens):
    for linea in tokens:
        for token in linea:
            if token['tipo'] == 'operador':
                if token['valor'] in incrementDecrementOperators:
                    token['tipo'] = 'INCREMENT_DECREMENT_OPERATOR'
                elif token['valor'] in arithmeticOperators:
                    token['tipo'] = 'ARITHMETIC_OPERATOR'
                elif token['valor'] in assignmentOperators:
                    token['tipo'] = 'ASSIGNMENT_OPERATOR'
                elif token['valor'] in comparisonOperators:
                    token['tipo'] = 'COMPARISON_OPERATOR'
                elif token['valor'] in logicalOperators:
                    token['tipo'] = 'LOGICAL_OPERATOR'
                elif token['valor'] in compoundAssignmentOperators:
                    token['tipo'] = 'COMPOUND_ASSIGNMENT_OPERATOR'
            if token['tipo'] == 'literal':
                if token['valor'] in booleanLiterals:
                    token['tipo'] = 'BOOLEAN_LITERAL'
                elif token['valor'] in stringLiterals:
                    token['tipo'] = 'STRING'
                elif token['valor'] in arrayLiterals:
                    token['tipo'] = 'ARRAY_LITERAL'
            if token['tipo'] == 'delimitador' and token['valor'] in delimitertipos:
                token['tipo'] = delimitertipos[token['valor']]
            if token['tipo'] == 'keyWord' and token['valor'] in keywordCategories:
                token['tipo'] = keywordCategories[token['valor']]
            if token['tipo'] == 'identificador':
                token['tipo'] = 'IDENTIFIER'
            if token['tipo'] == 'comentario':
                token['tipo'] = 'COMMENT'
            if token['tipo'] == 'cadena':
                token['tipo'] = 'STRING'
            if token['tipo'] == 'numero':
                token['tipo'] = 'NUMBER'
    return tokens

# Función para analizar léxicamente el código
def analizarLexico(code):
    # Elimina los espacios en blanco al inicio y al final del código
    code = code.strip()
    # Divide el código en líneas
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
                    tokensObjetos.append(clasificar_token(token_no_valido))
                # Agrega el token válido
                token_valido = linea[index+start:index+end]
                tokensObjetos.append(clasificar_token(token_valido))
                index += end
            else:
                # Si no hay más tokens válidos, procesa el resto de la línea como token no válido
                token_no_valido = linea[index:]
                tokensObjetos.append(clasificar_token(token_no_valido))
                break

        # Agrega la lista de objetos de tokens a la lista de líneas
        codigoPorLineas.append(tokensObjetos)

    # Clasifica los tokens
    codigoPorLineas = clasificarTokens(codigoPorLineas)

    # Retorna la lista de listas de objetos de tokens
    return codigoPorLineas

# Función para generar el reporte léxico
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
    reporte = {'errores':erroresLinea, 'tokens':tokensLinea}
    return reporte

# Ejemplo de uso
# codigo_js = """
# let 12x = '';
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
