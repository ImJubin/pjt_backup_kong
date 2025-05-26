<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { ref, watch } from 'vue'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const props = defineProps(['data'])

const chartData = ref({
  labels: [],
  datasets: [],
})

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: {
      display: true,
      text: '상품 시세 차트',
    },
  },
})

// ✅ props.data가 바뀔 때마다 chartData 업데이트
watch(
  () => props.data,
  (newData) => {
    chartData.value = {
      labels: newData.map(d => new Date(d.x).toLocaleTimeString()),
      datasets: [
        {
          label: 'Price',
          data: newData.map(d => d.y),
          fill: false,
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.1,
        },
      ],
    }
  },
  { immediate: true }
)
</script>

<template>
  <div>
    <pre>{{ data }}</pre>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>