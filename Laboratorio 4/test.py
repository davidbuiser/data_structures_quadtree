import random
import unittest
import matplotlib.pyplot as plt
from quadtree import construir_quadtree, radio_fuerza_bruta, cercanos_fuerza_bruta

TAMANO_CIUDAD = 10000
RADIO = 500

random.seed(42)

def punto_al_azar():
    return (random.uniform(0, TAMANO_CIUDAD), random.uniform(0, TAMANO_CIUDAD))

entregas = [punto_al_azar() for _ in range(10000)]
arbol = construir_quadtree(entregas)

class PruebasQuadtree(unittest.TestCase):
    def test_radio_igual_a_fuerza_bruta(self):
        for _ in range(100):
            centro = punto_al_azar()
            self.assertEqual(sorted(radio_fuerza_bruta(entregas, centro, RADIO)),
                             sorted(arbol.buscar_en_radio(centro, RADIO)))

    def test_cercanos_igual_a_fuerza_bruta(self):
        for _ in range(100):
            ubicacion = punto_al_azar()
            self.assertEqual(cercanos_fuerza_bruta(entregas, ubicacion, 5),
                             arbol.mas_cercanos(ubicacion, 5))

    def test_radio_sin_puntos(self):
        self.assertEqual(arbol.buscar_en_radio((-50000, -50000), RADIO), [])

    def test_borde_del_radio_inclusivo(self):
        pequeno = construir_quadtree([(3, 4), (100, 100)])
        self.assertEqual(pequeno.buscar_en_radio((0, 0), 5), [(3, 4)])

    def test_puntos_duplicados(self):
        repetidos = construir_quadtree([(10, 10)] * 100 + [(500, 500)])
        self.assertEqual(len(repetidos.buscar_en_radio((10, 10), 1)), 100)

    def test_pedir_mas_vecinos_que_puntos(self):
        pequeno = construir_quadtree([(1, 1), (2, 2), (3, 3)])
        self.assertEqual(len(pequeno.mas_cercanos((0, 0), 10)), 3)

def grafica_radio():
    centro = (5000, 5000)
    dentro = arbol.buscar_en_radio(centro, RADIO)
    plt.figure(figsize=(7, 7))
    plt.scatter(*zip(*entregas), s=2, color="lightgray", label="Puntos de entrega")
    plt.scatter(*zip(*dentro), s=12, color="red", label=f"Dentro del radio ({len(dentro)})")
    plt.gca().add_patch(plt.Circle(centro, RADIO, fill=False, color="blue"))
    plt.scatter(*centro, color="blue", marker="x", s=80, label="Centro")
    plt.title(f"Búsqueda por radio de {RADIO} m")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.legend()
    plt.savefig("radio.png", dpi=120)
    plt.close()

def grafica_cercanos():
    ubicacion = (3000, 7000)
    resultado = arbol.mas_cercanos(ubicacion, 5)
    cercanos = [p for _, p in resultado]
    distancia_maxima = resultado[-1][0]
    plt.figure(figsize=(7, 7))
    plt.scatter(*zip(*entregas), s=6, color="lightgray", label="Puntos de entrega")
    plt.scatter(*zip(*cercanos), s=40, color="green", label="5 más cercanos")
    for p in cercanos:
        plt.plot([ubicacion[0], p[0]], [ubicacion[1], p[1]], color="green", linewidth=0.8)
    plt.gca().add_patch(plt.Circle(ubicacion, distancia_maxima, fill=False, color="green", linestyle="--"))
    plt.scatter(*ubicacion, color="blue", marker="x", s=80, label="Ubicación dada")
    plt.title("Puntos más cercanos")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.xlim(ubicacion[0] - 3 * distancia_maxima, ubicacion[0] + 3 * distancia_maxima)
    plt.ylim(ubicacion[1] - 3 * distancia_maxima, ubicacion[1] + 3 * distancia_maxima)
    plt.gca().set_aspect("equal")
    plt.legend()
    plt.savefig("vecinos.png", dpi=120)
    plt.close()

if __name__ == "__main__":
    grafica_radio()
    grafica_cercanos()
    unittest.main()
