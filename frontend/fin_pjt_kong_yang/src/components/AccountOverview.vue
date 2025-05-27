<template>
  <div class="p-4 bg-gray-100 rounded">
    <h2 class="font-bold text-lg mb-2">내 계좌 현황</h2>

    <div v-if="store.accounts.length">
      <div
        v-for="account in store.accounts"
        :key="account.id"
        class="mb-4 p-3 bg-white rounded shadow"
      >
        <h3 class="text-md font-semibold">
          {{ account.alias_name || account.account_number }}
          <span class="text-xs text-gray-500">({{ account.account_type }})</span>
        </h3>
        <p>은행: {{ account.bank_name }}</p>
        <p>잔액: {{ account.current_balance.toLocaleString() }}원</p>

        <!-- 예금 상세 -->
        <div v-if="account.deposit_detail">
          <p>상품명: {{ account.deposit_detail.product_name }}</p>
          <p>이율: {{ account.deposit_detail.interest_rate }}%</p>
          <p>기간: {{ account.deposit_detail.duration_months }}개월</p>
          <p>시작일: {{ account.deposit_detail.started_at }}</p>
          <p>만기일: {{ account.deposit_detail.ends_at }}</p>
          <!-- <p>누적 이자: {{ account.deposit_detail.interest_accumulated.toLocaleString() }}원</p> -->
          <p>
            누적 이자:
            {{ parseFloat(account.deposit_detail.simulated_interest || account.deposit_detail.interest_accumulated).toLocaleString() }}원
          </p>

        </div>

        <!-- 적금 상세 -->
        <div v-else-if="account.savings_detail">
          <p>상품명: {{ account.savings_detail.product_name }}</p>
          <p>이율: {{ account.savings_detail.interest_rate }}%</p>
          <p>기간: {{ account.savings_detail.duration_months }}개월</p>
          <p>시작일: {{ account.savings_detail.started_at }}</p>
          <p>계약 만기일: {{ account.savings_detail.ends_at }}</p>
          <p>총 회차: {{ account.savings_detail.total_round }}</p>
          <p>목표 금액: {{ account.savings_detail.goal_amount.toLocaleString() }}원</p>
          <!-- <p>누적 이자: {{ account.savings_detail.interest_accumulated.toLocaleString() }}원</p> -->
          <p>
            누적 이자:
            {{ parseFloat(account.savings_detail.simulated_interest || account.savings_detail.interest_accumulated).toLocaleString() }}원
          </p>
          
          

          <p>계약 수령일: {{ account.savings_detail.contract_receive_date }}</p>
          <p>예상 수령일: {{ account.savings_detail.expected_receive_date }}</p>
          <p>납입 상태: {{ account.savings_detail.delay_label }}</p>
          <p>누적 연체일: {{ account.savings_detail.accumulated_delay_days }}일</p>
          <p>상태: {{ account.savings_detail.delay_status }}</p>
          <p>예상 만기일: {{ account.savings_detail.calculated_ends_at }}</p>
          <p>연체 개월: {{ account.savings_detail.delay_months }}개월</p>

          <p v-if="account.savings_detail.payments.length">
            최근 불입일: {{ account.savings_detail.payments.at(-1).paid_at }}
          </p>
          <p v-if="account.savings_detail.payments.length">
            현재 회차: {{ account.savings_detail.payments.at(-1).round_number }}
          </p>

          <!-- 납입 이력 전체 -->
          <div class="mt-2 p-2 border rounded bg-gray-50">
            <p class="font-semibold text-sm">납입 이력</p>
            <ul>
              <li
                v-for="payment in account.savings_detail.payments"
                :key="payment.id"
              >
                {{ payment.round_number }}회차 - {{ payment.paid_at }} - {{ payment.amount.toLocaleString() }}원
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <p>계좌 정보가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'  // 마운트 시점에서 비동기 작업 실행용
import { useAccountStore } from '@/stores/userAccount'  // 계좌 정보 Pinia 스토어

import axios from 'axios'

const store = useAccountStore()

// ✅ 실시간 이자 시뮬레이션 함수
const startInterestSimulation = function(detail) {
  if (!detail || !detail.started_at || !detail.ends_at || !detail.interest_total) return

  const start = new Date(detail.started_at)
  const end = new Date(detail.ends_at)
  const totalSeconds = (end - start) / 1000

  const totalInterest = parseFloat(detail.interest_total)
  const interestPerSecond = totalInterest / totalSeconds
  let simulatedInterest = parseFloat(detail.interest_accumulated)

  detail.simulated_interest = simulatedInterest.toFixed(2)

  setInterval(function() {
    simulatedInterest += interestPerSecond
    detail.simulated_interest = simulatedInterest.toFixed(2)
  }, 1000)
}

