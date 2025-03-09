from collections import defaultdict
import random

# Historial de jugadas del usuario
historial = defaultdict(int)

opciones = ["piedra", "papel", "tijeras"]

def predecir_jugada():
    if not historial:
        return random.choice(opciones)  # Primera vez es aleatorio
    return max(historial, key=historial.get)  # Predice la jugada más frecuente del usuario

def jugar():
    victorias_ia = 0
    victorias_usuario = 0

    while victorias_ia < 2 and victorias_usuario < 2:
        eleccion_usuario = input("Elige piedra, papel o tijeras: ").lower()

        if eleccion_usuario not in opciones:
            print("Elección inválida, intenta de nuevo.")
            continue

        eleccion_ia = predecir_jugada()
        print(f"IA eligió: {eleccion_ia}")

        # Almacenar la elección del usuario para futuras predicciones
        historial[eleccion_usuario] += 1

        if eleccion_usuario == eleccion_ia:
            print("¡Empate!")
        elif (eleccion_usuario == "piedra" and eleccion_ia == "tijeras") or \
                (eleccion_usuario == "papel" and eleccion_ia == "piedra") or \
                (eleccion_usuario == "tijeras" and eleccion_ia == "papel"):
            print("¡Ganaste esta ronda!")
            victorias_usuario += 1
        else:
            print("¡La IA gana esta ronda!")
            victorias_ia += 1

        print(f"Marcador: Usuario {victorias_usuario} - {victorias_ia} IA")

    if victorias_usuario == 2:
        print("¡Felicidades! Ganaste.")
    else:
        print("La IA ha ganado.")

if __name__ == "__main__":
 jugar()