import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Disparar")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)

# Velocidades
VELOCIDAD_JUGADOR = 5
VELOCIDAD_BALAS = 7
VELOCIDAD_ENEMIGOS = 3

# Crear la nave del jugador
jugador = pygame.Rect(ANCHO//2 - 25, ALTO - 50, 50, 50)

# Crear la lista de balas
balas = []

# Crear enemigos
enemigos = [{
    'rect': pygame.Rect(random.randint(0, ANCHO-50), random.randint(-100, -40), 50, 50),
    'color': NEGRO,
    'golpes': 0
} for _ in range(5)]

# Función para dibujar el jugador
def dibujar_jugador():
    pygame.draw.rect(pantalla, AZUL, jugador)

# Función para dibujar las balas
def dibujar_balas():
    for bala in balas:
        pygame.draw.rect(pantalla, ROJO, bala)

# Función para dibujar los enemigos
def dibujar_enemigos():
    for enemigo in enemigos:
        pygame.draw.rect(pantalla, enemigo['color'], enemigo['rect'])

# Función para mover las balas
def mover_balas():
    global balas
    for bala in balas:
        bala.y -= VELOCIDAD_BALAS
        if bala.y < 0:
            balas.remove(bala)

# Función para mover los enemigos
def mover_enemigos():
    for enemigo in enemigos:
        enemigo['rect'].y += VELOCIDAD_ENEMIGOS
        if enemigo['rect'].y > ALTO:
            enemigo['rect'].y = random.randint(-100, -40)
            enemigo['rect'].x = random.randint(0, ANCHO-50)

# Función para comprobar colisiones
def comprobar_colisiones():
    global enemigos, balas
    for bala in balas:
        for enemigo in enemigos:
            if bala.colliderect(enemigo['rect']):
                enemigo['golpes'] += 1
                balas.remove(bala)

                # Cambiar color del enemigo según la cantidad de golpes
                if enemigo['golpes'] == 1:
                    enemigo['color'] = VERDE
                elif enemigo['golpes'] == 2:
                    enemigo['color'] = AMARILLO
                elif enemigo['golpes'] >= 3:
                    enemigos.remove(enemigo)
                    # Crear un nuevo enemigo después de desaparecer
                    enemigos.append({
                        'rect': pygame.Rect(random.randint(0, ANCHO-50), random.randint(-100, -40), 50, 50),
                        'color': NEGRO,
                        'golpes': 0
                    })

# Función para manejar las teclas
def manejar_teclas():
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= VELOCIDAD_JUGADOR
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += VELOCIDAD_JUGADOR
    if teclas[pygame.K_SPACE]:
        balas.append(pygame.Rect(jugador.centerx - 5, jugador.top, 10, 20))

# Función para mostrar el puntaje
def mostrar_puntaje(puntaje):
    fuente = pygame.font.SysFont('Arial', 30)
    texto = fuente.render(f'Puntaje: {puntaje}', True, BLANCO)
    pantalla.blit(texto, (10, 10))

# Función principal del juego
def jugar():
    puntaje = 0
    reloj = pygame.time.Clock()
    corriendo = True
    while corriendo:
        pantalla.fill(NEGRO)

        # Comprobar los eventos (como cerrar la ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Mover y dibujar elementos
        manejar_teclas()
        mover_balas()
        mover_enemigos()
        comprobar_colisiones()

        # Dibujar todo en la pantalla
        dibujar_jugador()
        dibujar_balas()
        dibujar_enemigos()
        mostrar_puntaje(puntaje)

        # Aumentar puntaje por cada enemigo eliminado
        puntaje = 5 * (5 - len(enemigos))  # El puntaje depende de los enemigos restantes

        # Actualizar la pantalla
        pygame.display.update()

        # Controlar la velocidad de cuadros
        reloj.tick(60)

    pygame.quit()

# Iniciar el juego
if __name__ == "__main__":
    jugar()
