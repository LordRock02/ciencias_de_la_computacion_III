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
    'yield': 'YIELD_KEYWORD',
    'console': 'CONSOLE_KEYWORD',
    'log': 'LOG_KEYWORD',
    'alert': 'ALERT_KEYWORD'
}

def clasificarTokens(tokens):
    for token in tokens:
        if token['tipo'] == 'Operador':
            # Verificar si los siguientes dos tokens juntos forman un operador de incremento o decremento
            if token['valor'] + tokens[tokens.index(token) + 1]['valor'] in incrementDecrementOperators:
                # Eliminar el siguiente token y actualizar el valor del token actual y su tipo
                tokens[tokens.index(token)]['valor'] += tokens[tokens.index(token) + 1]['valor']
                tokens[tokens.index(token)]['tipo'] = 'INCREMENT_DECREMENT_OPERATOR'
                tokens.pop(tokens.index(token) + 1)
            elif token['valor'] in arithmeticOperators:
                token['tipo'] = 'ARITHMETIC_OPERATOR'
            elif token['valor'] in assignmentOperators:
                token['tipo'] = 'ASSIGNMENT_OPERATOR'
            elif token['valor'] in comparisonOperators:
                token['tipo'] = 'COMPARISON_OPERATOR'
            elif token['valor'] in logicalOperators:
                token['tipo'] = 'LOGICAL_OPERATOR'
            elif token['valor'] in bitwiseOperators:
                token['tipo'] = 'BITWISE_OPERATOR'
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

# Función para verificar si un conjunto de tokens es una condicción
def isConditiosStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 2 >= len(tokens):
        return {"isValid": False}
    
    # Desempaquetar los tokens necesarios
    identifier, condition, value = tokens[index:index+3]
    
    # Verificar si los tokens cumplen con la estructura de una condicióm
    if (identifier['tipo'] == 'IDENTIFIER' and
        condition['tipo'] == 'COMPARISON_OPERATOR' and
        value['tipo'] in ['IDENTIFIER', 'STRING', 'NUMBER', 'BOOLEAN_LITERAL', 'NULL_LITERAL', 'UNDEFINED_LITERAL', 'ARRAY_LITERAL']):
        
        # Agregar la asignación a la lista de statements
        statementsList.append({'tipo': 'CONDITION_STATEMENT', 'valor': tokens[index:index+3]})
        return {'isValid': True, 'index': index + 3}
    
    return {"isValid": False}

# Función para verificar si un conjunto de tokens es un if
def isIfStatement(tokens, index, statementsList):
    
    # Verificar si hay suficientes tokens para una declaración
    if index + 6 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de if
    if tokens[index]['tipo'] != 'IF_KEYWORD':
        return {"isValid": False}

    # Verificar si el token siguiente es un parentesis de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_PARENTHESIS':
        return {"isValid": False}
    
    # Intentar encontrar una condición después del parentesis de apertura
    result = isConditiosStatement(tokens, index + 2, statementsList)
    if result['isValid']:
        # Verificar si el token siguiente es un parentesis de cierre
        if tokens[result['index']]['tipo'] != 'CLOSING_PARENTHESIS':
            return {"isValid": False}
        
        # Verificar si el token siguiente es una llave de apertura
        if tokens[result['index'] + 1]['tipo'] != 'OPENING_CURLY_BRACE':
            return {"isValid": False}
        
        # Agregar la declaración a la lista de statements
        statementsList.append({'tipo': 'IF_STATEMENT', 'valor': tokens[index:result['index'] + 2]})
        return {'isValid': True, 'index': result['index'] + 2}
    
    return {"isValid": False}

# funcion para verificar si un conjunto de tokens es un else
def isElseStatement(tokens, index, statementsList):
    
    # Verificar si hay suficientes tokens para una declaración
    if index + 1 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de else
    if tokens[index]['tipo'] != 'ELSE_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es una llave de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_CURLY_BRACE':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'ELSE_STATEMENT', 'valor': tokens[index:index + 2]})
    return {'isValid': True, 'index': index + 2} 

