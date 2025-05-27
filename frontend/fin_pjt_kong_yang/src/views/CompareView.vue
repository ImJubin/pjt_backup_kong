<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">📊 상품 시세 비교</h2>

    <select v-model="selected" @change="updateChart">
      <option value="GLD">Gold</option>
      <option value="SLV">Silver</option>
      <option value="CPER">Copper</option>
    </select>

    <CommodityChart :data="store.data" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCommodityStore } from "@/stores/CommodityStore";
import CommodityChart from "@/components/CommodityChart.vue";

const store = useCommodityStore();
const selected = ref("GLD");

const updateChart = () => {
  store.fetchCommodityHistory(selected.value);
};

onMounted(updateChart);
</script>

<style scoped>
.chart-wrapper {
  font-family: "Noto Sans KR", sans-serif;
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 0 auto;
}

.chart-wrapper h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

select {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
}
</style>
