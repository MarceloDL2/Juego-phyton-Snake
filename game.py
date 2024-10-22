import pygame
import random

# Inicializar pygame
pygame.init()

# Definir colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# Cargar música
pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play(-1)  # Reproducir en bucle

# Dimensiones de la pantalla
ancho = 600
alto = 400

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Juego de la Vibora')

# Definir el reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Tamaño de los bloques de la serpiente
tamaño_bloque = 20
velocidad_inicial = 7

# Definir fuente para mostrar el puntaje
fuente = pygame.font.SysFont("comicsansms", 35)
fuente_menu = pygame.font.SysFont("comicsansms", 30)

# Función para mostrar el puntaje
def mostrar_puntaje(puntaje):
    valor = fuente.render("Puntaje: " + str(puntaje), True, blanco)
    pantalla.blit(valor, [0, 0])

# Función para dibujar la serpiente
def dibujar_serpiente(tamaño_bloque, lista_serpiente):
    for x in lista_serpiente:
        pygame.draw.rect(pantalla, verde, [x[0], x[1], tamaño_bloque, tamaño_bloque])

# Función para dibujar botones
def dibujar_boton(texto, x, y, w, h, color_activo, color_inactivo, accion=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(pantalla, color_activo, (x, y, w, h))
        if click[0] == 1 and accion is not None:
            accion()
    else:
        pygame.draw.rect(pantalla, color_inactivo, (x, y, w, h))

    texto_boton = fuente_menu.render(texto, True, blanco)
    pantalla.blit(texto_boton, [x + (w / 6), y + (h / 6)])

# Función principal del juego
def juego():
    game_over = False
    game_close = False

    # Posición inicial de la serpiente
    x = ancho / 2
    y = alto / 2

    # Cambio de posición inicial
    x_cambio = 0
    y_cambio = 0

    # Lista para almacenar las posiciones de la serpiente
    lista_serpiente = []
    largo_serpiente = 1

    # Posición de la comida
    comida_x = round(random.randrange(0, ancho - tamaño_bloque) / 20.0) * 20.0
    comida_y = round(random.randrange(0, alto - tamaño_bloque) / 20.0) * 20.0

    # Velocidad inicial
    velocidad = velocidad_inicial

    while not game_over:

        while game_close:
            pantalla.fill(negro)
            mensaje = fuente.render("Perdiste!", True, rojo)
            pantalla.blit(mensaje, [ancho / 3, alto / 3])

            # Botones clickeables
            dibujar_boton("Jugar de nuevo", 150, 200, 200, 50, verde, azul, juego)
            dibujar_boton("Salir", 150, 270, 200, 50, rojo, azul, pygame.quit)

            mostrar_puntaje(largo_serpiente - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
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

        # Verificar si la serpiente sale de los límites
        if x >= ancho or x < 0 or y >= alto or y < 0:
            game_close = True
        x += x_cambio
        y += y_cambio
        pantalla.fill(negro)

        # Dibujar la comida
        pygame.draw.rect(pantalla, rojo, [comida_x, comida_y, tamaño_bloque, tamaño_bloque])

        # Actualizar la posición de la serpiente
        cabeza_serpiente = []
        cabeza_serpiente.append(x)
        cabeza_serpiente.append(y)
        lista_serpiente.append(cabeza_serpiente)

        if len(lista_serpiente) > largo_serpiente:
            del lista_serpiente[0]

        # Verificar si la serpiente choca consigo misma
        for segmento in lista_serpiente[:-1]:
            if segmento == cabeza_serpiente:
                game_close = True

        dibujar_serpiente(tamaño_bloque, lista_serpiente)
        mostrar_puntaje(largo_serpiente - 1)

        pygame.display.update()

        # Verificar si la serpiente come la comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ancho - tamaño_bloque) / 20.0) * 20.0
            comida_y = round(random.randrange(0, alto - tamaño_bloque) / 20.0) * 20.0
            largo_serpiente += 1
            if velocidad < 20:
                velocidad += 1  # Incrementa la velocidad al comer comida

        reloj.tick(velocidad)

    pygame.quit()
    quit()

# Iniciar el juego
juego()
