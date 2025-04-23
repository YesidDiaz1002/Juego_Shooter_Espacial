import pygame
import random
import sys
import time

# Inicializar pygame
pygame.init()

# Constantes generales
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)

# Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO), flags=pygame.SWSURFACE)
pygame.display.set_caption("Shooter Espacial")
clock = pygame.time.Clock()

# Imágenes
jugador_img = pygame.Surface((50, 30))
jugador_img.fill(VERDE)

enemigo_img = pygame.Surface((40, 30))
enemigo_img.fill(ROJO)

explosion_img = pygame.Surface((40, 30))
explosion_img.fill(AMARILLO)

# Variables globales
jugador = pygame.Rect(ANCHO//2, ALTO - 60, 50, 30)
balas = []
enemigos = []
explosiones = []
puntaje = 0
record = 0
inicio_tiempo = 0

# Dificultad
frecuencia_enemigos = 30
velocidad_enemigos = 3

# Funciones
def mover_jugador(teclas, jugador):
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= 5
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += 5

def disparar(jugador):
    bala = pygame.Rect(jugador.centerx - 2, jugador.top, 5, 10)
    balas.append(bala)

def mover_balas():
    for bala in balas[:]:
        bala.y -= 5
        if bala.bottom < 0:
            balas.remove(bala)

def generar_enemigo():
    if random.randint(1, frecuencia_enemigos) == 1:
        x = random.randint(0, ANCHO - 40)
        enemigo = pygame.Rect(x, 0, 40, 30)
        enemigos.append(enemigo)

def mover_enemigos():
    for enemigo in enemigos[:]:
        enemigo.y += velocidad_enemigos
        if enemigo.top > ALTO:
            enemigos.remove(enemigo)

def colisiones():
    for enemigo in enemigos[:]:
        for bala in balas[:]:
            if enemigo.colliderect(bala):
                enemigos.remove(enemigo)
                balas.remove(bala)
                explosiones.append({"rect": enemigo.copy(), "tiempo": pygame.time.get_ticks()})
                break

def mostrar_explosiones():
    tiempo_actual = pygame.time.get_ticks()
    for ex in explosiones[:]:
        if tiempo_actual - ex["tiempo"] > 200:
            explosiones.remove(ex)
        else:
            pantalla.blit(explosion_img, ex["rect"])

def detectar_colision_jugador():
    for enemigo in enemigos:
        if jugador.colliderect(enemigo):
            return True
    return False

def mostrar_texto(texto, size, x, y, color=BLANCO):
    fuente = pygame.font.SysFont(None, size)
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

def menu_inicio():
    pantalla.fill(NEGRO)
    mostrar_texto("SHOOTER ESPACIAL", 64, ANCHO//4, ALTO//4)
    mostrar_texto("Presiona ESPACIO para comenzar", 32, ANCHO//4 + 50, ALTO//2)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False

def menu_dificultad():
    global frecuencia_enemigos, velocidad_enemigos
    opciones = ["FACIL", "MEDIO", "DIFICIL"]
    index = 0
    seleccionando = True
    while seleccionando:
        pantalla.fill(NEGRO)
        mostrar_texto("Selecciona dificultad:", 48, ANCHO//4, ALTO//4)
        for i, txt in enumerate(opciones):
            color = VERDE if i == index else BLANCO
            mostrar_texto(txt, 36, ANCHO//3, ALTO//2 + i * 50, color)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and index > 0:
                    index -= 1
                elif evento.key == pygame.K_DOWN and index < len(opciones) - 1:
                    index += 1
                elif evento.key == pygame.K_RETURN:
                    seleccionando = False

    if opciones[index] == "FACIL":
        frecuencia_enemigos = 30
        velocidad_enemigos = 2
    elif opciones[index] == "MEDIO":
        frecuencia_enemigos = 20
        velocidad_enemigos = 3
    elif opciones[index] == "DIFICIL":
        frecuencia_enemigos = 10
        velocidad_enemigos = 5

def game_over(puntaje_actual):
    global record
    pantalla.fill(NEGRO)
    if puntaje_actual > record:
        record = puntaje_actual
    mostrar_texto("¡GAME OVER!", 64, ANCHO//3, ALTO//3)
    mostrar_texto(f"Puntaje: {int(puntaje_actual)}", 32, ANCHO//3 + 30, ALTO//2 - 30)
    mostrar_texto(f"Récord: {int(record)}", 32, ANCHO//3 + 30, ALTO//2)
    mostrar_texto("Presiona R para reiniciar o ESC para salir", 28, ANCHO//5, ALTO//2 + 60)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    main()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global balas, enemigos, jugador, puntaje, inicio_tiempo, explosiones

    jugador = pygame.Rect(ANCHO//2, ALTO - 60, 50, 30)
    balas = []
    enemigos = []
    explosiones = []
    puntaje = 0
    inicio_tiempo = time.time()

    ejecutando = True
    while ejecutando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    disparar(jugador)

        teclas = pygame.key.get_pressed()
        mover_jugador(teclas, jugador)
        mover_balas()
        generar_enemigo()
        mover_enemigos()
        colisiones()

        puntaje = time.time() - inicio_tiempo

        if detectar_colision_jugador():
            game_over(puntaje)

        pantalla.fill(NEGRO)
        pantalla.blit(jugador_img, jugador)
        for bala in balas:
            pygame.draw.rect(pantalla, BLANCO, bala)
        for enemigo in enemigos:
            pantalla.blit(enemigo_img, enemigo)
        mostrar_explosiones()

        mostrar_texto(f"Puntaje: {int(puntaje)}", 28, 10, 10)
        mostrar_texto(f"Récord: {int(record)}", 28, 10, 40)

        pygame.display.flip()

# Iniciar juego
menu_inicio()
menu_dificultad()
main()
