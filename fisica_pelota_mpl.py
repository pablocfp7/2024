import matplotlib.pyplot as plt

# Parámetros físicos
gravedad = 9.81  # Aceleración debida a la gravedad (m/s^2)
coef_rebote = 0.9  # Coeficiente de restitución (reduce la velocidad en cada rebote)
coef_friccion = 0.01  # Factor que simula la fricción o resistencia al aire
altura_inicial = 10  # Altura inicial en metros

# Variables de simulación
posicion = altura_inicial  # Posición inicial (en metros)
velocidad = 0  # Velocidad inicial
tiempo = 0  # Tiempo inicial
dt = 0.01  # Intervalo de tiempo (segundos)

# Listas para graficar el movimiento
posiciones = []
tiempos = []

# Simulación del movimiento
while posicion > 0.01:  # La pelota se detendrá cuando la posición sea casi 0
    # Actualizamos la velocidad debido a la gravedad
    velocidad += gravedad * dt
    
    # Actualizamos la posición
    posicion -= velocidad * dt

    # Simulamos el rebote cuando la pelota llega al suelo
    if posicion <= 0:
        # Rebote: la pelota pierde energía según el coeficiente de restitución
        velocidad = -velocidad * coef_rebote
        
        # Si la velocidad es pequeña, se reduce por fricción
        if velocidad < 0:
            velocidad -= coef_friccion
    
    # Almacenamos la posición y el tiempo para graficar después
    tiempos.append(tiempo)
    posiciones.append(posicion)

    # Incrementamos el tiempo
    tiempo += dt

# Graficar la trayectoria de la pelota
plt.plot(tiempos, posiciones)
plt.title('Simulación del Rebote de la Pelota')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (m)')
plt.grid(True)
plt.show()
