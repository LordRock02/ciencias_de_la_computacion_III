import re

# Listas para los diferentes tipos de tokens en Javascript
operators = ['+', '-', '*', '=', '/', '%', '++', '--', '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '>>>', '+=', '-=', '*=', '/=', '%=', '<<=', '>>=', '>>>=', '&=', '|=', '^=']
literals = ['true', 'false', 'NULL', 'undefined', 'NaN', 'Infinity', '""', "''", "``"]
delimiters = ['(', ')', '{', '}', '[', ']', '"', "'", "`", ',', ';', ':', '.', '?', '=>']
keyWords = ['if', 'else', 'else if', 'switch', 'case', 'default', 'while', 'do', 'for', 'break', 'continue', 'return', 'function', 'var', 'let', 'const', 'new', 'delete', 'in', 'instanceof', 'typeof', 'void', 'this', 'super', 'class', 'extends', 'import', 'export', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'with', 'debugger', 'arguments', 'yield']
comments = ['//', '/*', '*/']

# Expresion regular para los identificadores
# Permite letras, digitos, guion bajo, guion medio y signo de dolar
# No puede empezar con un digito
identifierRegex = r"^[a-zA-Z_$][a-zA-Z0-9_$-]*$"

numberRegex = r'^[0-9]+(\.[0-9]+)?$'

stringRegex = r'"[^"]+"|\'[^\']+\'|`[^`]+`'

tokensRegex = r'"[^"]+"|\'[^\']+\'|`[^`]+`|\S+|"(?=\s)|\'(?=\s)|`(?=\s)'

def analizarLexico(code):

		tokens = re.findall(tokensRegex, code)
		print(tokens)

		for c in tokens:
				if any(c in lista for lista in [operators, literals, delimiters, keyWords, comments]):
						continue
				elif re.search(identifierRegex, c):
						continue
				elif re.search(stringRegex, c):
						continue
				elif re.search(numberRegex, c):
						continue
				return False
		return True 

'''print('code : ')
code = input()
print(f'resultado analisis: {analizarSintaxis(code)}')'''