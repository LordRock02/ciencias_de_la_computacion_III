from flask import Flask, render_template
from analizadorLexico import analizarLexico

app = Flask(__name__)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/analizar-lexico/<code>', methods=['POST'])
def analizarLexicoEndpoint(code:str):
	print(f'input : {code}')
	'''LLAMADA A FUNCION analizarLexico(input)'''
	resultado:bool = analizarLexico(code)
	return {'result':resultado}

if __name__ == '__main__':
		app.run(debug=True)
