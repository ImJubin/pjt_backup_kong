<!-- components/ProductRecommendationCard.vue -->
<template>
  <div class="p-4 border rounded bg-white shadow hover:bg-gray-100 transition">
    <h3 class="font-bold text-lg mb-1">{{ product.fin_prdt_nm }}</h3>
    <p class="text-gray-700">{{ product.kor_co_nm }}</p>
    <p class="text-sm mt-1">이율: {{ product.intr_rate2 }}%</p>
    <p class="text-sm">예치 기간: {{ product.save_trm }}개월</p>
    <p class="text-sm font-semibold text-green-700">
      예상 수익: {{ product.predicted_profit.toLocaleString() }}원
    </p>
  </div>
</template>

<script setup>
defineProps({
  product: Object
})
</script>
