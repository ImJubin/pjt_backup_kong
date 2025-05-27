<!-- <template>
  <div class="p-4 flex justify-center">
    <div class="calendar-card">
      <h2 class="text-xl font-bold mb-4 text-center">📅 예적금 일정 캘린더</h2>
      <v-calendar
        is-expanded
        mode="month"
        :attributes="store.calendarEvents"
        :now="new Date()" 
      />
      <v-calendar
      is-expanded
      mode="month"
      :attributes="store.calendarEvents"
      :now="new Date()"
      :from-page="{ month: new Date().getMonth() + 1, year: new Date().getFullYear() }"
    />
    </div>
  </div>
</template> -->

<template>
  <div class="p-4 flex justify-center">
    <div class="calendar-card">
      <h2 class="text-xl font-bold mb-4 text-center">📅 예적금 일정 캘린더</h2>
      <v-calendar
  is-expanded
  mode="month"
  :attributes="store.calendarEvents"
  :now="today"
  :from-page="{ month: today.getMonth() + 1, year: today.getFullYear() }"
  :model-value="today"
/>

    </div>
  </div>
</template>


<!-- <script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/userAccount'

const store = useAccountStore()

onMounted(async () => {
  console.log("브라우저 기준 오늘 날짜:", new Date())
  await store.fetchCalendarEvents()
  // await store.fetchCalendarEvents()
})
</script> -->
<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/userAccount'

const store = useAccountStore()

// ✅ "시분초 없는 오늘" 만들기
const today = new Date()
today.setHours(0, 0, 0, 0)

onMounted(async () => {
  console.log("브라우저 기준 오늘 날짜:", today)
  await store.fetchCalendarEvents()
})
</script>

<style scoped>
.calendar-card {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  max-width: 420px;
  width: 100%;
  padding: 24px;
}

/* ✅ 오늘 날짜 스타일: 최종 확실하게 적용되는 방식 */
::v-deep(.vc-day.today .vc-day-content) {
  background-color: black !important;
  color: white !important;
  border-radius: 9999px;
  padding: 6px 10px;
  font-weight: bold;
}

/* 일반 날짜 셀 스타일 */
::v-deep(.vc-day-content) {
  font-weight: 500;
  border-radius: 6px;
  padding: 6px;
  transition: background-color 0.2s ease;
}

::v-deep(.vc-day-content:hover) {
  background-color: #f3f4f6;
}

::v-deep(.today-highlight) {
  background-color: black !important;
  color: white !important;
  border-radius: 8px;
  /* padding: 4px 10px; */
  font-weight: bold;

  /* ✅ 깜빡임 제거 */
  transition: none !important;

  /* ✅ pill 찌그러짐 방지 */
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: auto;
  /* min-width: 2.2rem;
  height: 2.2rem; */

  
}

</style>
