<template>
  <Line :data="chartData" :options="chartOptions" />
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
      beginAtZero: false
    }
  }
}
</script>