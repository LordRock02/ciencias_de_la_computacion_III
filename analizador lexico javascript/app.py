from flask import Flask, render_template
from analizadorLexico import analizarLexico
from analizadorLexico import generarReporteLexico

app = Flask(__name__)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/analizar-lexico/<code>', methods=['POST'])
def analizarLexicoEndpoint(code:str):
	print(f'input : {code}')
	'''LLAMADA A FUNCION analizarLexico(input)'''
	resultado = analizarLexico(code)
	reporte = generarReporteLexico(resultado)
	print(f'este es el resultado{resultado}')
	print(f'reporte lexico {generarReporteLexico(resultado)}')
	return {'result':resultado, 'reporte': reporte}

if __name__ == '__main__':
		app.run(debug=True)