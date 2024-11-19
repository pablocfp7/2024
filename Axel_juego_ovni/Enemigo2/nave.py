import pygame
import random
import mixer
# Inicializar Pygame
pygame.init()


#Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naves")

# Cargar imagen de fondo
fondo = pygame.image.load('fondo.jpg').convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))  # Escalar al tamaño de la ventana

# Variables para el movimiento del fondo
fondo_y1 = 1
fondo_y2 = -HEIGHT  # Segunda copia del fondo, justo debajo
fondo_speed = 3  # Velocidad del movimiento del fondo

#Agregar musica
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

class Nave:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load('nave-espacial.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

    def mover(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        # Limitar el movimiento dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)

#Clase proyectil (bala,arma,misil)
class Proyectil:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load('misil.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

    def mover(self):
        self.rect.y -= self.velocidad

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)


#Creamos la primera clase de Enemigos
class Enemigo:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load('extraterrestre.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

    def mover(self):
        self.rect.y += self.velocidad  # Mover hacia abajo

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)


#Creamos la segunda clase de enemigo
class Enemigo2:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load('meteorito.png').convert_alpha()  # Imagen diferente para el segundo enemigo
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad

    def mover(self):
        self.rect.y += self.velocidad  # Mover hacia abajo
        self.rect.x += random.choice([-1, 1])  # Movimiento lateral aleatorio

    def dibujar(self, surface):
        surface.blit(self.image, self.rect.topleft)



# Crear la nave
nave = Nave(WIDTH // 2, HEIGHT // 2, 5)
proyectiles = []
enemigos = []
proyectil_velocidad = 10

# Temporizador para crear enemigos
crear_enemigos_intervalo = 1000  # Cada 1 segundo
pygame.time.set_timer(pygame.USEREVENT, crear_enemigos_intervalo)  # Generar evento

# Inicializar puntaje y contador de enemigos perdidos
puntaje = 0
enemigos_perdidos = 0
fuente = pygame.font.Font(None, 36)  # Fuente para el puntaje


def generar_enemigo():
    while True:
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-50, -10)
        velocidad_aleatoria = random.randint(1, 5)  # Velocidad aleatoria entre 1 y 5

        # Elegir aleatoriamente entre Enemigo y Enemigo2
        if random.choice([True, False]):
            nuevo_enemigo = Enemigo(x, y, velocidad_aleatoria)
        else:
            nuevo_enemigo = Enemigo2(x, y, velocidad_aleatoria)

        # Verificar si el nuevo enemigo colisiona con algún enemigo existente
        colision = False
        for enemigo in enemigos:
            if nuevo_enemigo.rect.colliderect(enemigo.rect):
                colision = True
                break

        if not colision:
            return nuevo_enemigo #Retornar el enemigo si no hay colision


# Bucle principal
running = True
while running:
    # Limpiar la pantalla
    screen.fill((0, 0, 0))

    # Mover el fondo hacia arriba
    fondo_y1 += fondo_speed
    fondo_y2 += fondo_speed

    # Reposicionar el fondo si sale de la pantalla
    if fondo_y1 >= HEIGHT:
        fondo_y1 = fondo_y2 - HEIGHT
    if fondo_y2 >= HEIGHT:
        fondo_y2 = fondo_y1 - HEIGHT

    # Dibujar el fondo
    screen.blit(fondo, (0, fondo_y1))
    screen.blit(fondo, (0, fondo_y2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nuevo_proyectil = Proyectil(nave.rect.centerx, nave.rect.top, proyectil_velocidad)
                proyectiles.append(nuevo_proyectil)
        if event.type == pygame.USEREVENT:  # Evento para crear enemigos
            for _ in range(random.randint(1, 3)):  # Generar entre 1 y 3 enemigos
                enemigo = generar_enemigo()
                enemigos.append(enemigo)

    keys = pygame.key.get_pressed()

    # Mover la nave
    nave.mover(keys)

    # Mover los proyectiles
    for proyectil in proyectiles[:]:
        proyectil.mover()
        if proyectil.rect.bottom < 0:
            proyectiles.remove(proyectil)

    # Mover enemigos
    for enemigo in enemigos[:]:
        enemigo.mover()
        if enemigo.rect.top > HEIGHT:
            enemigos.remove(enemigo)
            enemigos_perdidos += 1
            if enemigos_perdidos > 10:
                print("¡Juego Terminado! Se han perdido más de 10 enemigos.")
                running = False

    # Detección de colisiones entre proyectiles y enemigos
    for proyectil in proyectiles[:]:
        for enemigo in enemigos[:]:
            if proyectil.rect.colliderect(enemigo.rect):
                proyectiles.remove(proyectil)
                enemigos.remove(enemigo)
                puntaje += 1
                break

    # Detección de colisiones entre la nave y enemigos
    for enemigo in enemigos:
        if enemigo.rect.colliderect(nave.rect):
            print("¡Juego Terminado!")
            running = False

    # Dibujar la nave
    nave.dibujar(screen)

    # Dibujar los proyectiles
    for proyectil in proyectiles:
        proyectil.dibujar(screen)

    # Dibujar los enemigos
    for enemigo in enemigos:
        enemigo.dibujar(screen)

    # Mostrar puntaje
    texto_puntaje = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    screen.blit(texto_puntaje, (10, 10))

    # Mostrar enemigos perdidos
    texto_enemigos_perdidos = fuente.render(f'Enemigos Perdidos: {enemigos_perdidos}', True, (255, 255, 255))
    screen.blit(texto_enemigos_perdidos, (10, 40))

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)


# Mostrar mensaje de fin de juego
def mostrar_mensaje_fin():
    screen.fill((0, 0, 0))  # Limpiar la pantalla
    texto_fin = fuente.render('¡Juego Terminado!', True, (255, 0, 0))
    texto_puntaje_final = fuente.render(f'Puntaje Final: {puntaje}', True, (255, 255, 255))
    texto_enemigos_perdidos_final = fuente.render(f'Enemigos Perdidos: {enemigos_perdidos}', True, (255, 255, 255))

    # Posicionar el texto en la pantalla
    screen.blit(texto_fin, (WIDTH // 2 - texto_fin.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(texto_puntaje_final, (WIDTH // 2 - texto_puntaje_final.get_width() // 2, HEIGHT // 2))
    screen.blit(texto_enemigos_perdidos_final,
                (WIDTH // 2 - texto_enemigos_perdidos_final.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.delay(3000)  # Esperar 3 segundos


# Llamar a la función de fin de juego antes de salir
mostrar_mensaje_fin()

# Salir de Pygame

pygame.quit()