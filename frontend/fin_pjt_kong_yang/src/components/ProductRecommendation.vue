<template>
  <div class="p-4 bg-gray-100 rounded">
    <!-- 추천 카드 먼저 -->
    <div v-if="recommendations.length" class="mb-6">
      <h2 class="text-xl font-bold mb-4">✨추천 상품</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ProductRecommendationCard
          v-for="product in recommendations"
          :key="product.id + '-' + product.save_trm"
          :product="product"
        />
      </div>
    </div>


  </div>
</template>

<script setup>
import { watch, onMounted, ref } from 'vue'
import axios from 'axios'
import ProductRecommendationCard from './ProductRecommendationCard.vue'
import { useAccountStore } from '@/stores/userAccount'
import { useAmountStore } from '@/stores/amountCalculate'

const API_URL = 'http://127.0.0.1:8000'
const recommendations = ref([])
const amountStore = useAmountStore()
const accountStore = useAccountStore()

// 서버에 추천 상품 요청
const fetchRecommendation = async (amount = null) => {
  try {
    const token = sessionStorage.getItem('authToken')
    const res = await axios.post(`${API_URL}/products/recommend/`, {
      amount
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    recommendations.value = res.data
  } catch (err) {
    console.error('추천 요청 실패:', err)
  }
}

// 🔁 금액이 바뀔 때마다 추천 요청
watch(() => amountStore.amount, (newAmount) => {
  if (newAmount && newAmount > 0) {
    fetchRecommendation(newAmount)
  }
})

// 🔁 초기 진입 시 유저 계좌 기반 금액 + 추천 요청
onMounted(async () => {
  if (!amountStore.amount) {
    await amountStore.fetchInitialAmount()
  }
  fetchRecommendation(amountStore.amount)
})
</script>
