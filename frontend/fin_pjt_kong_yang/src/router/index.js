import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue";
import MyPageView from "@/views/MyPageView.vue";
import UpdateMyDataView from "@/views/UpdateMyDataView.vue";
import ArticleCreateView from "@/views/ArticleCreateView.vue";
import ArticleUpdateView from "@/views/ArticleUpdateView.vue";
import ArticleList from "../components/ArticleList.vue";
import ProductPageView from '@/views/ProductPageView.vue'
import BankFinderView from '@/views/BankFinderView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import SearchView from '@/views/SearchView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'
import LaterView from '@/views/LaterView.vue'

// ✅ 로그인된 사용자가 회원가입 페이지에 접근하지 못하도록
const requireNotLoggedIn = (to, from, next) => {
  const token = sessionStorage.getItem("authToken");
  if (token) {
    next("/"); // 홈으로 리다이렉트
  } else {
    next();
  }
};
// 로그인 되지 않은 사용자가 회원제 페이지에 들어가려고 할 때때
const requireLoggedIn = (to, from, next) => {
  const token = sessionStorage.getItem("authToken");
  if (!token) {
    next({ name: "Login" });
  } else {
    next();
  }
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/users/signup",
      name: "SignUp",
      component: SignUpView,
      beforeEnter: requireNotLoggedIn, // ✅ 로그인 상태 체크
    },
    {
      path: "/users/login",
      name: "Login",
      component: LoginView,
      beforeEnter: requireNotLoggedIn,
    },
    {
      path: "/users/mypage",
      name: "MyPage",
      component: MyPageView,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/users/update",
      name: "UpdateMyData",
      component: UpdateMyDataView,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/product",
      name: "ProductPage",
      component: ProductPageView,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/product/:type/:id",
      name: "ProductDetail",
      component: ProductDetailView,
      props: true,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/",
      name: "bankFinder",
      component: BankFinderView,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/create",
      name: "create",
      component: ArticleCreateView,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/articles/:id/edit",
      name: "ArticleUpdateView",
      component: ArticleUpdateView,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/articles/component/",
      name: "ArticleList",
      component: ArticleList,
      beforeEnter: requireLoggedIn,
    },
    {
      path: "/articles/:id",
      name: "ArticleDetailView",
      component: () => import("@/views/ArticleDetailView.vue"), // 또는 직접 import
      beforeEnter: requireLoggedIn,
    },
    // router/index.js 지수비교
    {
      path: "/compare",
      name: "Compare",
      component: () => import("@/views/CompareView.vue"),
    },
      { path: '/search', name: 'Search', component: SearchView },
      { path: '/video/:videoId', name: 'VideoDetail', component: VideoDetailView, props: true },
      { path: '/Later', name: 'Later', component: LaterView },
    ],
})

export default router;
