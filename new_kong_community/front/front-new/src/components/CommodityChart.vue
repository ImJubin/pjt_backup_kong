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

const formatDateTime = (iso) => {
  return new Date(iso).toLocaleString("ko-KR", {
    dateStyle: "short",
    timeStyle: "medium",
  });
};

const formatDate = (iso) => {
  const d = new Date(iso);
  return `${d.getFullYear()}. ${d.getMonth() + 1}. ${d.getDate()}`;
};

const isDateChanged = (prevIso, currIso) => {
  return formatDate(prevIso) !== formatDate(currIso);
};

const isPriceUp = (idx) => {
  return idx > 0 && props.data[idx].y > props.data[idx - 1].y;
};

const isPriceDown = (idx) => {
  return idx > 0 && props.data[idx].y < props.data[idx - 1].y;
};

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

    <div class="max-h-64 overflow-y-auto border rounded shadow">
      <table class="w-full text-sm table-auto">
        <thead class="sticky top-0 bg-white z-10">
          <tr class="bg-gray-100 text-left">
            <th class="px-4 py-2 border">🕒 시간</th>
            <th class="px-4 py-2 border">💰 가격</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(item, idx) in data" :key="idx">
            <!-- 날짜가 바뀌면 구분선 -->
            <tr v-if="idx > 0 && isDateChanged(data[idx - 1].x, item.x)">
              <td
                colspan="2"
                class="text-xs text-gray-500 text-center bg-gray-50 border-y py-1"
              >
                📅 {{ formatDate(item.x) }}
              </td>
            </tr>

            <tr>
              <td class="px-4 py-1 border">{{ formatDateTime(item.x) }}</td>
              <td
                class="px-4 py-1 border font-semibold"
                :class="{
                  'text-red-500': isPriceUp(idx),
                  'text-blue-600': isPriceDown(idx),
                }"
              >
                {{ item.y.toFixed(2) }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>
