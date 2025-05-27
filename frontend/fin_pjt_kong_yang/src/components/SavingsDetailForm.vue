<!-- src/components/SavingsDetailForm.vue -->
<script setup>
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const update = (key, value) => {
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: value,
  })
}
</script>

<template>
  <div class="mt-4">
    <h4 class="font-semibold mb-2">적금 상품 정보</h4>

    <div class="mb-2">
      <label>상품명</label>
      <input
        type="text"
        :value="modelValue.product_name"
        @input="update('product_name', $event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>금리 (%)</label>
      <input
        type="number"
        step="0.01"
        :value="modelValue.interest_rate"
        @input="update('interest_rate', +$event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>기간 (개월)</label>
      <input
        type="number"
        :value="modelValue.duration_months"
        @input="update('duration_months', +$event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>시작일</label>
      <input
        type="date"
        :value="modelValue.started_at"
        @input="update('started_at', $event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>만기일</label>
      <input
        type="date"
        :value="modelValue.ends_at"
        @input="update('ends_at', $event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>불입일</label>
      <input
        type="date"
        :value="modelValue.payment_date"
        @input="update('payment_date', $event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>현재 회차</label>
      <input
        type="number"
        :value="modelValue.round_number"
        @input="update('round_number', +$event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>총 회차</label>
      <input
        type="number"
        :value="modelValue.total_round"
        @input="update('total_round', +$event.target.value)"
        class="border p-2 w-full"
      />
    </div>

    <div class="mb-2">
      <label>목표 금액</label>
      <input
        type="number"
        :value="modelValue.goal_amount"
        @input="update('goal_amount', +$event.target.value)"
        class="border p-2 w-full"
      />
    </div>
  </div>
</template>
