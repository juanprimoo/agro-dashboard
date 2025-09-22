<template>
	<header class="w-full py-4 px-6 flex items-center justify-between shadow-md" style="background-color: #25341e;">
		<div class="flex items-center space-x-3">
			<img src="@/assets/logo.svg" alt="E-Safra" class="h-12 w-12" />
			<h1 class="text-white text-xl font-bold ml-4">E-Safra Dashboard</h1>
		</div>
	</header>

	<div class="p-4 space-y-6">
		<div class="text-lg font-semibold">
			<span>
				Dados Lavouras permanentes
			</span>

			<span @click="selectedEstado = null" class="cursor-pointer hover:underline">
				/ Brasil
			</span>

			<span v-if="selectedEstado"> / {{ selectedEstado.estado }}</span>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-5 gap-4">
			<div class="bg-green-100 p-4 rounded shadow">
				<h3 class="text-sm font-medium text-green-800">
					Valor de Produção
				</h3>

				<p class="text-xl font-bold text-green-900">
					{{ formatarMoeda(valorProducaoExibido) }}
				</p>
			</div>

			<div class="bg-green-100 p-4 rounded shadow">
				<h3 class="text-sm font-medium text-green-800">
					Área Destinada
				</h3>

				<p class="text-xl font-bold text-green-900">
					{{ formatarArea(areaDestinadaExibida) }}
				</p>
			</div>

			<div class="bg-green-100 p-4 rounded shadow">
				<h3 class="text-sm font-medium text-green-800">
					Área Colhida
				</h3>

				<p class="text-xl font-bold text-green-900">
					{{ formatarArea(areaColhidaExibida) }}
				</p>
			</div>

			<div class="bg-green-100 p-4 rounded shadow">
				<h3 class="text-sm font-medium text-green-800">
					Maior Rendimento
				</h3>

				<p class="text-xl font-bold text-green-900" v-if="culturaMaiorRendimento">
					{{ culturaMaiorRendimento.descricao_produto }}<br>
					{{ formatarInteiro(culturaMaiorRendimento.rendimento) }} kg/ha
				</p>

				<p class="text-xl font-bold text-green-900" v-else>-</p>
			</div>

			<div class="bg-green-100 p-4 rounded shadow">
				<h3 class="text-sm font-medium text-green-800">
					Maior Valor Produção
				</h3>

				<p class="text-xl font-bold text-green-900" v-if="culturaMaiorValor">
					{{ culturaMaiorValor.descricao_produto }}<br>
					{{ formatarMoeda(culturaMaiorValor.valor_producao) }}
				</p>

				<p class="text-xl font-bold text-green-900" v-else>-</p>
			</div>
		</div>

		<div class="mb-4">
			<label class="block mb-1 font-medium">Selecione o estado:</label>
			<select v-model="selectedEstadoId" @change="onEstadoChange" class="border rounded p-2 w-full md:w-64">
				<option value="">
					Brasil
				</option>
				
				<option v-for="estado in estados" :key="estado.id" :value="estado.id">
					{{ estado.nome }}
				</option>
			</select>
  		</div>
		
		<div class="flex gap-4">
			<div class="flex-1">
				<MapView :data="mapData" :highlight="selectedEstado?.id_estado ?? null" @regionSelected="selectRegion"/>
			</div>

			<div class="flex-1 bg-white p-4 rounded shadow">
				<ChartView :dados="culturasExibidas" titulo="Valor de Produção" />
			</div>
		</div>

		<div class="bg-white rounded shadow p-4 overflow-auto">
			<table class="w-full table-auto">
				<thead class="bg-gray-100">
					<tr>
						<th class="px-4 py-2 text-left">Produto</th>
						<th class="px-4 py-2 text-right">Área Destinada</th>
						<th class="px-4 py-2 text-right">Área Colhida</th>
						<th class="px-4 py-2 text-right">Quantidade Produzida (Toneladas)</th>
						<th class="px-4 py-2 text-right">Rendimento (kg/ha)</th>
						<th class="px-4 py-2 text-right">Valor Produção</th>
					</tr>
				</thead>

				<tbody>
					<tr v-for="item in culturasExibidas" :key="item.descricao_produto" class="border-b hover:bg-gray-50">
						<td class="px-4 py-2">{{ item.descricao_produto }}</td>
						<td class="px-4 py-2 text-right">{{ formatarArea(item.area_destinada, item.unidade_medida) }}</td>
						<td class="px-4 py-2 text-right">{{ formatarArea(item.area_colhida, item.unidade_medida) }}</td>
						<td class="px-4 py-2 text-right">{{ formatarInteiro(item.quantidade_produzida) }}</td>
						<td class="px-4 py-2 text-right">{{ formatarInteiro(item.rendimento) }}</td>
						<td class="px-4 py-2 text-right">{{ formatarMoeda(item.valor_producao) }}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import MapView from "@/components/MapView.vue";