# Función para verificar si un conjunto de tokens es un else if
def isElseIfStatement(tokens, index, statementsList):
        
    # Verificar si hay suficientes tokens para una declaración
    if index + 7 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de else
    if tokens[index]['tipo'] != 'ELSE_KEYWORD':
        return {"isValid": False}
    
    # Intentar encontrar un if después de la palabra clave de else
    result = isIfStatement(tokens, index + 1, statementsList)
    if result['isValid']:
        # Agregar la declaración a la lista de statements
        statementsList.append({'tipo': 'ELSE_IF_STATEMENT', 'valor': tokens[index:result['index']]})
        return {'isValid': True, 'index': result['index']}
    return {"isValid": False}

# Funcion para verificar si un conjunto de tokens es un switch
def isSwitchStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 4 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de switch
    if tokens[index]['tipo'] != 'SWITCH_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_PARENTHESIS':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un identificador
    if tokens[index + 2]['tipo'] != 'IDENTIFIER':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de cierre
    if tokens[index + 3]['tipo'] != 'CLOSING_PARENTHESIS':
        return {"isValid": False}
    
    # Verificar si el token siguiente es una llave de apertura
    if tokens[index + 4]['tipo'] != 'OPENING_CURLY_BRACE':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'SWITCH_STATEMENT', 'valor': tokens[index:index + 5]})
    return {'isValid': True, 'index': index + 5}

# Funcion para verificar si un conjunto de tokens es un case
def isCaseStatement(tokens, index, statementsList):
    
    # Verificar si hay suficientes tokens para una declaración
    if index + 2 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de case
    if tokens[index]['tipo'] != 'CASE_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un identificador
    if tokens[index + 1]['tipo'] not in ['IDENTIFIER', 'STRING', 'NUMBER']:
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de dos puntos
    if tokens[index + 2]['tipo'] != 'COLON':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'CASE_STATEMENT', 'valor': tokens[index:index + 3]})
    return {'isValid': True, 'index': index + 3}

# Funcion para verificar si un conjunto de tokens es un default
def isDefaultStatement(tokens, index, statementsList):
    
    # Verificar si hay suficientes tokens para una declaración
    if index + 1 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de default
    if tokens[index]['tipo'] != 'DEFAULT_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de dos puntos
    if tokens[index + 1]['tipo'] != 'COLON':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'DEFAULT_STATEMENT', 'valor': tokens[index:index + 2]})
    return {'isValid': True, 'index': index + 2}

# Funcion para verificar si un conjunto de tokens es un while
def isWhileStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 6 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de while
    if tokens[index]['tipo'] != 'WHILE_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_PARENTHESIS':
        return {"isValid": False}
    
    # Intentar encontrar una condición después del parentesis de apertura
    result = isConditiosStatement(tokens, index + 2, statementsList)
    if result['isValid']:
        # Verificar si el token siguiente es un parentesis de cierre
        if tokens[result['index']]['tipo'] != 'CLOSING_PARENTHESIS':
            return {"isValid": False}
        
        # Verificar si el token siguiente es una llave de apertura
        if tokens[result['index'] + 1]['tipo'] != 'OPENING_CURLY_BRACE':
            return {"isValid": False}
        
        # Agregar la declaración a la lista de statements
        statementsList.append({'tipo': 'WHILE_STATEMENT', 'valor': tokens[index:result['index'] + 2]})
        return {'isValid': True, 'index': result['index'] + 2}
    
    return {"isValid": False}

# Funcion para verificar si un conjunto de tokens es un do
def isDoStatement(tokens, index, statementlist):
    # Verificar si hay suficientes tokens para una declaración
    if index + 1 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de do
    if tokens[index]['tipo'] != 'DO_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es una llave de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_CURLY_BRACE':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementlist.append({'tipo': 'DO_STATEMENT', 'valor': tokens[index:index + 2]})
    return {'isValid': True, 'index': index + 2}

