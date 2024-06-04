import analizadorLexico 

def isBlank (tokens):
    return len(tokens) == 0

# Verificar recursivamente si el token o el grupo de tokens es un booleano
def isCondition(tokens):
    if len(tokens) == 0:
        return False
    if tokens[0]["tipo"] == "OPENING_PARENTHESIS":
        for i in range(1, len(tokens)):
            if tokens[i]["tipo"] == "CLOSING_PARENTHESIS":
                if i == len(tokens) - 1:
                    return isCondition(tokens[1:i])
                if tokens[i+1]["valor"] == "||" or tokens[i+1]["valor"] == "&&":
                    return isCondition(tokens[1:i]) and isCondition(tokens[i+2:])
                return False
    for i in range(len(tokens)):
        if tokens[i]['valor'] == "||" or tokens[i]['valor'] == "&&":
            if i == 0 or i == len(tokens) - 1:
                return False
            return isCondition(tokens[:i]) and isCondition(tokens[i+1:])
    if len(tokens) == 1:
        return tokens[0]['tipo'] == "BOOLEAN_LITERAL"
    if tokens[0]['valor'] == '!':
        return isCondition(tokens[1:])
    if (tokens[0]['tipo'] == "IDENTIFIER" or tokens[0]['tipo'] == "NUMBER" or tokens[0]['tipo'] == "STRING" or tokens[0]['tipo'] == "BOOLEAN_LITERAL") and tokens[1]['tipo']=='COMPARISON_OPERATOR' and (tokens[2]['tipo'] == "IDENTIFIER" or tokens[2]['tipo'] == "NUMBER" or tokens[2]['tipo'] == "STRING" or tokens[2]['tipo'] == "BOOLEAN_LITERAL"):
        if len(tokens) == 3:
            return True
    return False

def isArithmeticOperation(tokens):
    if len(tokens) == 0:
        return False
    if tokens[0]["tipo"] == "OPENING_PARENTHESIS":
        for i in range(1, len(tokens)):
            if tokens[i]["tipo"] == "CLOSING_PARENTHESIS":
                if i == len(tokens) - 1:
                    return isCondition(tokens[1:i])
                if tokens[i+1]["tipo"] == "ARITHMETIC_OPERATOR":
                    return isArithmeticOperation(tokens[1:i]) and isArithmeticOperation(tokens[i+2:])
                return False
    for i in range(len(tokens)):
        if tokens[i]['tipo'] == "ARITHMETIC_OPERATOR":
            if i == 0 or i == len(tokens) - 1:
                return False
            return isArithmeticOperation(tokens[:i]) and isArithmeticOperation(tokens[i+1:])
    if len(tokens) == 1:
        return tokens[0]['tipo'] == "NUMBER" or tokens[0]['tipo'] == "IDENTIFIER" or tokens[0]['tipo'] == "STRING"
    if tokens[0]['valor'] == '-':
        return isArithmeticOperation(tokens[1:])
    return False

# Verificar si un conjunto de tokens es una asignacion
def isAssignment(tokens):
    if len(tokens) < 4:
        return False
    if tokens[0]["tipo"] == "IDENTIFIER" and tokens[1]["valor"] == "=" and (tokens[2]["tipo"] == "IDENTIFIER" or tokens[2]["tipo"] == "NUMBER" or tokens[2]["tipo"] == "STRING" or tokens[2]["tipo"] == "BOOLEAN_LITERAL" or tokens[2]["tipo"] == "ARRAY_LITERAL") and tokens[3]["valor"] == ";":
        return True
    if tokens[0]["tipo"] == "IDENTIFIER" and tokens[1]["valor"] == "=" and isCondition(tokens[2:-1]) and tokens[-1]["valor"] == ";":
        return True
    if tokens[0]["tipo"] == "IDENTIFIER" and tokens[1]["valor"] == "=" and isArithmeticOperation(tokens[2:-1]) and tokens[-1]["valor"] == ";":
        return True
    if tokens[0]["tipo"] == "IDENTIFIER" and tokens[1]["valor"] == "=" and tokens[2]["tipo"] == "NEW_KEYWORD" and tokens[3]["tipo"] == "IDENTIFIER" and tokens[4]["valor"] == "(" and tokens[-2]["valor"] == ")" and tokens[-1]["valor"] == ";":
        return True
    return False

# Verificar si un conjunto de tokens es una asignacion compuesta
def isCompoundAssignment(tokens):
    if len(tokens) < 2:
        return False
    if tokens[0]["tipo"] == "IDENTIFIER" and tokens[1]["tipo"]=='INCREMENT_DECREMENT_OPERATOR' and tokens[2]["valor"] == ";":
        return True
    if tokens[0]["tipo"] == "IDENTIFIER" and tokens[1]["tipo"]=='COMPOUND_ASSIGNMENT_OPERATOR' and (tokens[2]["tipo"] == "IDENTIFIER" or tokens[2]["tipo"] == "NUMBER") and tokens[3]["valor"] == ";":
        return True
    return False

