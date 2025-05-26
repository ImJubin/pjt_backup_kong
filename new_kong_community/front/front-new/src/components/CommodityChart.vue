<script setup>
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { ref, watch } from "vue";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
);

const props = defineProps(["data"]);

const chartData = ref({
  labels: [],
  datasets: [],
});

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: { position: "top" },
    title: {
      display: true,
      text: "상품 시세 차트",
    },
  },
});

// ✅ props.data가 바뀔 때마다 chartData 업데이트
watch(
  () => props.data,
  (newData) => {
    chartData.value = {
      labels: newData.map((d) => new Date(d.x).toLocaleTimeString()),
      datasets: [
        {
          label: "Price",
          data: newData.map((d) => d.y),
          fill: false,
          borderColor: "rgba(75, 192, 192, 1)",
          tension: 0.1,
        },
      ],
    };
  },
  { immediate: true }
);
</script>

<template>
  <div>
    <Line :data="chartData" :options="chartOptions" class="mb-6" />

    <table class="table-auto text-sm mt-4 border rounded shadow w-full">
      <thead>
        <tr class="bg-gray-100 text-left">
          <th class="px-4 py-2 border">시간</th>
          <th class="px-4 py-2 border">가격</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, idx) in data" :key="idx">
          <td class="px-4 py-1 border">
            {{ new Date(item.x).toLocaleString("ko-KR") }}
          </td>
          <td class="px-4 py-1 border">{{ item.y.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
