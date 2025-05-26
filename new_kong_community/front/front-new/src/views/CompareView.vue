<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">상품 시세 비교</h2>

    <select v-model="selected" @change="updateChart">
      <option value="GLD">Gold</option>
      <option value="SLV">Silver</option>
      <option value="CPER">Copper</option>
    </select>

    <CommodityChart :data="store.data" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCommodityStore } from '@/stores/CommodityStore'
import CommodityChart from '@/components/CommodityChart.vue'

const store = useCommodityStore()
const selected = ref('GLD')

const updateChart = () => {
  store.fetchCommodityHistory(selected.value)
}

onMounted(updateChart)
</script>