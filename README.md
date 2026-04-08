#  Descargador Automático de Mangas - Olympus Biblioteca

Script en Python para descargar mangas **completos** de Olympus Biblioteca de forma automática y ordenada.

##  Características

- Descarga **todo el manga** con **una sola URL** (la página de la serie).
- Solo descarga capítulos reales (ignora .5, .1, extras, pausas, especiales, omakes, etc.).
- Crea carpetas por capítulo (`Cap_001`, `Cap_002`, …).
- Al terminar genera un **archivo .zip** con todo el manga listo para leer.
- Modo silencioso (no abre ventanas).
- Muy optimizado (usa un solo navegador durante todo el proceso).

## Archivos incluidos

- `descargar_manga_completo.py` → Script principal
- `comprimir_manga.py` → Compresor manual (por si necesitas usarlo después)
- `README.md` → Este archivo

##  Requisitos

- Python 3.10 o superior
- Google Chrome instalado
- Las siguientes librerías:

```bash
pip install selenium webdriver-manager tqdm requests