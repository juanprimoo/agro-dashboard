<template>
    <div>
        <h3 class="text-lg font-semibold mb-2">{{ titulo }}</h3>
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<script>
import { onMounted, ref, watch } from "vue";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  props: {
    dados: {
      type: Array,
      required: true
    },
    titulo: {
      type: String,
      default: "Gráfico"
    }
  },
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null;

    function criarGrafico() {
      if (!chartCanvas.value) return;

      const labels = props.dados.map(item => item.descricao_produto);
      const valores = props.dados.map(item => item.valor_producao);

      if (chartInstance) {
        chartInstance.destroy();
      }

      chartInstance = new Chart(chartCanvas.value, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Valor de Produção (R$)",
              data: valores,
              backgroundColor: "#4CAF50" // verde para combinar com o tema
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return new Intl.NumberFormat("pt-BR", {
                    style: "currency",
                    currency: "BRL"
                  }).format(context.raw);
                }
              }
            }
          },
          scales: {
            y: {
              ticks: {
                callback: function(value) {
                  return new Intl.NumberFormat("pt-BR", {
                    style: "currency",
                    currency: "BRL"
                  }).format(value);
                }
              }
            }
          }
        }
      });
    }

    onMounted(criarGrafico);

    watch(() => props.dados, criarGrafico, { deep: true });

    return { chartCanvas };
  }
};
</script>

<style>
canvas {
  width: 100% !important;
  height: 500px !important;
}
</style>