# Verificar si un conjunto de tokens es una declaracion de variable
def isDeclaration(tokens):
    if len(tokens) < 5:
        return False
    if tokens[0]["tipo"] == "VARIABLE_DECLARATION_KEYWORD" and isAssignment(tokens[1:]):
        return True
    if tokens[0]["tipo"] == 'VARIABLE_DECLARATION_KEYWORD' and tokens[1]["tipo"] == "IDENTIFIER" and tokens[2]["valor"] == ";" :
        return True
    return False

# Verificar si un conjunto de tokens es un sentencia de console.log
def isConsoleLog(tokens):
    if len(tokens) < 6:
        return False
    if tokens[0]["valor"] == "console" and tokens[1]["valor"] == "." and tokens[2]["valor"] == "log" and tokens[3]["tipo"] == "OPENING_PARENTHESIS" and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["valor"] == ";":
        return True
    return False

# Verificar si un conjunto de tokens es una sentencia if
def isIfStatement(codigoPorLineas):
    if len(codigoPorLineas) < 5 or codigoPorLineas[0]["tipo"] != "IF_KEYWORD" or codigoPorLineas[-1]['tipo'] != "OPENING_CURLY_BRACE":
        return False
    if codigoPorLineas[0]["valor"] == "if" and codigoPorLineas[1]["tipo"] == "OPENING_PARENTHESIS" and isCondition(codigoPorLineas[2:-2]) and codigoPorLineas[-2]["tipo"] == "CLOSING_PARENTHESIS" and codigoPorLineas[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True 
    return False
        
# Verificar si un conjunto de tokens es una sentencia else
def isElseStatement(tokens):
    if len(tokens) < 3:
        return False
    if tokens[0]['tipo']=='CLOSING_CURLY_BRACE':
        tokens = tokens[1:]
    if tokens[0]["tipo"] == "ELSE_KEYWORD" and tokens[1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    return False
        
# Verificar si un conjunto de tokens es una sentencia else if
def isElseIfStatement(tokens):
    if len(tokens) < 6:
        return False
    if tokens[0]['tipo']=='CLOSING_CURLY_BRACE':
        tokens = tokens[1:]
    if tokens[0]["valor"] == "else" and tokens[1]["valor"] == "if" and tokens[2]["tipo"] == "OPENING_PARENTHESIS" and isCondition(tokens[3:-2]) and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    return False

# Verificar si un conjunto de tokens es una sentencia switch
def isSwitchStatement(tokens):
    if len(tokens) < 5:
        return False
    if tokens[0]['tipo']=='SWITCH_KEYWORD' and tokens[1]["tipo"] == "OPENING_PARENTHESIS" and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    return False

# Verificar si un conjunto de tokens es una sentencia case
def isCaseStatement(tokens):
    if len(tokens) < 3:
        return False
    if tokens[0]["tipo"] == "CASE_KEYWORD" and (tokens[1]["tipo"] == "NUMBER" or tokens[1]["tipo"] == "STRING") and tokens[2]["valor"] == ":":
        return True
    return False

# Verificar si un conjunto de tokens es una sentencia default
def isDefaultStatement(tokens):
    if len(tokens) < 2:
        return False
    if tokens[0]["tipo"] == "DEFAULT_KEYWORD" and tokens[1]["valor"] == ":":
        return True
    return False

def isClosingCurlyBraceStatement(tokens):
    return tokens[0]["tipo"] == "CLOSING_CURLY_BRACE" and len(tokens) == 1

def isBreakStatement(tokens):
    if len(tokens) < 2:
        return False
    return tokens[0]["tipo"] == "BREAK_KEYWORD" and tokens[1]["valor"] == ";"

def isWhileStatement(tokens):
    if len(tokens) < 5:
        return False
    return tokens[0]["tipo"] == "WHILE_KEYWORD" and tokens[1]["tipo"] == "OPENING_PARENTHESIS" and isCondition(tokens[2:-2]) and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE"

def isDoWhileStatement(tokens):
    if len(tokens) < 5:
        return False
    if tokens[0]['tipo']=='CLOSING_CURLY_BRACE':
        tokens = tokens[1:]
    return tokens[0]["tipo"] == "WHILE_KEYWORD" and tokens[1]["tipo"] == "OPENING_PARENTHESIS" and isCondition(tokens[2:-2]) and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "STATEMENT_TERMINATOR"
    
def isDoStatement(tokens):
    if len(tokens) < 2:
        return False
    return tokens[0]["tipo"] == "DO_KEYWORD" and tokens[1]["tipo"] == "OPENING_CURLY_BRACE"

def isForStatement(tokens):
    if len(tokens) < 15:
        return False
    if tokens[0]["tipo"] == "FOR_KEYWORD" and tokens[1]["tipo"] == "OPENING_PARENTHESIS" and isDeclaration(tokens[2: 7]) and isCondition(tokens[7: -5]) and tokens[-5]['tipo']=='STATEMENT_TERMINATOR' and tokens[-4]['tipo']=='IDENTIFIER' and tokens[-3]['tipo']=='INCREMENT_DECREMENT_OPERATOR' and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    if tokens[0]["tipo"] == "FOR_KEYWORD" and tokens[1]["tipo"] == "OPENING_PARENTHESIS" and isDeclaration(tokens[2: 7]) and isCondition(tokens[7: -6]) and tokens[-6]['tipo']=='STATEMENT_TERMINATOR' and tokens[-5]['tipo']=='IDENTIFIER' and tokens[-4]['tipo']=='COMPOUND_ASSIGNMENT_OPERATOR'and tokens[-3]['tipo']=='NUMBER' and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    
def isFunction(tokens):
    if len(tokens) < 5:
        return False
    if tokens[0]["tipo"] == "FUNCTION_KEYWORD" and tokens[1]["tipo"] == "IDENTIFIER" and tokens[2]["tipo"] == "OPENING_PARENTHESIS" and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    return False

def isThisStatement(tokens):
    if len(tokens) < 6:
        return False
    if tokens[0]["tipo"] == "THIS_KEYWORD" and tokens[1]["tipo"] == 'OBJECT_PROPERTY_ACCESSOR' and isAssignment(tokens[2:]):
        return True
    return False

def isClass(tokens):
    if len(tokens) < 3:
        return False
    if tokens[0]["tipo"] == "CLASS_KEYWORD" and tokens[1]["tipo"] == "IDENTIFIER" and tokens[2]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    return False

def isConstructor(tokens):
    if len(tokens) < 4:
        return False
    if tokens[0]["tipo"] == "CONSTRUCTOR_KEYWORD" and tokens[1]["tipo"] == "OPENING_PARENTHESIS" and tokens[-2]["tipo"] == "CLOSING_PARENTHESIS" and tokens[-1]["tipo"] == "OPENING_CURLY_BRACE":
        return True
    return False
    
lineStatementCheckers = {
    'BLANK': isBlank,
    'ASSIGNMENT': isAssignment,
    'COMPOUND_ASSIGNMENT': isCompoundAssignment,
    'DECLARATION': isDeclaration,
    'CONSOLE_LOG': isConsoleLog,
    'IF': isIfStatement,
    'ELSE': isElseStatement,
    'ELSE_IF': isElseIfStatement,
    'SWITCH': isSwitchStatement,
    'CASE': isCaseStatement,
    'DEFAULT': isDefaultStatement,
    'CLOSING_CURLY_BRACE': isClosingCurlyBraceStatement,
    'BREAK': isBreakStatement,
    'WHILE': isWhileStatement,
    'DO': isDoStatement,
    'DO_WHILE': isDoWhileStatement,
    'FOR': isForStatement,
    'FUNCTION': isFunction,
    'THIS': isThisStatement,
    'CLASS': isClass,
    'CONSTRUCTOR': isConstructor,
}

def analizarSintaxis(codigoPorLineas):
    lineasObjeto = []
    for linea in codigoPorLineas:
        tokens = []
        for token in linea:
            tokens.append(token['valor'] + ' ' )
        lineaAgregada = False
        for key in lineStatementCheckers:
            if lineStatementCheckers[key](linea):
                lineasObjeto.append({'tipo': key, 'tokens': tokens})
                lineaAgregada = True
                break
        if not lineaAgregada:
            lineasObjeto.append({'tipo': 'INVALID', 'tokens': tokens})
    
    return lineasObjeto

def generarReporteSintactico(codigoAnalizado):
    errores = ""
    tokens = ""
    numeroLinea = 1

    for linea in codigoAnalizado:
        tokens += f'{linea["tokens"]}: {linea['tipo']}\n'
        
        if linea['tipo'] == 'INVALID':
            errores += "SINTAX_ERROR: There is a syntax error in line " + str(numeroLinea) + " due to "+ str(linea['tokens']) +" not being recognized as a valid statement\n"
        
        numeroLinea += 1
        
    # Construye el reporte final
    reporteFinal = "----ERRORES SINTACTICOS----\n" + errores + "\n----LINEAS----\n" + tokens
    return reporteFinal

# codigo_js = """
# class Persona {
#   constructor(nombre, edad) {
#     this.nombre = nombre;
#     this.edad = edad;
#   }
# }

# const juan = new Persona('Juan', 30);
# let x = (1+3)*4;
# console.log(juan.nombre);
# """
# codigoPorLineas = analizadorLexico.analizarLexico(codigo_js)
# codigoAnalizado = analizarSintactico(codigoPorLineas)
# print(generarReporteSintactico(codigoAnalizado))
    
    
