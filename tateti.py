# Función para imprimir el tablero
def imprimir_tablero(tablero):
    print("---------")
    for fila in tablero:
        print("|", " | ".join(fila), "|")
        print("---------")

# Función para verificar si un jugador ha ganado
def verificar_ganador(tablero, jugador):
    # Revisar filas
    for fila in tablero:
        if fila.count(jugador) == 3:
            return True
    # Revisar columnas
    for i in range(3):
        if all(tablero[j][i] == jugador for j in range(3)):
            return True
    # Revisar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True
    return False

# Función para verificar si el tablero está lleno (empate)
def tablero_lleno(tablero):
    for fila in tablero:
        if " " in fila:
            return False
    return True

# Función principal del juego
def jugar():
    # Inicializar el tablero
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    jugadores = ["X", "O"]
    turno = 0
    
    while True:
        # Mostrar el tablero
        imprimir_tablero(tablero)
        
        # Solicitar la jugada del jugador
        print(f"Turno del jugador {jugadores[turno % 2]}: ")
        fila = int(input("Ingresa la fila (0-2): "))
        columna = int(input("Ingresa la columna (0-2): "))
        
        # Verificar si la casilla está vacía
        if tablero[fila][columna] != " ":
            print("¡Esa casilla ya está ocupada! Intenta de nuevo.")
            continue
        
        # Colocar la jugada
        tablero[fila][columna] = jugadores[turno % 2]
        
        # Verificar si el jugador actual ha ganado
        if verificar_ganador(tablero, jugadores[turno % 2]):
            imprimir_tablero(tablero)
            print(f"¡El jugador {jugadores[turno % 2]} ha ganado!")
            break
        
        # Verificar si hay empate
        if tablero_lleno(tablero):
            imprimir_tablero(tablero)
            print("¡El juego ha terminado en empate!")
            break
        
        # Cambiar de turno
        turno += 1

# Iniciar el juego
if __name__ == "__main__":
    jugar()
