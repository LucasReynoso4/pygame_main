import pygame
pygame.init()

#ANCHO, ALTO
W, H = 1200, 600
TITULO_VENTANA = "TRUNKS ADVENTURES"


proyectiles_juego = pygame.sprite.Group()  
proyectiles_juego_personaje = pygame.sprite.Group() 

gravedad = 2
potencia_salto = -15
limite_velocidad_caida = 15


velocidad_proyectil = 5
contador_muerte = 0



piso = pygame.Rect(0,520,W,20)

PANTALLA = pygame.display.set_mode((W,H))
def girar_imagenes(lista_original, flip_x: bool, flip_y: bool)-> list:
    lista_girada = []
    for imagen in lista_original:
        lista_girada.append(pygame.transform.flip(imagen, flip_x, flip_y))

    return lista_girada

def reescalar_imagen(lista_animaciones, W, H):
    for lista in lista_animaciones:
        for i in range(len(lista)):
            imagen = lista[i]
            lista[i] = pygame.transform.scale(imagen, (W,H))

#FONDOS
UBICACION_FONDO_INICIO = "fondos/fondo_inicio.jpg"
UBICACION_FONDO_PAUSA = "fondos/fondo_opciones.png"
UBICACION_FONDO_PERDISTE = "fondos/fondo_perdiste.png"
UBICACION_FONDO_RANKING = "fondos/fondo_ranking.png"
UBICACION_FONDO_GANASTE = "fondos/fondo_ganaste.png"

#BOTONES
UBICACION_BOTON_JUGAR = "botones/jugar.png"
UBICACION_BOTON_PAUSA = "botones/pausa.png"
UBICACION_BOTON_RANKING = "botones/ranking.png"
UBICACION_BOTON_SALIR = "botones/salir.png"
UBICACION_BOTON_GUARDAR = "botones/guardar.png"
UBICACION_BOTON_VOLVER = "botones/volver.png"
UBICACION_BOTON_NIVEL_1 = "botones/01.png"
UBICACION_BOTON_NIVEL_2 = "botones/02.png"
UBICACION_BOTON_NIVEL_3 = "botones/03.png"
UBICACION_BOTON_SELECTOR_NIVELES = "botones/Levels.png"
UBICACION_BOTON_ON_OFF_SONIDO = "botones/Volume.png"

#AUDIO 
UBICACION_SONIDO_CLICK = "audio/click.mp3"
UBICACION_SONIDO_INICIAR = "audio/iniciar.mp3"
UBICACION_SONIDO_MUSICA_MENU = "audio/musica_intro_dragonball.mp3"
UBICACION_SONIDO_ATAQUE_ESPADA = "audio/espada.wav"
UBICACION_SONIDO_PROYECTIL = "audio/proyectil.wav"
UBICACION_SONIDO_NIVEL_1 = "audio/level_1.wav"
UBICACION_SONIDO_NIVEL_2 = "audio/level_2.wav"
UBICACION_SONIDO_NIVEL_3 = "audio/level_3.wav"
UBICACION_SONIDO_ENEMIGO_MUERE = "audio/enemigo_muere.wav"
UBICACION_SONIDO_RANGER_MUERE = "audio/muere_trunks.wav"

#PERSONAJE
personaje_quieto = [
    pygame.image.load("imagenes/trunks/quieto/0.png"),
    pygame.image.load("imagenes/trunks/quieto/1.png"),
    pygame.image.load("imagenes/trunks/quieto/2.png"),
    pygame.image.load("imagenes/trunks/quieto/3.png"),
]



personaje_camina = [
    pygame.image.load("imagenes/trunks/camina/camina1.png"),
    pygame.image.load("imagenes/trunks/camina/camina2.png"),
    pygame.image.load("imagenes/trunks/camina/camina3.png"),
    pygame.image.load("imagenes/trunks/camina/camina4.png"),
    pygame.image.load("imagenes/trunks/camina/camina5.png"),
    pygame.image.load("imagenes/trunks/camina/camina6.png")
]


personaje_salta = [
    pygame.image.load("imagenes/trunks/salta/salta1.png"),
    pygame.image.load("imagenes/trunks/salta/salta2.png"),
    pygame.image.load("imagenes/trunks/salta/salta3.png"),
    pygame.image.load("imagenes/trunks/salta/salta4.png"),
    pygame.image.load("imagenes/trunks/salta/salta5.png")
]
personaje_pega = [
    pygame.image.load("imagenes/trunks/pega/pega1.png"),
    pygame.image.load("imagenes/trunks/pega/pega2.png"),
    pygame.image.load("imagenes/trunks/pega/pega3.png"),
    pygame.image.load("imagenes/trunks/pega/pega4.png")
]


ataque_espada = [
    pygame.image.load("imagenes/trunks/ataque_espada/4.png"),
    pygame.image.load("imagenes/trunks/ataque_espada/5.png"),
    pygame.image.load("imagenes/trunks/ataque_espada/6.png"),
    pygame.image.load("imagenes/trunks/ataque_espada/7.png"),
    pygame.image.load("imagenes/trunks/ataque_espada/8.png"),
    pygame.image.load("imagenes/trunks/ataque_espada/9.png"),

    
]
personaje_camina_izquierda = girar_imagenes(personaje_camina, True, False)
personaje_quieto_izquierda = girar_imagenes(personaje_quieto, True, False)
ataque_espada_izquierda = girar_imagenes(ataque_espada, True, False)
lista_animaciones = [personaje_quieto, personaje_camina, personaje_camina_izquierda, personaje_salta, personaje_quieto_izquierda]
imagenes_reescaladas = reescalar_imagen(lista_animaciones, 30, 70)

#ENEMIGO
enemigo_quieto = [
    pygame.image.load("imagenes/enemigo_quieto/0.png"),
    pygame.image.load("imagenes/enemigo_quieto/1.png"),
    pygame.image.load("imagenes/enemigo_quieto/2.png"),
    pygame.image.load("imagenes/enemigo_quieto/3.png")
]
enemigo_camina = [
    pygame.image.load("imagenes/enemigo_camina/4.png"),
    pygame.image.load("imagenes/enemigo_camina/5.png"),
    pygame.image.load("imagenes/enemigo_camina/6.png"),
    pygame.image.load("imagenes/enemigo_camina/7.png"),

]
enemigo_muere = [
    pygame.image.load("imagenes/enemigo_muere/8.png"),
    pygame.image.load("imagenes/enemigo_muere/9.png"),
    pygame.image.load("imagenes/enemigo_muere/10.png"),
    pygame.image.load("imagenes/enemigo_muere/11.png")
    
]
enemigo_camina_izquierda = girar_imagenes(enemigo_camina, True, False)




