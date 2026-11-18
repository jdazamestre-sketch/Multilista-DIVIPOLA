# =============================================================================
# multilista.py
# Lectura de la DIVIPOLA y representación jerárquica mediante una MULTILISTA.
#
# Jerarquía:   País  ->  Departamentos  ->  Municipios
#
#   Colombia (nodo raíz)
#     └── sublista de departamentos   (LinkedList)
#           └── cada departamento tiene su sublista de municipios (LinkedList)
#
# Una multilista es una lista enlazada en la que cada nodo, además de apuntar
# al siguiente (next), puede tener una SUBLISTA (sub) con sus "hijos".
# =============================================================================

import csv


# -----------------------------------------------------------------------------
# Node: un nodo de la multilista.
#   data -> la información del nodo (un diccionario con nombre, código, etc.)
#   next -> el siguiente nodo del MISMO nivel (siguiente departamento o municipio)
#   sub  -> la sublista de hijos (LinkedList) o None si no tiene hijos
# -----------------------------------------------------------------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.sub = None


# -----------------------------------------------------------------------------
# LinkedList: lista enlazada simple con head y tail.
# Se usa tanto para la lista de departamentos como para cada lista de municipios.
# -----------------------------------------------------------------------------
class LinkedList:
    def __init__(self):
        self.head = None   # primer nodo
        self.tail = None   # último nodo (para insertar al final en O(1))
        self.size = 0      # cantidad de nodos

    # Inserta un nodo nuevo al final de la lista y lo devuelve
    def append(self, data):
        new_node = Node(data)
        if self.head == None:          # lista vacía: el nuevo es head y tail
            self.head = new_node
            self.tail = new_node
        else:                          # si no, se engancha después del tail
            self.tail.next = new_node
            self.tail = new_node
        self.size = self.size + 1
        return new_node

    # Busca un nodo cuyo data[campo] sea igual a valor (recorrido con while)
    def search(self, campo, valor):
        current = self.head
        while current != None:
            if current.data[campo] == valor:
                return current         # lo encontró
            current = current.next
        return None                    # no está en la lista


# -----------------------------------------------------------------------------
# Utilidad: en el CSV las coordenadas vienen con coma decimal ("-75,581775")
# -----------------------------------------------------------------------------
def a_numero(texto):
    return float(texto.replace(",", "."))


# -----------------------------------------------------------------------------
# construir_multilista: lee el CSV y arma la multilista completa.
# Devuelve el nodo raíz "Colombia".
# -----------------------------------------------------------------------------
def construir_multilista(ruta_csv):
    # Nodo raíz (el país) con su sublista de departamentos
    pais = Node({"tipo": "País", "nombre": "Colombia", "codigo": "170"})
    pais.sub = LinkedList()

    # utf-8-sig quita el BOM que trae el archivo al inicio
    archivo = open(ruta_csv, encoding="utf-8-sig", newline="")
    lector = csv.DictReader(archivo)
    filas = list(lector)               # todas las filas del CSV
    archivo.close()

    i = 0
    while i < len(filas):
        fila = filas[i]
        cod_dep = fila["Código Departamento"]
        nom_dep = fila["Nombre Departamento"]

        # 1) ¿Ya existe el departamento en la sublista del país?
        dep = pais.sub.search("codigo", cod_dep)
        if dep == None:
            # No existe: se crea y se le pone su propia sublista de municipios
            dep = pais.sub.append({"tipo": "Departamento",
                                   "nombre": nom_dep,
                                   "codigo": cod_dep})
            dep.sub = LinkedList()

        # 2) Se agrega el municipio al final de la sublista del departamento
        dep.sub.append({
            "tipo": fila["Tipo: Municipio / Isla / Área no municipalizada"],
            "nombre": fila["Nombre Municipio"],
            "codigo": fila["Código Municipio"],
            "lat": a_numero(fila["Latitud"]),
            "lon": a_numero(fila["longitud"]),
        })
        i = i + 1

    # 3) A cada departamento le calculamos un centro (promedio de sus municipios)
    #    para poder ubicarlo en el mapa.
    dep = pais.sub.head
    while dep != None:
        suma_lat = 0
        suma_lon = 0
        mun = dep.sub.head
        while mun != None:
            suma_lat = suma_lat + mun.data["lat"]
            suma_lon = suma_lon + mun.data["lon"]
            mun = mun.next
        dep.data["lat"] = suma_lat / dep.sub.size
        dep.data["lon"] = suma_lon / dep.sub.size
        dep = dep.next

    return pais


# -----------------------------------------------------------------------------
# imprimir_arbol: muestra la multilista con el formato del enunciado
#   ├── para los que tienen hermanos después, └── para el último
# -----------------------------------------------------------------------------
def imprimir_arbol(pais, max_municipios=None):
    print(pais.data["nombre"])
    dep = pais.sub.head
    while dep != None:
        ultimo_dep = dep.next == None
        rama = "└── " if ultimo_dep else "├── "
        print(rama + "Departamento: " + dep.data["nombre"])

        # sangría: si el departamento no es el último, se sigue la línea vertical
        sangria = "     " if ultimo_dep else "│    "
        mun = dep.sub.head
        contador = 0
        while mun != None:
            if max_municipios != None and contador == max_municipios:
                print(sangria + "└── ... (" + str(dep.sub.size - contador) + " más)")
                break
            rama_m = "└── " if mun.next == None else "├── "
            print(sangria + rama_m + "Municipio: " + mun.data["nombre"])
            contador = contador + 1
            mun = mun.next
        dep = dep.next


# -----------------------------------------------------------------------------
# a_diccionario: convierte la multilista a diccionarios/listas de Python
# para poder enviarla como JSON desde Flask (recorriendo con while).
# -----------------------------------------------------------------------------
def a_diccionario(nodo):
    resultado = dict(nodo.data)        # copia de los datos del nodo
    if nodo.sub != None:
        hijos = []
        current = nodo.sub.head
        while current != None:
            hijos.append(a_diccionario(current))   # recursivo: cada hijo con sus hijos
            current = current.next
        resultado["hijos"] = hijos
    return resultado


# Si se ejecuta este archivo directamente, imprime el árbol en consola
if __name__ == "__main__":
    colombia = construir_multilista("DIVIPOLA.csv")
    imprimir_arbol(colombia, max_municipios=3)   # pon None para ver todos
    print()
    print("Departamentos:", colombia.sub.size)
    total = 0
    dep = colombia.sub.head
    while dep != None:
        total = total + dep.sub.size
        dep = dep.next
    print("Municipios:", total)
