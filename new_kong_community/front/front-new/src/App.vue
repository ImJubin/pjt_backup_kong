<!-- src/App.vue -->
<template>
  <div class="p-4">
    <RouterLink to="/compare">📊 시세 비교</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>