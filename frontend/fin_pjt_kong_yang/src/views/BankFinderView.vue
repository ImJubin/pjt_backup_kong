<template>
  <div>
    <div class="orange-color" style="padding: 10px; text-align: center; color: white;">
      PJT07 - 은행 검색 애플리케이션
    </div>
    <div style="padding: 10px;">
      <h2 style="border-bottom: 1px solid rgb(255, 147, 85); padding-left: 5px;">은행 찾기</h2>
      <MapSearch />
    </div>
  </div>
</template>

<script setup>
import MapSearch from '@/components/MapSearch.vue'
</script>
