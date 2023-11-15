import pygame, random
from constantes import *


def obtener_rectangulos(principal: pygame.Rect):
    """
Crea y devuelve un diccionario que contiene varios rectángulos asociados al rectángulo principal.

Parameters:
- principal (pygame.Rect): El rectángulo principal del cual se derivan los demás.

Returns:
- dict: Un diccionario que contiene rectángulos etiquetados como 'main', 'bottom', 'right', 'left' y 'top'.
"""
    diccionario = {}
    diccionario["main"] = principal
    diccionario["bottom"] = pygame.Rect(principal.left, principal.bottom - 10, principal.width, 10)
    diccionario["right"] = pygame.Rect(principal.right -2, principal.top, 2, principal.height)
    diccionario["left"] = pygame.Rect(principal.left, principal.top, 2, principal.height)
    diccionario["top"] = pygame.Rect(principal.left, principal.top, principal.width, 6)
    
    return diccionario


class Plataforma(pygame.sprite.Sprite):
    """
Clase que representa una plataforma en el juego.

Attributes:
- x (int): Coordenada x de la posición de la plataforma.
- y (int): Coordenada y de la posición de la plataforma.
- imagen (str): Ruta de la imagen utilizada para representar la plataforma.
- image (pygame.Surface): Superficie que representa la imagen de la plataforma.
- rect (pygame.Rect): Rectángulo que delimita la posición y dimensiones de la plataforma.
"""
    def __init__(self, x, y, imagen):
        """
Inicializa una nueva instancia de la clase Plataforma.

Parameters:
- x (int): Coordenada x de la posición de la plataforma.
- y (int): Coordenada y de la posición de la plataforma.
- imagen (str): Ruta de la imagen utilizada para representar la plataforma.
"""
        super().__init__()
        self.image = imagen
        self.image = pygame.image.load(imagen)
        self.image = pygame.transform.scale(self.image, (120, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Personaje(pygame.sprite.Sprite):
    """
Clase que representa al personaje del juego.

Attributes:
- x (int): Coordenada x de la posición inicial del personaje.
- y (int): Coordenada y de la posición inicial del personaje.
- animaciones (list): Lista de animaciones para representar el personaje en diferentes estados.
- contador_pasos (int): Contador para el seguimiento de pasos del personaje.
- velocidad (int): Velocidad de movimiento del personaje.
- posicion_actual_x (int): Índice de la posición actual en la lista de animaciones.
- imagenes_reescaladas (list): Imágenes reescaladas utilizadas para representar al personaje.
- rect (pygame.Rect): Rectángulo que delimita la posición y dimensiones del personaje.
- lados (dict): Diccionario que contiene rectángulos adicionales alrededor del personaje.
- que_hace (str): Estado actual del personaje (puede ser "Derecha", "Izquierda", "Salta", "Ataque_izquierda", "Ataque_derecha", "Quieto").
- desplazamiento_y (int): Valor de desplazamiento vertical del personaje.
- desplazamiento_x (int): Valor de desplazamiento horizontal del personaje.
- esta_saltando (bool): Indica si el personaje está en estado de salto.
- tiene_escudo (bool): Indica si el personaje tiene un escudo activado.
- direccion (str): Dirección actual del personaje ("derecha" o "izquierda").
- sonido_proyectil (pygame.mixer.Sound): Sonido para los disparos del personaje.
- sonido_espada (pygame.mixer.Sound): Sonido para los ataques de espada del personaje.
- tiempo_ultimo_disparo (int): Tiempo del último disparo realizado por el personaje.
- retraso_entre_disparos (int): Tiempo de retraso entre disparos en milisegundos.
"""
    def __init__(self, x, y, animaciones):
        """
        Inicializa una nueva instancia de la clase Personaje.

        Parameters:
        - x (int): Coordenada x de la posición inicial del personaje.
        - y (int): Coordenada y de la posición inicial del personaje.
        - animaciones (list): Lista de animaciones para representar al personaje en diferentes estados.
        """
        super().__init__()
        self.animaciones = animaciones
        self.contador_pasos = 0
        self.velocidad = 10
        self.posicion_actual_x = 0
        self.imagenes_reescaladas = imagenes_reescaladas
        self.rect = self.animaciones[self.posicion_actual_x].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)
        self.que_hace = "Quieto"
        self.desplazamiento_y = 0
        self.desplazamiento_x = 0
        self.esta_saltando = False
        self.tiene_escudo = False
        self.direccion = "derecha"  # Nueva variable para controlar la dirección del personaje
        self.sonido_proyectil = pygame.mixer.Sound(UBICACION_SONIDO_PROYECTIL)
        self.sonido_espada = pygame.mixer.Sound(UBICACION_SONIDO_ATAQUE_ESPADA)
        self.tiempo_ultimo_disparo = 0  # Variable para rastrear el tiempo del último disparo
        self.retraso_entre_disparos = 700 # Establece el retraso deseado entre disparos en milisegundos
        
    def update(self, plataformas):


        """
        Actualiza el estado del personaje en cada fotograma.

        Parameters:
        - plataformas (list): Lista de plataformas en el juego.
        """
        keys = pygame.key.get_pressed()
        
 
        if keys[pygame.K_RIGHT] and self.rect.right < W - self.velocidad:
            self.que_hace = "Derecha"
            self.rect.x += self.velocidad
            self.direccion = "derecha"  # Actualiza la dirección cuando se mueve hacia la derecha
        elif keys[pygame.K_LEFT] and self.rect.left > self.velocidad:
            self.que_hace = "Izquierda"
            self.rect.x -= self.velocidad
            self.direccion = "izquierda"  # Actualiza la dirección cuando se mueve hacia la izquierda
            #SALTO
        elif self.rect.colliderect(piso) and keys[pygame.K_UP] and self.esta_saltando == False:
                    self.que_hace = "Salta"
                    self.desplazamiento_y = -potencia_salto
                    self.esta_saltando = True

        
        elif keys[pygame.K_q]:
            if self.direccion == "izquierda":
                self.que_hace = "Ataque_izquierda"  # Ataque hacia la izquierda si la dirección es "izquierda"
                self.sonido_espada.play()
            else:
                self.que_hace = "Ataque_derecha"  # Ataque hacia la derecha
                self.sonido_espada.play()
        elif keys[pygame.K_r]and pygame.time.get_ticks() - self.tiempo_ultimo_disparo >= self.retraso_entre_disparos:
            self.tiempo_ultimo_disparo = pygame.time.get_ticks()
            if self.direccion == "derecha":
                proyectil = Proyectil(self.rect.right, self.rect.centery, 10, pygame.image.load("imagenes/poder/67 - copia.png"))  # Crea un proyectil en la posición del personaje
                self.sonido_proyectil.play()
            else:
                proyectil = Proyectil(self.rect.left, self.rect.centery, -10, pygame.image.load("imagenes/poder/67.png"))  # Crea un proyectil en la posición del personaje, con velocidad negativa para lanzarlo hacia la izquierda
                self.sonido_proyectil.play()
            proyectiles_juego_personaje.add(proyectil)
        else:    
            self.que_hace = "Quieto"
            self.desplazamiento_x = 0


            for plataforma in plataformas:
                if self.rect.colliderect(plataforma):
                    self.que_hace = "Salta"
                    self.desplazamiento_y = -potencia_salto
                    self.esta_saltando = True
                    print("entro....")
                    break 



        self.rect.x += self.desplazamiento_x
        for lado in self.lados:
            if lado == "top":
                self.rect.y += self.desplazamiento_x


        self.lados = obtener_rectangulos(self.rect)

    def colision_con_plataformas(self, plataformas):
        """
Verifica si el personaje colisiona con alguna plataforma en la lista y ajusta su posición en consecuencia.

Parameters:
- plataformas (list): Lista de plataformas en el juego.
"""
        for plataforma in plataformas:
            if self.lados["bottom"].colliderect(plataforma.rect) and self.desplazamiento_y >= 0:
                self.rect.y = plataforma.rect.top - self.rect.height
                self.esta_saltando = False
                self.desplazamiento_y = 0
                break  # Importante salir del bucle después de la primera colisión

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones):
        super().__init__()
        self.animaciones = animaciones
        self.contador_pasos = 0
        self.velocidad = 3
        self.direccion = 1
        self.posicion_actual_x = 0
        self.rect = self.animaciones[self.posicion_actual_x].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)
        self.que_hace = "quieto"
        self.cayendo = True
        self.en_plataforma = False

    def update(self, grupo_plataformas):
        if self.cayendo:
            self.rect.y += self.velocidad + 5
            self.que_hace = "quieto"
            colision_plataforma = pygame.sprite.spritecollide(self, grupo_plataformas, False)
            if colision_plataforma:
                self.cayendo = False
                plataforma = colision_plataforma[0]
                self.rect.bottom = plataforma.rect.top
        else:
            self.rect.x += self.velocidad * self.direccion
            if self.direccion == 1:
                self.que_hace = "izquierda"
            elif self.direccion == -1:
                self.que_hace = "derecha"

            colision_plataforma = pygame.sprite.spritecollide(self, grupo_plataformas, False)
            if colision_plataforma:
                plataforma = colision_plataforma[0]
                if self.rect.right > plataforma.rect.right or self.rect.left < plataforma.rect.left:
                    self.direccion *= -1
                else:
                    self.rect.bottom = plataforma.rect.top
            else:
                self.cayendo = True

        if self.rect.left <= 0 or self.rect.right >= W:
            self.direccion *= -1

        if self.rect.bottom >= H/2 +220:  # Límite del eje Y (400)
            self.rect.bottom = H/2 +220
            self.cayendo = False

        if self.rect.top >= H/2 +220:
            self.rect.bottom = H/2 +221  # Ajustamos la posición para que no atraviese el piso
            self.cayendo = False

        self.lados = obtener_rectangulos(self.rect)

    def generar_enemigos(cantidad):
        enemigos = pygame.sprite.Group()

        for _ in range(cantidad):
            x = random.randint(0, W - 50)  
            y = random.randint(-200, -50)  
            enemigo = Enemigo(x, y, enemigo_camina)  
            enemigos.add(enemigo)
        return enemigos
    
    def agregar_enemigos(enemigos_actuales, cantidad):
        enemigos = pygame.sprite.Group(enemigos_actuales)

        for _ in range(cantidad):
            x = random.randint(0, W - 50)
            y = random.randint(-200, -50)
            enemigo = Enemigo(x, y, enemigo_camina)
            enemigos.add(enemigo)
        return enemigos


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen = pygame.image.load("imagenes/boss_dispara/3.png")
        self.rect = self.imagen.get_rect()
        self.rect.right = W -5 
        self.rect.bottom = 465
        self.tiro_delay = 4000
        self.colisiones_proyectil = 0
        self.delay_proyectil = 0
        self.DELAY_MAX = 1000
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        PANTALLA.blit(self.imagen, self.rect)

    def disparo(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.ultimo_tiro >= self.tiro_delay:
            self.ultimo_tiro = tiempo

            proyectil_boss = Proyectil(self.rect.right, self.rect.centery, -5, pygame.image.load("imagenes/boss_disparo/disparo_boss.png"))
            proyectiles_juego.add(proyectil_boss)

class Espada(pygame.sprite.Sprite):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.rect = pygame.Rect(x, y, z, z)

class Orbe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("orbes/20.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lados = obtener_rectangulos(self.rect)



class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, imagen):
        """
Inicializa una instancia de la clase Proyectil.

Parámetros:
- x (int): La coordenada x inicial del proyectil.
- y (int): La coordenada y inicial del proyectil.
- velocidad (int): La velocidad horizontal del proyectil.
- imagen (pygame.Surface): La imagen del proyectil.

Atributos:
- imagen (pygame.Surface): La imagen del proyectil.
- rect (pygame.Rect): El rectángulo que rodea al proyectil.
- velocidad (int): La velocidad horizontal del proyectil.
- tiempo_creacion (int): El tiempo en milisegundos en el que se creó el proyectil.
"""

        super().__init__()
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad
        self.tiempo_creacion = pygame.time.get_ticks()

    def update(self):
        """
    Actualiza la posición del proyectil en el juego.

    - Mueve el proyectil horizontalmente según su velocidad.
    - Dibuja la imagen del proyectil en la pantalla.

    Si el proyectil sale de los límites de la pantalla, se elimina.
    """
        self.rect.x += self.velocidad
        PANTALLA.blit(self.imagen, self.rect)

        if self.rect.right < 0 or self.rect.left > W:
            self.kill()

class Boton():
    def __init__(self, imagen, escala, x, y):
        super(Boton, self).__init__()
        self.escala = escala
        self.imagen = pygame.transform.smoothscale(imagen, self.escala)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clickeado = False

    def actualizar_imagen(self, imagen):
        self.imagen = pygame.transform.smoothscale(imagen, self.escala)

    def renderizar(self, pantalla):
        accionar = False
        posicion = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion):
            if pygame.mouse.get_pressed()[0] and not self.clickeado:
                accionar = True
                self.clickeado = True 
            if not pygame.mouse.get_pressed()[0]:
                self.clickeado = False

        pantalla.blit(self.imagen, self.rect)
        return accionar
    
    
    def on_off_volumen(self, pantalla):
        accionar = False
        posicion = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion):
            if pygame.mouse.get_pressed()[0] and not self.clickeado:
                accionar = True
                self.clickeado = True

                self.estado_volumen = not self.estado_volumen
                if self.estado_volumen:
                    pygame.mixer.music.set_volume(0.2)
                else:
                    pygame.mixer.music.set_volume(0.0)

            if not pygame.mouse.get_pressed()[0]:
                self.clickeado = False

        pantalla.blit(self.imagen, self.rect)
        return accionar
    




