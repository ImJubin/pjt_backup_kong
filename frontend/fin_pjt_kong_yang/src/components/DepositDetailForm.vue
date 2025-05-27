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
    <h4 class="font-semibold mb-2">예금 상품 정보</h4>

    <div>
      <label>상품명</label>
      <input :value="modelValue.product_name" @input="update('product_name', $event.target.value)" />
    </div>

    <div>
      <label>금리 (%)</label>
      <input type="number" :value="modelValue.interest_rate" @input="update('interest_rate', +$event.target.value)" />
    </div>

    <div>
      <label>기간 (개월)</label>
      <input type="number" :value="modelValue.duration_months" @input="update('duration_months', +$event.target.value)" />
    </div>

    <div>
      <label>시작일</label>
      <input type="date" :value="modelValue.started_at" @input="update('started_at', $event.target.value)" />
    </div>

    <div>
      <label>만기일</label>
      <input type="date" :value="modelValue.ends_at" @input="update('ends_at', $event.target.value)" />
    </div>
  </div>
</template>
