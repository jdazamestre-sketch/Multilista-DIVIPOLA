// =============================================================================
// universal.js  (como en la guía): crea el mapa de Leaflet y la capa base
// de OpenStreetMap. La plantilla index.html agrega luego los marcadores.
// =============================================================================

// Mapa dentro del div #map, centrado en Colombia
const map = L.map("map").setView([4.6, -74.1], 6);

// Capa de mosaicos (tiles) de OpenStreetMap con su atribución
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Capa donde se dibujan los municipios del departamento seleccionado
const capaMunicipios = L.layerGroup().addTo(map);

// Marcadores de municipios por departamento: { "05": [ {marker, li}, ... ] }
const municipiosPorDep = {};

// Muestra en el mapa y en el panel los municipios del departamento elegido
function seleccionarDepartamento(codigo) {
  const yaAbierto = document.getElementById("dep-" + codigo).classList.contains("abierto");

  // se cierran todos los departamentos del panel y se limpia el mapa
  document.querySelectorAll(".dep").forEach(d => d.classList.remove("abierto"));
  capaMunicipios.clearLayers();
  if (yaAbierto) return;            // segundo clic: solo cierra

  const item = document.getElementById("dep-" + codigo);
  item.classList.add("abierto");    // el CSS muestra su lista de municipios

  const puntos = [];
  municipiosPorDep[codigo].forEach(m => {
    m.marker.addTo(capaMunicipios);
    puntos.push(m.marker.getLatLng());
  });
  map.fitBounds(puntos, { padding: [30, 30], maxZoom: 11 });
  item.scrollIntoView({ block: "nearest" });
}

// Clic en un municipio del panel: centra el mapa y abre su popup
function seleccionarMunicipio(codigoDep, indice) {
  const m = municipiosPorDep[codigoDep][indice].marker;
  map.setView(m.getLatLng(), 11);
  m.openPopup();
}
