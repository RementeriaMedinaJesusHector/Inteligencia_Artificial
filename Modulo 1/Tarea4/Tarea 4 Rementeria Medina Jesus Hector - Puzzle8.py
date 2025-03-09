import random
import time
from collections import deque
from copy import deepcopy
import heapq

#Estado del juego
class Estado:
    def __init__(self, tablero, movimientos=None, costo=0, heuristica=0):
        self.tablero = tablero
        self.movimientos = movimientos or []
        #Número de movimientos realizados
        self.costo = costo
        #Estimación de movimientos restantes
        self.heuristica = heuristica

    def __eq__(self, other):
        return self.tablero == other.tablero

    def __hash__(self):
        return hash(str(self.tablero))

    def __lt__(self, other):
        return (self.costo + self.heuristica) < (other.costo + other.heuristica)

#Genrar un tablero aleatorio
def generar_tablero_aleatorio():
    tablero = [i for i in range(9)]
    while True:
        random.shuffle(tablero)
        matriz = [tablero[i:i + 3] for i in range(0, 9, 3)]
        if es_resoluble(matriz):
            return matriz

#Comprobar si el tablero tiene solucion
def es_resoluble(tablero):
    plano = sum(tablero, [])
    inversions = sum(
        1 for i in range(len(plano)) for j in range(i + 1, len(plano)) if plano[i] and plano[j] and plano[i] > plano[j])
    return inversions % 2 == 0

#Algoritmo distancia manhattan
def distancia_manhattan(tablero, objetivo):
    distancia = 0
    #Recorrer el tablero
    for i in range(3):
        for j in range(3):
            #Ignorar el 0
            if tablero[i][j] != 0:
                #encontrar posicion correcta
                fila_obj, col_obj = divmod(objetivo.index(tablero[i][j]), 3)
                #calcular distancia
                distancia += abs(fila_obj - i) + abs(col_obj - j)
    return distancia

def generar_sucesores(estado, objetivo):
    #Estados generados
    sucesores = []
    #Movimientos disponibles
    movimientos = [(0, 1, 'derecha'), (1, 0, 'abajo'), (0, -1, 'izquierda'), (-1, 0, 'arriba')]
    #Posicion del 0
    fila, col = next((i, j) for i, fila in enumerate(estado.tablero) for j, val in enumerate(fila) if val == 0)

    #generar estados
    for df, dc, direccion in movimientos:
        nueva_fila, nueva_col = fila + df, col + dc
        #verificar si es valido
        if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
            nuevo_tablero = deepcopy(estado.tablero)
            nuevo_tablero[fila][col], nuevo_tablero[nueva_fila][nueva_col] = nuevo_tablero[nueva_fila][nueva_col], \
            nuevo_tablero[fila][col]
            #agregar movimiento a la lista
            nuevos_movimientos = estado.movimientos + [direccion]
            #calcular distancia del nuevo estado
            heuristica = distancia_manhattan(nuevo_tablero, sum(objetivo, []))
            #nuevo objeto estado
            sucesores.append(Estado(nuevo_tablero, nuevos_movimientos, estado.costo + 1, heuristica))

    return sucesores

#Algoritmo de A*
def a_star(inicio, objetivo):
    #Inicia el temporizador
    inicio_tiempo = time.time()
    #Cola de proridad
    prioridad = []
    #
    estado_inicial = Estado(inicio, heuristica=distancia_manhattan(inicio, sum(objetivo, [])))
    #Agregar estado inicial a la cola
    heapq.heappush(prioridad, estado_inicial)
    #Estados visitados
    visitados = set()

    #
    while prioridad:
        estado_actual = heapq.heappop(prioridad)

        if estado_actual.tablero == objetivo:
            fin_tiempo = time.time()
            tiempo_transcurrido = fin_tiempo - inicio_tiempo
            return estado_actual.movimientos, tiempo_transcurrido

        #Marcar estado como visitado
        visitados.add(estado_actual)

        #Posibles movimientos
        for sucesor in generar_sucesores(estado_actual, objetivo):
            if sucesor not in visitados:
                heapq.heappush(prioridad, sucesor)

    #No se encontro solucion
    return None, None

#Imrpimir tablero actual
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(map(str, fila)))
    print()

def jugar_puzzle_8():
    #Generar un tablero aleatorio
    inicio = generar_tablero_aleatorio()

    #Tablero inicial fijo
    #inicio = [
        #[5, 1, 3],
        #[7, 2, 8],
        #[4, 0, 6]
    #]

    #Objetivo final del tablero
    objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    #Imprmir el tablero inicial
    print("Estado inicial:")
    imprimir_tablero(inicio)

    #Buscar solucion
    solucion, tiempo_transcurrido = a_star(inicio, objetivo)

    #Imprimir cantidad de movimientos y tiempo
    if solucion:
    #Imprimir los movimientos realizados y el estado de los tableros
        estado_actual = deepcopy(inicio)
        #Imprimir los movimientos realizados
        for i, movimiento in enumerate(solucion, 1):
            fila, col = next((i, j) for i, fila in enumerate(estado_actual) for j, val in enumerate(fila) if val == 0)
            if movimiento == 'derecha':
                estado_actual[fila][col], estado_actual[fila][col + 1] = estado_actual[fila][col + 1], \
                estado_actual[fila][col]
            elif movimiento == 'izquierda':
                estado_actual[fila][col], estado_actual[fila][col - 1] = estado_actual[fila][col - 1], \
                estado_actual[fila][col]
            elif movimiento == 'arriba':
                estado_actual[fila][col], estado_actual[fila - 1][col] = estado_actual[fila - 1][col], \
                estado_actual[fila][col]
            elif movimiento == 'abajo':
                estado_actual[fila][col], estado_actual[fila + 1][col] = estado_actual[fila + 1][col], \
                estado_actual[fila][col]
            print(f"Movimiento {i}: {movimiento}")
            imprimir_tablero(estado_actual)
        print(f"Solución encontrada en {len(solucion)} movimientos.")
        print(f"Tiempo transcurrido: {tiempo_transcurrido:.4f} segundos.")

    else: print("No se encontró solución.")

if __name__ == "__main__":
    jugar_puzzle_8()