# Funcion para verificar si un conjunto de tokens es un for
def isForStatement(tokens, index, statementlist):
    # Verificar si hay suficientes tokens para un for
    if index + 14 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de for
    if tokens[index]['tipo'] != 'FOR_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_PARENTHESIS':
        return {"isValid": False}
    
    # Intentar encontrar una declaración después del parentesis de apertura
    result = isDeclarationStatement(tokens, index + 2, statementlist)
    if result['isValid']:
        
        # Intentar encontrar una condición después del punto y coma
        result = isConditiosStatement(tokens, result['index'], statementlist)
        if result['isValid']:
            # Verificar si el token siguiente es un punto y coma
            if tokens[result['index']]['tipo'] != 'STATEMENT_TERMINATOR':
                return {"isValid": False}
            
            
            # Verificar si el token siguiente es un identificador
            if tokens[result['index'] + 1]['tipo'] != 'IDENTIFIER':
                return {"isValid": False}
            
            # Verificar si el token siguiente es un operador de incremento o decremento
            if tokens[result['index'] + 2]['tipo'] != 'INCREMENT_DECREMENT_OPERATOR':
                print(tokens[result['index'] + 2]['tipo'])
                return {"isValid": False}

            # Verificar si el token siguiente es un parentesis de cierre
            if tokens[result['index'] + 3]['tipo'] != 'CLOSING_PARENTHESIS':
                return {"isValid": False}
            
            
            # Verificar si el token siguiente es una llave de apertura
            if tokens[result['index'] + 4]['tipo'] != 'OPENING_CURLY_BRACE':
                return {"isValid": False}
            
            # Agregar la declaración a la lista de statements
            statementlist.append({'tipo': 'FOR_STATEMENT', 'valor': tokens[index:result['index'] + 5]})
            return {'isValid': True, 'index': result['index'] + 5}
    
    return {"isValid": False}   

# Función para verificar si un conjunto de tokens es un break
def isBreakStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 1 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de break
    if tokens[index]['tipo'] != 'BREAK_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de punto y coma
    if tokens[index + 1]['tipo'] != 'STATEMENT_TERMINATOR':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'BREAK_STATEMENT', 'valor': tokens[index:index + 2]})
    return {'isValid': True, 'index': index + 2}

# Función para verificar si un conjunto de tokens es un continue
def isContinueStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 1 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de continue
    if tokens[index]['tipo'] != 'CONTINUE_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de punto y coma
    if tokens[index + 1]['tipo'] != 'STATEMENT_TERMINATOR':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'CONTINUE_STATEMENT', 'valor': tokens[index:index + 2]})
    return {'isValid': True, 'index': index + 2}

# Función para verificar si un conjunto de tokens es un return
def isReturnStatement(tokens, index, statementsList):
    # Verificar si hay suficientes tokens para una declaración
    if index + 2 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de return
    if tokens[index]['tipo'] != 'RETURN_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un identificador
    if tokens[index + 1]['tipo'] not in ['IDENTIFIER', 'STRING', 'NUMBER', 'BOOLEAN_LITERAL', 'NULL_LITERAL', 'UNDEFINED_LITERAL', 'ARRAY_LITERAL']:
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de punto y coma
    if tokens[index + 2]['tipo'] != 'STATEMENT_TERMINATOR':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementsList.append({'tipo': 'RETURN_STATEMENT', 'valor': tokens[index:index + 2]})
    return {'isValid': True, 'index': index + 3}

# Funcion para verificar si un conjunto de tokens es un console.log
def isConsoleLogStatement(tokens, index, statementList):
    # Verificar si hay suficientes tokens para un console.log
    if index + 6 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de console
    if tokens[index]['tipo'] != 'CONSOLE_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de punto
    if tokens[index + 1]['tipo'] != 'OBJECT_PROPERTY_ACCESSOR':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un identificador
    if tokens[index + 2]['tipo'] != 'LOG_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de apertura
    if tokens[index + 3]['tipo'] != 'OPENING_PARENTHESIS':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un identificador
    if tokens[index + 4]['tipo'] not in ['IDENTIFIER', 'STRING', 'NUMBER', 'BOOLEAN_LITERAL', 'NULL_LITERAL', 'UNDEFINED_LITERAL', 'ARRAY_LITERAL']:
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de cierre
    if tokens[index + 5]['tipo'] != 'CLOSING_PARENTHESIS':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de punto y coma
    if tokens[index + 6]['tipo'] != 'STATEMENT_TERMINATOR':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementList.append({'tipo': 'CONSOLE_LOG_STATEMENT', 'valor': tokens[index:index + 7]})
    return {'isValid': True, 'index': index + 7}

