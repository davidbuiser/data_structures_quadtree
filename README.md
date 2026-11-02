# Laboratorio 4: Quadtree vs. Fuerza Bruta

**Estudiante:** Carlos David Buitrago

Sistema de consulta para 10.000 puntos de entrega en una ciudad. Se implementa un Quadtree 2D y se compara contra fuerza bruta en dos consultas: *¿qué puntos están a un radio de 500 m de un punto dado?* y *¿cuál es el punto de entrega más cercano a una ubicación dada?*

---

## 1. Declaración de uso de IA  

- **Herramienta:** Claude (Anthropic), modelo Claude Sonnet 5.5.
- **Qué hizo la IA:** Redactó el código que dio origen a las gráficas de `test.py` y `analisis.py`, asimismo con la impresión en consola de los resultados y este README. También elaboró una hoja de ruta con el planteamiento inicial del problema, usado por el estudiante para la lógica posterior y apoyó las labores de interpretación del laboratorio.


## 2. Qué es un quadtree

Un **quadtree** es un árbol en el que cada nodo interno tiene cuatro hijos y que se usa para dividir recursivamente el plano en cuadrantes. Su utilidad es acelerar consultas espaciales: en vez de comparar la consulta con todos los puntos, se descartan regiones enteras del plano que no pueden contener la respuesta.


## 3. Estructura del repositorio y ejecución

| Archivo       | Contenido |
| ------------- | --- |
| `quadtree.py` | Clase `Quadtree` (inserción, búsqueda por radio, k vecinos más cercanos) y las funciones de fuerza bruta. |
| `test.py`     | 6 pruebas unitarias y 2 gráficas de verificación visual (`radio.png`, `vecinos.png`). |
| `analisis.py` | Medición de tiempos para n de 10³ a 10⁶, gráficas y resumen numérico. |

Requiere Python 3.10 o superior y `matplotlib`.

```
pip install matplotlib
python test.py        # genera radio.png y vecinos.png y ejecuta las pruebas
python analisis.py    # genera comparacion_tiempos.png y armado.png (varios minutos)
```

---

## 4. Pruebas (`test.py`)

El criterio de corrección es que el árbol devuelva **exactamente** lo mismo que la fuerza bruta.

| Prueba | Qué verifica |
| --- | --- |
| `radio_igual_a_fuerza_bruta` | 100 consultas aleatorias: mismos puntos (listas ordenadas) con 10.000 puntos. |
| `cercanos_igual_a_fuerza_bruta` | 100 consultas aleatorias: mismos 5 más cercanos y mismas distancias. |
| `radio_sin_puntos` | Consulta muy lejos de la ciudad: devuelve lista vacía. |
| `borde_del_radio_inclusivo` | Un punto a distancia exactamente igual al radio sí se incluye. |
| `puntos_duplicados` | 100 puntos idénticos no rompen la construcción y se encuentran todos. |
| `pedir_mas_vecinos_que_puntos` | Con k mayor que n se devuelven los n puntos existentes. |

**Verificación visual:** `radio.png` (puntos dentro del círculo de 500 m resaltados) y `vecinos.png` (5 vecinos más cercanos con un círculo de radio igual a la distancia al quinto).

---

## 5. Metodología de medición (`analisis.py`)

- **Tamaños:** 10³, 3·10³, 10⁴, 3·10⁴, 10⁵, 3·10⁵ y 10⁶ puntos.
- **Distribuciones:** uniforme y agrupada.
- **Consultas:** 20 puntos al azar en la ciudad por cada n (el mismo conjunto para árbol y fuerza bruta). Se reporta el **tiempo promedio por consulta** en milisegundos.
- **Construcción:** se mide una vez por tamaño.
- **Radio:** 500 m, igual en todos los tamaños.
- **Cruce:** `desde_que_n_gana` devuelve el primer n desde el cual el árbol es más rápido en ese n y en todos los mayores.
- **Reproducibilidad:** semilla fija. Los tiempos absolutos dependen del hardware y de la versión de Python.