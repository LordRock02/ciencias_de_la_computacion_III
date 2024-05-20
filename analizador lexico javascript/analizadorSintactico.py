import re;
import analizadorLexico;

# Definición de los diferentes tipos de operadores
arithmeticOperators = ['+', '-', '*', '/']
assignmentOperators = ['=']
comparisonOperators = ['>', '<', '>=', '<=']
logicalOperators = ['&&', '||', '!']
bitwiseOperators = ['&', '|', '^', '~', '<<', '>>', '>>>']
incrementDecrementOperators = ['++', '--']
equalityOperators = ['==', '!=']
compoundAssignmentOperators = ['+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '>>>=', '&=', '|=', '^=']

# Definición de los diferentes tipos de literales
booleanLiterals = ['true', 'false']
nullLiteral = ['NULL']
undefinedLiteral = ['undefined']
numericLiterals = ['NaN', 'Infinity']
stringLiterals = ['""', "''", "``"]
arrayLiterals = ['[]']

# Definición de los diferentes tipos de delimitadores
delimitertipos = {
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
    '=>': 'ARROW_FUNCTION',
    ':': 'COLON'
}

# Definición de los diferentes tipos de palabras clave
keywordCategories = {
    'if': 'IF_KEYWORD',
    'else': 'ELSE_KEYWORD',
    'switch': 'SWITCH_KEYWORD',
    'case': 'CASE_KEYWORD',
    'default': 'DEFAULT_KEYWORD',
    'while': 'WHILE_KEYWORD',
    'do': 'DO_KEYWORD',
    'for': 'FOR_KEYWORD',
    'break': 'BREAK_KEYWORD',
    'continue': 'CONTINUE_KEYWORD',
    'return': 'RETURN_KEYWORD',
    'function': 'FUNCTION_KEYWORD',
    'var': 'DECLARATION_KEYWORD',
    'let': 'DECLARATION_KEYWORD',
    'const': 'DECLARATION_KEYWORD',
    'new': 'NEW_KEYWORD',
    'delete': 'DELETE_KEYWORD',
    'in': 'IN_KEYWORD',
    'instanceof': 'INSTANCEOF_KEYWORD',
    'tipoof': 'tipoOF_KEYWORD',
    'void': 'VOID_KEYWORD',
    'this': 'THIS_KEYWORD',
    'super': 'SUPER_KEYWORD',
    'class': 'CLASS_KEYWORD',
    'extends': 'EXTENDS_KEYWORD',
    'import': 'IMPORT_KEYWORD',
    'export': 'EXPORT_KEYWORD',
    'async': 'ASYNC_KEYWORD',
    'await': 'AWAIT_KEYWORD',
    'try': 'TRY_KEYWORD',
    'catch': 'CATCH_KEYWORD',
    'finally': 'FINALLY_KEYWORD',
    'throw': 'THROW_KEYWORD',
    'with': 'WITH_KEYWORD',
    'debugger': 'DEBUGGER_KEYWORD',
    'arguments': 'ARGUMENTS_KEYWORD',
    'yield': 'YIELD_KEYWORD'
}

def clasificarTokens(tokens):
    for token in tokens:
        if token['tipo'] == 'Operador':
            if token['valor'] in arithmeticOperators:
                token['tipo'] = 'ARITHMETIC_OPERATOR'
            elif token['valor'] in assignmentOperators:
                token['tipo'] = 'ASSIGNMENT_OPERATOR'
            elif token['valor'] in comparisonOperators:
                token['tipo'] = 'COMPARISON_OPERATOR'
            elif token['valor'] in logicalOperators:
                token['tipo'] = 'LOGICAL_OPERATOR'
            elif token['valor'] in bitwiseOperators:
                token['tipo'] = 'BITWISE_OPERATOR'
            elif token['valor'] in incrementDecrementOperators:
                token['tipo'] = 'INCREMENT_DECREMENT_OPERATOR'
            elif token['valor'] in equalityOperators:
                token['tipo'] = 'EQUALITY_OPERATOR'
            elif token['valor'] in compoundAssignmentOperators:
                token['tipo'] = 'COMPOUND_ASSIGNMENT_OPERATOR'
        if token['tipo'] == 'Literal':
            if token['valor'] in booleanLiterals:
                token['tipo'] = 'BOOLEAN_LITERAL'
            elif token['valor'] in nullLiteral:
                token['tipo'] = 'NULL_LITERAL'
            elif token['valor'] in undefinedLiteral:
                token['tipo'] = 'UNDEFINED_LITERAL'
            elif token['valor'] in numericLiterals:
                token['tipo'] = 'NUMERIC_LITERAL'
            elif token['valor'] in stringLiterals:
                token['tipo'] = 'STRING'
            elif token['valor'] in arrayLiterals:
                token['tipo'] = 'ARRAY_LITERAL'
        if token['tipo'] == 'Delimitador' and token['valor'] in delimitertipos:
            token['tipo'] = delimitertipos[token['valor']]
        if token['tipo'] == 'Palabra clave' and token['valor'] in keywordCategories:
            token['tipo'] = keywordCategories[token['valor']]
        if token['tipo'] == 'Identificador':
            token['tipo'] = 'IDENTIFIER'
        if token['tipo'] == 'Comentario':
            token['tipo'] = 'COMMENT'
        if token['tipo'] == 'String':
            token['tipo'] = 'STRING'
        if token['tipo'] == 'Número':
            token['tipo'] = 'NUMBER'
    return tokens

# Función para verificar si un conjunto de tokens es una asignación de variable
def isAssignmentStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una asignación
    if index + 3 >= len(tokens):
        return {"isValid": False}

    # Desempaquetar los tokens necesarios
    identifier, operator, value, terminator = tokens[index:index+4]

    # Verificar si los tokens cumplen con la estructura de una asignación
    if (identifier['tipo'] == 'IDENTIFIER' and
        operator['tipo'] == 'ASSIGNMENT_OPERATOR' and
        value['tipo'] in ['IDENTIFIER', 'STRING', 'NUMBER', 'BOOLEAN_LITERAL', 'NULL_LITERAL', 'UNDEFINED_LITERAL', 'ARRAY_LITERAL'] and
        terminator['tipo'] == 'STATEMENT_TERMINATOR'):
        
        # Agregar la asignación a la lista de statements
        statementsList.append({'tipo': 'ASSIGNMENT_STATEMENT', 'valor': tokens[index:index+4]})
        return {'isValid': True, 'index': index + 4}
    
    return {"isValid": False}

# Función para verificar si un conjunto de tokens es una declaración de variable
def isDeclarationStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 1 >= len(tokens):
        return {"isValid": False}

    # Verificar si el token actual es una palabra clave de declaración
    if tokens[index]['tipo'] != 'DECLARATION_KEYWORD':
        return {"isValid": False}

    # Intentar encontrar una asignación después de la palabra clave de declaración
    result = isAssignmentStatement(tokens, index + 1, statementsList)
    if result['isValid']:
        # Agregar la declaración a la lista de statements
        statementsList.append({'tipo': 'DECLARATION_STATEMENT', 'valor': tokens[index:result['index']]})
        return {'isValid': True, 'index': result['index']}
    
    return {"isValid": False}

statements = []
# Función para verificar si el codigo es correcto sintacticamente
def analizadorSintactico(code):
    result = analizadorLexico.analizarLexico(code)
    print(result)
    if result['isValid']:
        clasifiedTokensList = clasificarTokens(result['tokensList'])
        print(clasifiedTokensList)
        index = 0
        isValid = True
        while isValid and index < len(clasifiedTokensList):
            print(index, len(clasifiedTokensList), clasifiedTokensList[index])
            if clasifiedTokensList[index]['tipo'] == 'IDENTIFIER':
                aux = isAssignmentStatement(clasifiedTokensList, index, statements)
                print(aux)
                if aux['isValid']:
                    index = aux['index']
                else:
                    isValid = False
                    print('El código es incorrecto sintacticamente')
                    break
            elif clasifiedTokensList[index]['tipo'] == 'DECLARATION_KEYWORD':
                aux = isDeclarationStatement(clasifiedTokensList, index, statements)
                if aux['isValid']:
                    index = aux['index']
                else:
                    isValid = False
                    print('El código es incorrecto sintacticamente')
                    break
        
        if isValid:
            print(statements)
            print('El código es correcto sintacticamente')         
    else:
        print('El código contiene tokens no válidos')
    
 # Ejemplo de uso
codigo_js = "var x = 5; x=4;"
analizadorSintactico(codigo_js)
