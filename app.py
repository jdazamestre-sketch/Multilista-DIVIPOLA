# =============================================================================
# app.py
# Aplicación Flask (siguiendo la guía "How to Make a Web Map with Python's
# Flask and Leaflet"):
#   - La ruta "/" arma los marcadores a partir de la multilista y se los pasa
#     a la plantilla con render_template; la plantilla los recorre con Jinja.
#   - Además, la API expone la multilista completa en JSON.
#
# Ejecutar:   python app.py      y abrir   http://127.0.0.1:8000
# =============================================================================

from flask import Flask, jsonify, render_template
from multilista import construir_multilista, a_diccionario, imprimir_arbol

app = Flask(__name__)

# La multilista se construye UNA sola vez, leyendo el CSV de la DIVIPOLA
colombia = construir_multilista("DIVIPOLA.csv")


# -----------------------------------------------------------------------------
# Página del mapa: igual que en la guía, se arma una lista de "markers"
# (con lat, lon y texto del popup) y se envía a la plantilla.
# Aquí cada marcador de departamento lleva también la lista de sus municipios,
# sacada de la SUBLISTA del nodo departamento.
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    markers = []
    dep = colombia.sub.head                      # recorre la lista de departamentos
    while dep != None:
        municipios = []
        mun = dep.sub.head                       # recorre la sublista de municipios
        while mun != None:
            municipios.append({
                "nombre": mun.data["nombre"],
                "codigo": mun.data["codigo"],
                "tipo": mun.data["tipo"],
                "lat": mun.data["lat"],
                "lon": mun.data["lon"],
            })
            mun = mun.next
        markers.append({
            "nombre": dep.data["nombre"],
            "codigo": dep.data["codigo"],
            "lat": dep.data["lat"],
            "lon": dep.data["lon"],
            "popup": dep.data["nombre"] + " (" + str(dep.sub.size) + " municipios)",
            "municipios": municipios,
        })
        dep = dep.next

    total = 0
    current = colombia.sub.head
    while current != None:
        total = total + current.sub.size
        current = current.next

    return render_template("index.html", markers=markers,
                           total_departamentos=colombia.sub.size,
                           total_municipios=total)


# API: toda la multilista como JSON  (País -> Departamentos -> Municipios)
@app.route("/api/multilista")
def api_multilista():
    return jsonify(a_diccionario(colombia))


# API: un departamento con sus municipios, buscado por código (ej: /api/departamento/05)
@app.route("/api/departamento/<codigo>")
def api_departamento(codigo):
    dep = colombia.sub.search("codigo", codigo)
    if dep == None:
        return jsonify({"error": "Departamento no encontrado"}), 404
    return jsonify(a_diccionario(dep))


if __name__ == "__main__":
    # Al iniciar se muestra el árbol en la consola (resumido)
    imprimir_arbol(colombia, max_municipios=3)
    app.run(debug=True, port=8000)   # puerto 8000 (en Windows el 5000 suele estar reservado)