import ChartView from "@/components/ChartView.vue";
import { getDadosLavourasPermanentes } from "@/services/api.js";
import { formatarMoeda, formatarArea, formatarInteiro } from "@/utils/funcoes.js";
import { selectEstado, calcularNacional, maiorRendimento, maiorValor } from "@/utils/dashboardData.js";
import estadosCoordenadas from "@/utils/estadosCoordenadas.js";

export default {
  components: { MapView, ChartView },
  setup() {
    const dados = ref([]);
    const selectedEstado = ref(null);
    const estados = ref(estadosCoordenadas);
    const selectedEstadoId = ref(""); // para o select

	async function carregarDados() {
		dados.value = await getDadosLavourasPermanentes();
	}

    function selectRegion(id_estado) {
      selectedEstado.value = selectEstado(dados.value, id_estado);
      selectedEstadoId.value = id_estado || ""; // mantém select sincronizado
    }

    function onEstadoChange() {
      if (selectedEstadoId.value === "") {
        selectRegion(null); // nível nacional
      } else {
        selectRegion(selectedEstadoId.value);
      }
    }

    const mapData = computed(() => {
      const obj = {};
      dados.value.forEach((estado) => {
        obj[estado.id_estado] = estado.total?.valor_producao || 0;
      });
      return obj;
    });

    const culturasExibidas = computed(() => {
      if (selectedEstado.value) return selectedEstado.value.cultura.slice(1).filter(c => c.valor_producao > 0);
      return calcularNacional(dados.value);
    });

    const culturaMaiorRendimento = computed(() => {
      const lista = selectedEstado.value ? selectedEstado.value.cultura.slice(1) : calcularNacional(dados.value);
      return maiorRendimento(lista);
    });

    const culturaMaiorValor = computed(() => {
      const lista = selectedEstado.value ? selectedEstado.value.cultura.slice(1) : calcularNacional(dados.value);
      return maiorValor(lista);
    });

    const valorProducaoExibido = computed(() =>
      selectedEstado.value ? selectedEstado.value.total?.valor_producao || 0 :
      dados.value.reduce((acc, e) => acc + (e.total?.valor_producao || 0), 0)
    );

    const areaDestinadaExibida = computed(() =>
      selectedEstado.value ? selectedEstado.value.cultura[0]?.area_destinada || 0 :
      dados.value.reduce((acc, e) => acc + (e.cultura[0]?.area_destinada || 0), 0)
    );

    const areaColhidaExibida = computed(() =>
      selectedEstado.value ? selectedEstado.value.cultura[0]?.area_colhida || 0 :
      dados.value.reduce((acc, e) => acc + (e.cultura[0]?.area_colhida || 0), 0)
    );

    onMounted(carregarDados);

    return {
      dados,
      selectedEstado,
      selectedEstadoId,
      estados,
      selectRegion,
      onEstadoChange,
      mapData,
      culturasExibidas,
      valorProducaoExibido,
      areaDestinadaExibida,
      areaColhidaExibida,
      culturaMaiorRendimento,
      culturaMaiorValor,
      formatarMoeda,
      formatarArea,
      formatarInteiro
    };
  }
};
</script>

