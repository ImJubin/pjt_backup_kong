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
        <RouterLink to="/compare">[시세 비교]</RouterLink>
        <br />
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped></style>
