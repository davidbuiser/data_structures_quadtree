import heapq
import math

CAPACIDAD = 8
PROFUNDIDAD_MAX = 20

def distancia(punto_a, punto_b):
    return math.hypot(punto_a[0] - punto_b[0], punto_a[1] - punto_b[1])

class Quadtree:
    def __init__(self, izquierda, abajo, derecha, arriba, profundidad = 0):
        self.izquierda, self.abajo = izquierda, abajo
        self.derecha, self.arriba = derecha, arriba
        self.centro_x = (izquierda + derecha) / 2
        self.centro_y = (abajo + arriba) / 2
        self.profundidad = profundidad
        self.puntos = []
        self.hijos = []

    def insertar(self, punto):
        if self.hijos:
            self.obtener_hijo(punto).insertar(punto)
            return
        self.puntos.append(punto)
        if len(self.puntos) > CAPACIDAD and self.profundidad < PROFUNDIDAD_MAX:
            self.dividir()

    def dividir(self):
        p = self.profundidad + 1
        self.hijos = [
            Quadtree(self.izquierda, self.abajo, self.centro_x, self.centro_y, p),
            Quadtree(self.centro_x, self.abajo, self.derecha, self.centro_y, p),
            Quadtree(self.izquierda, self.centro_y, self.centro_x, self.arriba, p),
            Quadtree(self.centro_x, self.centro_y, self.derecha, self.arriba, p),
        ]
        for punto in self.puntos:
            self.obtener_hijo(punto).insertar(punto)
        self.puntos = []

    def obtener_hijo(self, punto):
        posicion = 0
        if punto[0] >= self.centro_x:
            posicion += 1
        if punto[1] >= self.centro_y:
            posicion += 2
        return self.hijos[posicion]

    def distancia_al_cuadrante(self, punto):
        dx = max(self.izquierda - punto[0], 0, punto[0] - self.derecha)
        dy = max(self.abajo - punto[1], 0, punto[1] - self.arriba)
        return math.hypot(dx, dy)

    def buscar_en_radio(self, centro, radio):
        if self.distancia_al_cuadrante(centro) > radio:
            return []
        encontrados = [p for p in self.puntos if distancia(p, centro) <= radio]
        for hijo in self.hijos:
            encontrados += hijo.buscar_en_radio(centro, radio)
        return encontrados

    def mas_cercanos(self, punto, cuantos=1, cercanos=None):
        if cercanos is None:
            cercanos = []
        if len(cercanos) == cuantos and self.distancia_al_cuadrante(punto) > cercanos[-1][0]:
            return cercanos
        for p in self.puntos:
            cercanos.append((distancia(p, punto), p))
        cercanos.sort()
        del cercanos[cuantos:]
        for hijo in sorted(self.hijos, key = lambda h: h.distancia_al_cuadrante(punto)):
            hijo.mas_cercanos(punto, cuantos, cercanos)
        return cercanos

def construir_quadtree(puntos):
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    arbol = Quadtree(min(xs), min(ys), max(xs), max(ys))
    for punto in puntos:
        arbol.insertar(punto)
    return arbol

def radio_fuerza_bruta(puntos, centro, radio):
    return [p for p in puntos if distancia(p, centro) <= radio]

def cercanos_fuerza_bruta(puntos, punto, cuantos = 1):
    return heapq.nsmallest(cuantos, ((distancia(p, punto), p) for p in puntos))