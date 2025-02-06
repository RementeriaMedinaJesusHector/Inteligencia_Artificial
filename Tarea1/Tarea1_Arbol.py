class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar(nodo.derecha, valor)
        return nodo

    def vacio(self):
        return self.raiz is None

    def imprimir_arbol(self):
        self._imprimir_arbol(self.raiz)
        print()

    def _imprimir_arbol(self, nodo):
        if nodo:
            self._imprimir_arbol(nodo.izquierda)
            print(nodo.valor, end=" ")
            self._imprimir_arbol(nodo.derecha)

    def buscar_nodo(self, valor):
        return self._buscar_nodo(self.raiz, valor)

    def _buscar_nodo(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self._buscar_nodo(nodo.izquierda, valor)
        return self._buscar_nodo(nodo.derecha, valor)

if __name__ == "__main__":
    mi_arbol = Arbol()

    mi_arbol.insertar(9)
    mi_arbol.insertar(6)
    mi_arbol.insertar(2)
    mi_arbol.insertar(0)
    mi_arbol.insertar(10)

    mi_arbol.imprimir_arbol()

    nodo_encontrado = mi_arbol.buscar_nodo(6)
    if nodo_encontrado:
        print(f"Nodo {6} encontrado en el árbol.")
    else:
        print(f"Nodo {6} no encontrado en el árbol.")
