import pygame
import time
import random

# Inicializar pygame
pygame.init()

# Definir colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)

# Dimensiones de la ventana del juego
ancho = 800
alto = 600

# Crear la ventana del juego
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Viborita')

# Tamaño de la serpiente y velocidad
tamaño_bloque = 20
velocidad = 7

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Cargar imágenes
imagen_fondo = pygame.image.load('img/background.jpg')
imagen_serpiente = pygame.image.load('img/snake.png')
imagen_comida = pygame.image.load('img/food.png')

# Redimensionar imágenes
imagen_fondo = pygame.transform.scale(imagen_fondo, (ancho, alto))
imagen_serpiente = pygame.transform.scale(imagen_serpiente, (tamaño_bloque, tamaño_bloque))
imagen_comida = pygame.transform.scale(imagen_comida, (tamaño_bloque, tamaño_bloque))

# Fuente para el puntaje y el menú
fuente = pygame.font.SysFont("comicsansms", 35)

# Cargar música
pygame.mixer.music.load('music/musica.mp3')
pygame.mixer.music.play(-1)  # Reproducir en bucle

# Función para mostrar el puntaje
def mostrar_puntaje(puntaje):
    valor = fuente.render("Puntaje: " + str(puntaje), True, blanco)
    pantalla.blit(valor, [0, 0])

# Función para mostrar el menú cuando se pierde
def mostrar_menu():
    pantalla.fill(negro)
    mensaje = fuente.render("Perdiste! Haz clic en Reiniciar o Salir", True, rojo)
    pantalla.blit(mensaje, [ancho / 6, alto / 3])

    # Crear botones
    boton_reiniciar = pygame.Rect(ancho / 4, alto / 2, 100, 50)
    boton_salir = pygame.Rect(ancho / 2, alto / 2, 100, 50)

    # Dibujar botones
    pygame.draw.rect(pantalla, blanco, boton_reiniciar)
    pygame.draw.rect(pantalla, blanco, boton_salir)

    texto_reiniciar = fuente.render("Reiniciar", True, negro)
    texto_salir = fuente.render("Salir", True, negro)
    
    pantalla.blit(texto_reiniciar, (ancho / 4 + 5, alto / 2 + 10))
    pantalla.blit(texto_salir, (ancho / 2 + 20, alto / 2 + 10))

    pygame.display.update()

    return boton_reiniciar, boton_salir

# Función principal del juego
def juego():
    game_over = False
    game_close = False

    # Posición inicial de la serpiente
    x = ancho / 2
    y = alto / 2

    # Cambios en la posición
    x_cambio = 0
    y_cambio = 0

    # Inicializar la serpiente
    serpiente = []
    largo_serpiente = 1

    # Posición de la comida
    comida_x = round(random.randrange(0, ancho - tamaño_bloque) / 20.0) * 20.0
    comida_y = round(random.randrange(0, alto - tamaño_bloque) / 20.0) * 20.0

    while not game_over:

        while game_close:
            boton_reiniciar, boton_salir = mostrar_menu()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_reiniciar.collidepoint(evento.pos):
                        juego()  # Reiniciar el juego
                    if boton_salir.collidepoint(evento.pos):
                        game_over = True
                        game_close = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x_cambio = -tamaño_bloque
                    y_cambio = 0
                elif evento.key == pygame.K_RIGHT:
                    x_cambio = tamaño_bloque
                    y_cambio = 0
                elif evento.key == pygame.K_UP:
                    y_cambio = -tamaño_bloque
                    x_cambio = 0
                elif evento.key == pygame.K_DOWN:
                    y_cambio = tamaño_bloque
                    x_cambio = 0

        if x >= ancho or x < 0 or y >= alto or y < 0:
            game_close = True
        x += x_cambio
        y += y_cambio
        pantalla.blit(imagen_fondo, (0, 0))  # Dibujar el fondo

        pantalla.blit(imagen_comida, [comida_x, comida_y])  # Dibujar la comida

        cuerpo_serpiente = []
        cuerpo_serpiente.append(x)
        cuerpo_serpiente.append(y)
        serpiente.append(cuerpo_serpiente)

        if len(serpiente) > largo_serpiente:
            del serpiente[0]

        for bloque in serpiente[:-1]:
            if bloque == cuerpo_serpiente:
                game_close = True

        for bloque in serpiente:
            pantalla.blit(imagen_serpiente, (bloque[0], bloque[1]))  # Dibujar la serpiente

        mostrar_puntaje(largo_serpiente - 1)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ancho - tamaño_bloque) / 20.0) * 20.0
            comida_y = round(random.randrange(0, alto - tamaño_bloque) / 20.0) * 20.0
            largo_serpiente += 1

        reloj.tick(velocidad)

    pygame.quit()
    quit()

# Iniciar el juego
juego()
