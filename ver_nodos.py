# =============================================================================
# ver_nodos.py
# Muestra la multilista "por dentro": cada nodo con su data, su next y su sub.
# =============================================================================
from multilista import construir_multilista, imprimir_arbol

colombia = construir_multilista("DIVIPOLA.csv")


# Devuelve el nombre del nodo o "None" (para mostrar a dónde apunta next/sub)
def nombre(nodo):
    if nodo == None:
        return "None"
    return nodo.data["nombre"]


print("=" * 70)
print(" 1) NODO RAÍZ")
print("=" * 70)
print("Node(data =", colombia.data, ")")
print("   next ->", nombre(colombia.next))
print("   sub  -> LinkedList(head =", nombre(colombia.sub.head),
      ", tail =", nombre(colombia.sub.tail), ", size =", colombia.sub.size, ")")

print()
print("=" * 70)
print(" 2) SUBLISTA DE DEPARTAMENTOS (cada nodo y sus punteros)")
print("=" * 70)
dep = colombia.sub.head
i = 1
while dep != None:
    print(str(i).rjust(2) + ". [" + dep.data["codigo"] + "] " + dep.data["nombre"])
    print("      next -> " + nombre(dep.next))
    print("      sub  -> LinkedList(head = " + nombre(dep.sub.head) +
          ", tail = " + nombre(dep.sub.tail) + ", size = " + str(dep.sub.size) + ")")
    dep = dep.next
    i = i + 1

print()
print("=" * 70)
print(" 3) EJEMPLO: SUBLISTA DE MUNICIPIOS DE ATLÁNTICO, NODO POR NODO")
print("=" * 70)
atl = colombia.sub.search("codigo", "08")
mun = atl.sub.head
while mun != None:
    print("Node(data =", mun.data, ")")
    print("      next ->", nombre(mun.next))
    mun = mun.next

print()
print("=" * 70)
print(" 4) ÁRBOL COMPLETO DE LA MULTILISTA")
print("=" * 70)
imprimir_arbol(colombia)   # sin límite: todos los municipios
