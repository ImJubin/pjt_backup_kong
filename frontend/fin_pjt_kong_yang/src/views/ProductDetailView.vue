<!-- <template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-2">상품 상세 정보</h2>
    <div v-if="product">
      <p><strong>상품명:</strong> {{ product.fin_prdt_nm }}</p>
      <p><strong>은행:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>이율:</strong> {{ product.bestRate }}%</p>
      <p><strong>설명:</strong> {{ product.description || '설명 없음' }}</p> -->
      <!-- 기타 항목들... -->
    <!-- </div>
    <div v-else class="text-gray-500">로딩 중...</div>
  </div>
</template> -->

<!-- <script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const product = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/products/${route.params.type}/${route.params.id}/`)
    product.value = res.data
  } catch (err) {
    error.value = '상품을 불러오는 데 실패했습니다.'
  }
})

</script> -->


<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">상품 상세 정보</h2>

    <div v-if="product">
      <p><strong>상품명:</strong> {{ product.fin_prdt_nm }}</p>
      <p><strong>은행:</strong> {{ product.kor_co_nm }}</p>
      <p><strong>금융상품 코드:</strong> {{ product.fin_prdt_cd }}</p>
      <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
      <p><strong>만기 후 이자율:</strong> {{ product.mtrt_int }}</p>
      <p><strong>우대 조건:</strong> {{ product.spcl_cnd || '없음' }}</p>
      <p><strong>가입 대상:</strong> {{ product.join_member }}</p>
      <p><strong>기타 유의사항:</strong> {{ product.etc_note || '없음' }}</p>
      <p><strong>최고 한도:</strong> {{ product.max_limit ? product.max_limit + '원' : '제한 없음' }}</p>
      <p><strong>공시 기간:</strong> {{ product.dcls_strt_day }} ~ {{ product.dcls_end_day || '제한 없음' }}</p>
      <p><strong>제출일:</strong> {{ product.fin_co_subm_day }}</p>

      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-2">금리 옵션</h3>
        <table class="w-full border">
          <thead class="bg-gray-100">
            <tr>
              <th class="p-2 border">유형</th>
              <th class="p-2 border">기간(개월)</th>
              <th class="p-2 border">기본 금리</th>
              <th class="p-2 border">최고 금리</th>
              <th v-if="product.options[0]?.rsrv_type_nm" class="p-2 border">적립 유형</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(opt, i) in product.options" :key="i">
              <td class="p-2 border">{{ opt.intr_rate_type_nm }}</td>
              <td class="p-2 border">{{ opt.save_trm }}</td>
              <td class="p-2 border">{{ opt.intr_rate != null ? opt.intr_rate + '%' : '-' }}</td>
              <td class="p-2 border">{{ opt.intr_rate2 != null ? opt.intr_rate2 + '%' : '-' }}</td>
              <td v-if="opt.rsrv_type_nm" class="p-2 border">{{ opt.rsrv_type_nm }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <PurchaseForm :product="product" :type="product.type" />
    </div>
    

    <div v-else class="text-gray-500">로딩 중...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import PurchaseForm from '@/components/PurchaseForm.vue'

const route = useRoute()
const product = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/products/${route.params.type}/${route.params.id}/`)
    product.value = res.data
  } catch (err) {
    console.error('상품 로드 실패', err)
  }
})
</script>
