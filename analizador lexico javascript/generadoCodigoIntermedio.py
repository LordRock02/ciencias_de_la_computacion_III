class GeneradorCodigoIntermedio:
    def __init__(self):
        self.temp_counter = 0
        self.codigo_intermedio = []

    def nuevo_temporal(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def generar(self, nodo):
        if nodo is None:
            return None
        
        if nodo.tipo == 'NUMERO' or nodo.tipo == 'IDENTIFICADOR':
            return nodo.valor
        
        elif nodo.tipo == 'OPERACION':
            izq = self.generar(nodo.izquierda)
            der = self.generar(nodo.derecha)
            temp = self.nuevo_temporal()
            self.codigo_intermedio.append(f"{temp} = {izq} {nodo.operador} {der}")
            return temp

        elif nodo.tipo == 'ASIGNACION':
            temp = self.generar(nodo.valor)
            self.codigo_intermedio.append(f"{nodo.variable} = {temp}")
            return nodo.variable
        
        # Agregar más casos según sea necesario para otros tipos de nodos

    def obtener_codigo_intermedio(self):
        return self.codigo_intermedio

# Ejemplo de uso
generador = GeneradorCodigoIntermedio()
arbol_sintactico = ...  # Árbol sintáctico generado por el analizador sintáctico
generador.generar(arbol_sintactico)
codigo_intermedio = generador.obtener_codigo_intermedio()

# Imprimir o guardar el código intermedio
for instruccion in codigo_intermedio:
    print(instruccion)