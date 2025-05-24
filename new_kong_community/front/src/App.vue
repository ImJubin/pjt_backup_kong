<script setup>
import { RouterLink, RouterView } from "vue-router";
// import { useRouter } from 'vue-router'

// const router = useRouter()

function goToDetail() {
  router.push({ name: 'detail', params: { id: 1 } })
}

</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <br />
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped></style>
