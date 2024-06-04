import analizadorLexico, analizadorSintactico, analizadorSemantico

def compilarCodigo(codigo:str):
    # Analiza léxicamente el código
    codigoAnalizadoLexicamente = analizadorLexico.analizarLexico(codigo)
    # Generamos el Reporte Léxico
    reporteLexico = analizadorLexico.generarReporteLexico(codigoAnalizadoLexicamente)
    
    # Analiza sintácticamente el código
    codigoAnalizadoSintacticamente = analizadorSintactico.analizarSintaxis(codigoAnalizadoLexicamente)
    # Generamos el Reporte Sintáctico
    reporteSintactico = analizadorSintactico.generarReporteSintactico(codigoAnalizadoSintacticamente)
    
    # Analiza semánticamente el código
    codigoAnalizadoSemanticamente = analizadorSemantico.analizarSemantico(codigoAnalizadoLexicamente)
    # Generamos el Reporte Semántico
    reporteSemantico = analizadorSemantico.generarReporteSemantico(codigoAnalizadoSemanticamente)
    
    return {'lexico':reporteLexico, 'sintactico':reporteSintactico, 'semantico':reporteSemantico}

# Ejemplos
if_example = """
let x = 10;
if (x > 10) {
  console.log('X es mayor a 10');
} else if (x < 10){
    console.log('X es menor a 10');
} else {
    console.log('X es igual a 10');
}
"""

class_example = """
class Persona {
  constructor(nombre, edad) {
    this.nombre = nombre;
    this.edad = edad;
  }
}
const juan = new Persona('Juan', 30);
console.log(juan.nombre);
"""

for_example = """
for (let i = 0; i < 10; i++) {
  if (i % 2 === 0) {
    console.log(i);
  }
}
"""

function_example = """
function sumar(a, b) {
  return a + b;
}
console.log(sumar(1, 2));
console.log(sumar(3, 4));
console.log(sumar(5, 6));
"""

declare_example = """
let x = 10;
let y = 20;
let z = x + y;
console.log(z);
"""

switch_example = """
let x = 10;
switch (x) {
  case 10:
    console.log('X es 10');
    break;
  case 20:
    console.log('X es 20');
    break;
  default:
    console.log('X no es 10 ni 20');
}
"""

# print(compilarCodigo(if_example)['lexico'])
# print(compilarCodigo(if_example)['sintactico'])
# print(compilarCodigo(if_example)['semantico'])

# print(compilarCodigo(class_example)['lexico'])
# print(compilarCodigo(class_example)['sintactico'])
# print(compilarCodigo(class_example)['semantico'])

# print(compilarCodigo(for_example)['lexico'])
# print(compilarCodigo(for_example)['sintactico'])
# print(compilarCodigo(for_example)['semantico'])

# print(compilarCodigo(function_example)['lexico'])
# print(compilarCodigo(function_example)['sintactico'])
# print(compilarCodigo(function_example)['semantico'])

# print(compilarCodigo(declare_example)['lexico'])
# print(compilarCodigo(declare_example)['sintactico'])
# print(compilarCodigo(declare_example)['semantico'])