# Función para verificar si un conjunto de tokens es un alert
def isAlertStatement(tokens, index, statementList):
    # Verificar si hay suficientes tokens para un alert
    if index + 4 >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una palabra clave de alert
    if tokens[index]['tipo'] != 'ALERT_KEYWORD':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de apertura
    if tokens[index + 1]['tipo'] != 'OPENING_PARENTHESIS':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un identificador
    if tokens[index + 2]['tipo'] not in ['IDENTIFIER', 'STRING', 'NUMBER', 'BOOLEAN_LITERAL', 'NULL_LITERAL', 'UNDEFINED_LITERAL', 'ARRAY_LITERAL']:
        return {"isValid": False}
    
    # Verificar si el token siguiente es un parentesis de cierre
    if tokens[index + 3]['tipo'] != 'CLOSING_PARENTHESIS':
        return {"isValid": False}
    
    # Verificar si el token siguiente es un delimitador de punto y coma
    if tokens[index + 4]['tipo'] != 'STATEMENT_TERMINATOR':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementList.append({'tipo': 'ALERT_STATEMENT', 'valor': tokens[index:index + 5]})
    return {'isValid': True, 'index': index + 5}

# Función para verificar si un conjunto de tokens es un comentario
def isCommentStatement(tokens, index, statementList):
    # Verificar si hay suficientes tokens para un comentario
    if index >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es un comentario
    if tokens[index]['tipo'] != 'COMMENT':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementList.append({'tipo': 'COMMENT_STATEMENT', 'valor': tokens[index]})
    return {'isValid': True, 'index': index + 1}

# Función para verificar si un conjunto de tokens es una llave de cierre
def isClosingCurlyBrace(tokens, index, statementList):
    # Verificar si hay suficientes tokens para una llave de cierre
    if index >= len(tokens):
        return {"isValid": False}
    
    # Verificar si el token actual es una llave de cierre
    if tokens[index]['tipo'] != 'CLOSING_CURLY_BRACE':
        return {"isValid": False}
    
    # Agregar la declaración a la lista de statements
    statementList.append({'tipo': 'CLOSING_CURLY_BRACE', 'valor': tokens[index]})
    return {'isValid': True, 'index': index + 1}

# Diccionario de funciones de manejo
handlers = {
    'IDENTIFIER': isAssignmentStatement,
    'DECLARATION_KEYWORD': isDeclarationStatement,
    'ELSE_KEYWORD': isElseStatement,
    'IF_KEYWORD': isIfStatement,
    'SWITCH_KEYWORD': isSwitchStatement,
    'CASE_KEYWORD': isCaseStatement,
    'DEFAULT_KEYWORD': isDefaultStatement,
    'WHILE_KEYWORD': isWhileStatement,
    'DO_KEYWORD': isDoStatement,
    'FOR_KEYWORD': isForStatement,
    'BREAK_KEYWORD': isBreakStatement,
    'CONTINUE_KEYWORD': isContinueStatement,
    'RETURN_KEYWORD': isReturnStatement,
    'CONSOLE_KEYWORD': isConsoleLogStatement,
    'ALERT_KEYWORD': isAlertStatement,
    'COMMENT': isCommentStatement,
    'CLOSING_CURLY_BRACE': isClosingCurlyBrace
}

statements = []
# Función para verificar si el codigo es correcto sintacticamente
def analizadorSintactico(code):
    result = analizadorLexico.analizarLexico(code)
    # print(result)
    if result['isValid']:
        clasifiedTokensList = clasificarTokens(result['tokensList'])
        # print(clasifiedTokensList)
        index = 0
        isValid = True
        while isValid and index < len(clasifiedTokensList):
            # print(index, len(clasifiedTokensList), clasifiedTokensList[index])
            
            if clasifiedTokensList[index]['tipo'] in handlers:
                if clasifiedTokensList[index]['tipo'] == 'ELSE_KEYWORD' and clasifiedTokensList[index + 1]['tipo'] == 'IF_KEYWORD':
                    print('ELSE IF')
                    aux = isElseIfStatement(clasifiedTokensList, index, statements)
                else:
                    print(clasifiedTokensList[index]['tipo'])
                    aux = handlers[clasifiedTokensList[index]['tipo']](clasifiedTokensList, index, statements)
                
                if aux['isValid']:
                    index = aux['index']
                else:
                    isValid = False
                    print('El código es incorrecto sintacticamente')
                    break
            else:
                isValid = False
                print('El código es incorrecto sintacticamente')
                break
        
        if isValid:
            for statement in statements:
                print(statement['tipo'], statement['valor'], '\n')
            print('El código es correcto sintacticamente')         
    else:
        print('El código contiene tokens no válidos')
    
# Ejemplo de uso
codigo_js = "var x = 10; if(x > 5){console.log(x);}"
analizadorSintactico(codigo_js)