// ✅ 컴포넌트가 마운트되면 실행
onMounted(async function() {
  const token = sessionStorage.getItem('authToken')

  try {
    // 0. 누적 이자 서버에서 갱신
    await axios.post('http://127.0.0.1:8000/users/update-interest/', {}, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 1. 계좌 정보 불러오기
    await store.fetchAccounts()

    // 2. 각 계좌에 대해 실시간 이자 시뮬레이션 시작
    store.accounts.forEach(function(acc) {
      if (acc.savings_detail) startInterestSimulation(acc.savings_detail)
      if (acc.deposit_detail) startInterestSimulation(acc.deposit_detail)
    })

  } catch (err) {
    console.error('이자 갱신 또는 계좌 조회 실패:', err)
  }
})
</script>



<!-- <script setup>
import { onMounted } from 'vue'  // 마운트 시점에서 비동기 작업 실행용
import { useAccountStore } from '@/stores/userAccount'  // 계좌 정보 Pinia 스토어
import AccountAddForm from '@/components/AccountAddForm.vue'  // 계좌 추가 폼 컴포넌트

// Pinia 스토어에서 계좌 목록 가져오기
const store = useAccountStore()

// ✅ 실시간 이자 시뮬레이션 함수 (표현식 함수 방식)
const startInterestSimulation = function(detail) {
  // detail이 비어있거나 필수 정보 없으면 실행 안 함 (예외 방지용)
  if (!detail || !detail.started_at || !detail.ends_at || !detail.interest_total) return

  // 시작일과 만기일로 전체 기간 계산 (초 단위)
  const start = new Date(detail.started_at)
  const end = new Date(detail.ends_at)
  const totalSeconds = (end - start) / 1000  // 예: 6개월 → 약 15만 초

  // 전체 받을 이자
  const totalInterest = parseFloat(detail.interest_total)

  // ✅ 1초마다 증가할 이자량 계산
  const interestPerSecond = totalInterest / totalSeconds

  // 현재 누적 이자에서 시작
  let simulatedInterest = parseFloat(detail.interest_accumulated)

  // 초기 표시값 설정
  detail.simulated_interest = simulatedInterest.toFixed(2)

  // ✅ 1초마다 interestPerSecond 만큼 이자 증가
  setInterval(function() {
    simulatedInterest += interestPerSecond
    detail.simulated_interest = simulatedInterest.toFixed(2)
  }, 1000)  // 1000ms = 1초
}

// ✅ 컴포넌트가 마운트되면 실행
onMounted(async function() {
  // 1. 서버에서 계좌 정보 불러오기
  await store.fetchAccounts()

  // 2. 모든 계좌에 대해 실시간 이자 시뮬레이션 시작
  store.accounts.forEach(function(acc) {
    if (acc.savings_detail) startInterestSimulation(acc.savings_detail)  // 적금용
    if (acc.deposit_detail) startInterestSimulation(acc.deposit_detail)  // 예금용
  })

  // // 3. (선택사항) 1분마다 실제 서버 값으로 갱신하려면 아래 주석 해제
  // setInterval(async function() {
  //   await store.fetchAccounts()
  //   console.log('new')
  // }, 60000)
})
</script> -->




<!-- <script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/userAccount'
import AccountAddForm from '@/components/AccountAddForm.vue'

const store = useAccountStore()

onMounted(async () => {
  // ✅ 1. 최초 데이터 로딩
  await store.fetchAccounts()

  // ✅ 2. 실제 이자 반영을 위한 갱신 - 10초마다 서버에서 다시 가져오기
  setInterval(async () => {
    await store.fetchAccounts()
  }, 10000) // 10000ms = 10초
})
</script> -->
<!-- 
<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/userAccount'
import AccountAddForm from '@/components/AccountAddForm.vue'

const store = useAccountStore()

// ✨ 누적 이자 시뮬레이션 (10초 단위로 계산된 이자 증가)
function startInterestSimulation(account) {
  const detail = account.savings_detail
  if (!detail) return

  const start = new Date(detail.started_at)
  const end = new Date(detail.ends_at)
  const now = new Date()

  const totalSeconds = (end - start) / 1000
  const totalInterest = parseFloat(detail.interest_total)

  // 누적 이자 증가량 (10초당)
  const interestPer10s = totalInterest / (totalSeconds / 10)
  let simulatedInterest = parseFloat(detail.interest_accumulated)

  detail.simulated_interest = simulatedInterest.toFixed(2)

  setInterval(() => {
    simulatedInterest += interestPer10s
    detail.simulated_interest = simulatedInterest.toFixed(2)
  }, 10000)
}

onMounted(async () => {
  // 1. 최초 데이터 로딩
  await store.fetchAccounts()

  // 2. 모든 적금에 대해 시뮬레이션 시작
  store.accounts.forEach(acc => {
    if (acc.savings_detail) {
      startInterestSimulation(acc)
    }
  })

  // // 3. 10초마다 서버에서 최신 데이터 fetch (안 해도 OK)
  // setInterval(async () => {
  //   await store.fetchAccounts()
  // }, 60000)  // 1분마다 실제 DB 이자 갱신 fetch (선택사항)
})
</script> -->

<!-- 
<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/userAccount'
import AccountAddForm from '@/components/AccountAddForm.vue'

const store = useAccountStore()

// 🔁 공통 이자 시뮬레이션 함수 (적금 또는 예금 모두 사용 가능)
function startInterestSimulation(detail, type) {
  if (!detail || !detail.started_at || !detail.ends_at || !detail.interest_total) return

  const start = new Date(detail.started_at)
  const end = new Date(detail.ends_at)
  const totalSeconds = (end - start) / 1000
  const totalInterest = parseFloat(detail.interest_total)
  const interestPer10s = totalInterest / (totalSeconds / 10)

  let simulatedInterest = parseFloat(detail.interest_accumulated)
  detail.simulated_interest = simulatedInterest.toFixed(2)

  setInterval(() => {
    simulatedInterest += interestPer10s
    detail.simulated_interest = simulatedInterest.toFixed(2)
  }, 10000) // 10초마다
}

onMounted(async () => {
  // 1. 계좌 데이터 불러오기
  await store.fetchAccounts()

  // 2. 모든 계좌에 대해 이자 시뮬레이션 시작
  store.accounts.forEach(acc => {
    if (acc.savings_detail) startInterestSimulation(acc.savings_detail, 'savings')
    if (acc.deposit_detail) startInterestSimulation(acc.deposit_detail, 'deposit')
  })

  // // 3. 1분마다 서버로부터 실제 값 fetch (선택 사항)
  // setInterval(async () => {
  //   await store.fetchAccounts()
  // }, 60000)
})
</script> -->

