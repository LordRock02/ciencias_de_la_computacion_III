// Listas para los diferentes tipos de tokens en Javascript
operators = ['+', '-', '*', '/', '%', '++', '--', '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '>>>', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '>>>=', '&=', '|=', '^=']
literals = ['true', 'false', 'NULL', 'undefined', 'NaN', 'Infinity']
delimiters = ['(', ')', '{', '}', '[', ']', ',', ';', ':', '.', '?', '=>']
keyWords = ['if', 'else', 'else if', 'switch', 'case', 'default', 'while', 'do', 'for', 'break', 'continue', 'return', 'function', 'var', 'let', 'const', 'new', 'delete', 'in', 'instanceof', 'typeof', 'void', 'this', 'super', 'class', 'extends', 'import', 'export', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'with', 'debugger', 'arguments', 'yield']
comments = ['//', '/*', '*/']

// Expresion regular para los identificadores
// Permite letras, digitos, guion bajo, guion medio y signo de dolar
// No puede empezar con un digito

identifierRegex = /^[a-zA-Z_$][a-zA-Z0-9_$-]*$/

// Prueba del regex
alert(identifierRegex.test('hola/'))