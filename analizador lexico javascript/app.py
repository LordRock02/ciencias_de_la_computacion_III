from flask import Flask, render_template
from analizadorLexico import analizarLexico, generarReporteLexico
from analizadorSemantico import analizarSemantico, generarReporteSemantico
from analizadorSintactico import analizarSintaxis, generarReporteSintactico

app = Flask(__name__)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/analizar-lexico/<code>', methods=['POST'])
def analizarLexicoEndpoint(code:str):
	print(f'input : {code}')
	'''LLAMADA A FUNCION analizarLexico(input)'''
	resultado = analizarLexico(code)
	resultado2 = analizarSintaxis(resultado)
	resultado3 = analizarSemantico(resultado2)
	reporte = generarReporteLexico(resultado)
	reporte2 = generarReporteSintactico(resultado2)
	reporte3 = generarReporteSemantico(resultado3)
	print(f'este es el resultado{resultado}')
	print(f'reporte lexico {reporte}')
	print(f'reporte sintactico {reporte2}')
	print(f'reporte semantico {reporte3}')
	return {'result':resultado, 'reporteLexico': reporte, 'reporteSintactico' : reporte2, 'reporteSemantico': reporte3}

if __name__ == '__main__':
		app.run(debug=True)