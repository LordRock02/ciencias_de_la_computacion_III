import analizadorSintactico
import analizadorLexico

declaredVariables = []

def analizarSemantico (codigoAnalizado):
    lineasObjeto = []
    for linea in codigoAnalizado:
        if analizadorSintactico.isDeclaration(linea):
            if linea[1]['valor'] in declaredVariables:
                lineasObjeto.append({'nombre': linea[1]['valor'], 'accion': 'REDECLARED', 'isValid': False})
            else:
                declaredVariables.append({'nombre': linea[1]['valor'], 'tipo': linea[0]['valor']})
                lineasObjeto.append({'nombre': linea[1]['valor'], 'accion': 'DECLARED', 'isValid': True})
        
        elif analizadorSintactico.isAssignment(linea):
            if linea[0]['valor'] not in declaredVariables:
                lineasObjeto.append({'nombre': linea[0]['valor'], 'accion': 'UNDECLARED_VARIABLE', 'isValid': False})
            else:
                if declaredVariables[linea[0]['tipo']] == 'const':
                    lineasObjeto.append({'nombre': linea[0]['valor'], 'accion': 'ASSIGNED_CONST', 'isValid': False})
                lineasObjeto.append({'nombre': linea[0]['valor'], 'accion': 'ASSIGNED', 'isValid': True})
        
        elif analizadorSintactico.isThisStatement(linea):
            lineasObjeto.append({'nombre': linea[0]['valor']+linea[1]['valor']+linea[2]['valor'], 'accion': 'USED', 'isValid': True})

    return lineasObjeto

def generarReporteSemantico(codigoAnalizado):
    errores = ""
    tokens = ""
    numeroLinea = 1
    errors = []

    for linea in codigoAnalizado:
        tokens += f'{linea["nombre"]}: {linea["accion"]}\n'
        
        if not linea['isValid']:
            errores += "SEMANTIC_ERROR: There is a semantic error in line " + str(numeroLinea) + " due to variable "+ str(linea['nombre']) +" not being used correctly \n"
            errors.append("SEMANTIC_ERROR: There is a semantic error in line " + str(numeroLinea) + " due to variable "+ str(linea['nombre']) +" not being used correctly")
        numeroLinea += 1
        
    # Construye el reporte final
    reporteFinal = "----ERRORES SEMANTICOS----\n" + errores + "\n----ACCIONES----\n" + tokens
    print(f'reporte semantico ------------ {reporteFinal}')
    return errors

# # Función de prueba
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
# codigoAnalizado = analizarSemantico(codigoPorLineas)
# print(codigoAnalizado)
# print(generarReporteSemantico(codigoAnalizado))

