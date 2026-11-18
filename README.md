# Multilista jerárquica con la DIVIPOLA

Colombia → Departamentos → Municipios, construida con nodos (`Node`) y listas enlazadas (`LinkedList`) donde cada nodo puede tener una sublista.

## Archivos
- `DIVIPOLA.csv`: datos del DANE (33 departamentos, 1122 municipios). Se lee con el módulo `csv`.
- `multilista.py`: arma la multilista y la imprime como árbol (├── / └──).
- `app.py`: Flask.
  - `/`: el mapa. Como en la guía, arma la lista `markers` recorriendo la multilista y la pasa con `render_template`.
  - `/api/multilista`: toda la multilista en JSON.
  - `/api/departamento/<codigo>`: un departamento con sus municipios (ej. `/api/departamento/05`).
- `templates/index.html`: plantilla Jinja; un `{% for %}` escribe los marcadores de Leaflet y la lista del panel.
- `ver_nodos.py` (`VER_NODOS.bat`): muestra la multilista por dentro, nodo por nodo (data, next y sub).
- `static/css/universal.css` y `static/js/universal.js`: estilos y creación del mapa (estructura de la guía).

## Cómo correrlo
Doble clic en `CORRER.bat`, o:
```
pip install flask
python multilista.py      # imprime el árbol en consola
python ver_nodos.py       # muestra los nodos con sus punteros
python app.py             # abre http://127.0.0.1:8000
```
