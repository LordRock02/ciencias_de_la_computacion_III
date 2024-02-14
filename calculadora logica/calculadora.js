function verificarProposicion(proposicion) {
    // Expresiones regulares para variables, operadores lógicos y paréntesis
    var variableRegex = /[a-z]/;
    var operadorRegex = /[&|!]/;
    var parentesisRegex = /[()]/;

    // Contadores para verificar la validez de los paréntesis
    var parentesisAbiertos = 0;
    var parentesisCerrados = 0;

    var esperaVariable = false

    // Verificar cada caracter de la proposición
    for (var i = 0; i < proposicion.length; i++) {
        var caracter = proposicion[i];
        if (variableRegex.test(caracter)) {
            // Es una variable, continuar verificando
            esperaVariable = false
            continue;
        } else if (operadorRegex.test(caracter)) {
            // Es un operador lógico, continuar verificando
            esperaVariable = true
            continue;
        } else if (parentesisRegex.test(caracter)) {
            // Es un paréntesis, verificar si está balanceado
            if (caracter === '(') {
                parentesisAbiertos++;
            } else if (caracter === ')') {
                parentesisCerrados++;
            }
        } else if (caracter == ' ') {
            continue;
        } else {
            // Caracter no reconocido, la proposición no está bien escrita
            return false;
        }
    }

    if(esperaVariable){
        return false
    }

    // Verificar que el número de paréntesis abiertos y cerrados sea el mismo
    if (parentesisAbiertos !== parentesisCerrados) {
        return false;
    }

    // La proposición está bien escrita
    return true;
}


// Ejemplo de uso:
var proposicion = "(a & b) | (c & !d)()";
if (verificarProposicion(proposicion)) {
    console.log("La proposición está bien escrita.");
} else {
    console.log("La proposición no está bien escrita.");
}