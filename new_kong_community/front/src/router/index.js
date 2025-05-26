import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import ArticleCreateView from "@/views/ArticleCreateView.vue";
import ArticleUpdateView from "@/views/ArticleUpdateView.vue";
import ArticleList from "../components/ArticleList.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/create",
      name: "create",
      component: ArticleCreateView,
    },
    {
      path: "/articles/:id/edit",
      name: "ArticleUpdateView",
      component: ArticleUpdateView,
    },
    {
      path: "/articles/component/",
      name: "ArticleList",
      component: ArticleList,
    },
    {
      path: '/articles/:id',
      name: 'ArticleDetailView',
      component: () => import('@/views/ArticleDetailView.vue'), // 또는 직접 import
    },
  // router/index.js
    {
      path: '/compare',
      name: 'Compare',
      component: () => import('@/views/CompareView.vue')
    },
  ],

}

);

export default router;
