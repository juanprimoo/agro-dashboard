<template>
  <div id="map" class="w-full h-[500px]"></div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import brazilGeoJSON from "../utils/brazil-states.json"; 

export default {
	props: { data: Object,highlight: [Number, String] },
	emits: ["regionSelected"],
	setup(props, { emit }) {
		const map = ref(null);
		const geojsonLayer = ref(null);

		// Função para definir cor de acordo com valor
		function getColor(valor) {
			if (valor > 50000000) 
				return "#00441b"; 
			if (valor > 10000000) 
				return "#006d2c";
			if (valor > 1000000)  
				return "#238b45";
			if (valor > 100000)
				return "#41ab5d";
			if (valor > 0)
				return "#74c476";
			return "#e5f5e0";
		}

		function alteraCorEstado(feature) {
			const id = feature.properties.codigo_ibge.toString();
			const valor = props.data[id] || 0;

			return {
				fillColor: props.highlight === id ? "#ffeb3b" : getColor(valor),
				weight: props.highlight?.toString() === id ? 3 : 1,
				color: "white",
				fillOpacity: 0.7
			};
		}

		function onEachFeature(feature, layer) {
			layer.on({
					click: () => {
					emit("regionSelected", feature.properties.codigo_ibge);
				}
			});
		}

		onMounted(() => {
			map.value = L.map("map").setView([-14, -52], 4);

			L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
				attribution: "&copy; OpenStreetMap contributors"
			}).addTo(map.value);

			geojsonLayer.value = L.geoJSON(brazilGeoJSON, { style: alteraCorEstado,onEachFeature}).addTo(map.value);
		});

		
		function updateLayerStyles() {
			if (!geojsonLayer.value) return;

			geojsonLayer.value.eachLayer((layer) => {
				const id = layer.feature.properties.codigo_ibge.toString();
				const valor = props.data[id] || 0;

				layer.setStyle({
					fillColor: props.highlight?.toString() === id ? "#ff7f0e" : getColor(valor),
					weight: props.highlight?.toString() === id ? 3 : 1,
					color: "white",
					fillOpacity: 0.7
				});
			});
		}

		// Watch para reagir a mudanças em highlight ou data
		watch(
			[() => props.highlight, () => props.data],
			() => {
				updateLayerStyles();
			}, {
				deep: true
			}
		);

		return {};
	}
};
</script>
