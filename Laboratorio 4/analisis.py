import random
import time
import matplotlib.pyplot as plt
import numpy as np
from quadtree import construir_quadtree, radio_fuerza_bruta, cercanos_fuerza_bruta

TAMANO_CIUDAD = 10000
RADIO = 500
NUM_CONSULTAS = 20
CANTIDADES = [1000, 3000, 10000, 30000, 100000, 300000, 1000000]

random.seed(1)

def punto_al_azar():
    return (random.uniform(0, TAMANO_CIUDAD), random.uniform(0, TAMANO_CIUDAD))

def generar_uniforme(n):
    puntos = np.random.uniform(0, TAMANO_CIUDAD, size=(n, 2))
    return puntos.tolist()

def generar_agrupado(n, num_clusters=10, dispersion=400):
    centros = np.random.uniform(0, TAMANO_CIUDAD, size=(num_clusters, 2))

    indices_centros = np.random.choice(num_clusters, size=n)
    centros_asignados = centros[indices_centros]
    ruido = np.random.normal(loc=0.0, scale=dispersion, size=(n, 2))
    puntos = np.clip(centros_asignados + ruido, 0.0, TAMANO_CIUDAD)
    return puntos.tolist()

def tiempo_promedio(funcion, consultas):
    inicio = time.perf_counter()
    for consulta in consultas:
        funcion(consulta)
    return (time.perf_counter() - inicio) * 1000 / len(consultas)

def desde_que_n_gana(t_arbol, t_fb):
    for i in range(len(CANTIDADES)):
        if all(a < f for a, f in zip(t_arbol[i:], t_fb[i:])):
            return CANTIDADES[i]
    return None

def medir(generar):
    r = {"armado": [], "radio_arbol": [], "radio_fb": [], "cercano_arbol": [], "cercano_fb": []}
    for n in CANTIDADES:
        entregas = generar(n)
        consultas = [punto_al_azar() for _ in range(NUM_CONSULTAS)]
        inicio = time.perf_counter()
        arbol = construir_quadtree(entregas)
        r["armado"].append((time.perf_counter() - inicio) * 1000)
        r["radio_arbol"].append(tiempo_promedio(lambda c: arbol.buscar_en_radio(c, RADIO), consultas))
        r["radio_fb"].append(tiempo_promedio(lambda c: radio_fuerza_bruta(entregas, c, RADIO), consultas))
        r["cercano_arbol"].append(tiempo_promedio(lambda c: arbol.mas_cercanos(c, 1), consultas))
        r["cercano_fb"].append(tiempo_promedio(lambda c: cercanos_fuerza_bruta(entregas, c, 1), consultas))
        print(f"n={n:8d} | radio: árbol {r['radio_arbol'][-1]:9.3f} ms, fb {r['radio_fb'][-1]:9.3f} ms"
              f" | cercano: árbol {r['cercano_arbol'][-1]:9.3f} ms, fb {r['cercano_fb'][-1]:9.3f} ms"
              f" | armado {r['armado'][-1]:9.1f} ms", flush=True)
    return r

def graficar(resultados):
    figura, ejes = plt.subplots(1, 2, figsize=(14, 5))
    for nombre, r in resultados.items():
        ejes[0].plot(CANTIDADES, r["radio_arbol"], "o-", label=f"Quadtree ({nombre})")
        ejes[0].plot(CANTIDADES, r["radio_fb"], "s--", label=f"Fuerza bruta ({nombre})")
        ejes[1].plot(CANTIDADES, r["cercano_arbol"], "o-", label=f"Quadtree ({nombre})")
        ejes[1].plot(CANTIDADES, r["cercano_fb"], "s--", label=f"Fuerza bruta ({nombre})")
    ejes[0].set_title(f"Búsqueda por radio ({RADIO} m)")
    ejes[1].set_title("Vecino más cercano")
    for eje in ejes:
        eje.set_xscale("log")
        eje.set_yscale("log")
        eje.set_xlabel("Cantidad de puntos (n), escala logarítmica")
        eje.set_ylabel("Tiempo por consulta (ms), escala logarítmica")
        eje.grid(True, which="both", alpha=0.3)
        eje.legend()
    figura.tight_layout()
    figura.savefig("comparacion_tiempos.png", dpi=120)
    plt.close(figura)

    plt.figure(figsize=(8, 5))
    for nombre, r in resultados.items():
        plt.plot(CANTIDADES, r["armado"], "o-", label=nombre)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Cantidad de puntos (n), escala logarítmica")
    plt.ylabel("Tiempo de armado (ms), escala logarítmica")
    plt.title("Tiempo de armado del Quadtree")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.savefig("armado.png", dpi=120)
    plt.close()

def main():
    resultados = {}
    for nombre, generar in [("uniforme", generar_uniforme), ("agrupado", generar_agrupado)]:
        print(f"\nDistribución {nombre}")
        resultados[nombre] = medir(generar)
    graficar(resultados)

    print("\nRESUMEN DE RESULTADOS")
    for nombre, r in resultados.items():
        print(f"\n{nombre}:")
        print(f"  Quadtree gana en radio desde n = {desde_que_n_gana(r['radio_arbol'], r['radio_fb'])}")
        print(f"  Quadtree gana en más cercano desde n = {desde_que_n_gana(r['cercano_arbol'], r['cercano_fb'])}")
        print(f"  En n = {CANTIDADES[-1]}: radio {r['radio_fb'][-1] / r['radio_arbol'][-1]:.1f}x, "
              f"más cercano {r['cercano_fb'][-1] / r['cercano_arbol'][-1]:.1f}x más rápido que fuerza bruta")
        print(f"  Armado por punto: {r['armado'][0] / CANTIDADES[0]:.4f} ms (n = {CANTIDADES[0]}) "
              f"-> {r['armado'][-1] / CANTIDADES[-1]:.4f} ms (n = {CANTIDADES[-1]})")

if __name__ == "__main__":
    main()