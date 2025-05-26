<template>
  <div>
    <pre>{{ data }}</pre> <!-- ✅ 여기에 디버깅용으로 출력 -->
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend)

const props = defineProps(['data'])

const chartData = {
  labels: props.data.map(d => new Date(d.x).toLocaleString()),
  datasets: [{
    label: 'Price',
    data: props.data.map(d => d.y),
    fill: false,
    tension: 0.1
  }]
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: true }
  },
  scales: {
    y: {
      beginAtZero: false,
      min: 0,           // 👈 이거 추가!
      suggestedMax: 100 // 👈 이거도 추가해서 더 넓게 보기
    }
  }
}
</script>