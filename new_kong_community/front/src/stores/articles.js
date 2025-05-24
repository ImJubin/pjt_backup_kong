import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";

export const useArticleStore = defineStore(
  "article",
  () => {
    const articles = ref([]);
    const API_URL = "http://127.0.0.1:8000";

    const getArticles = function () {
      axios({
        method: "get",
        url: "http://127.0.0.1:8000/api/v1/articles/",
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          console.log(res);
          console.log(res.data);
          articles.value = res.data;
        })
        .catch((err) => console.log(err));
    };

    // ✏️ 게시글 수정 (PUT)
    const updateArticle = (articleId, updatedData) => {
      return axios({
        method: "put",
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        data: updatedData,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
    };

    const deleteArticle = (articleId) => {
      return axios({
        method: "delete",
        url: `${API_URL}/api/v1/articles/${articleId}/`,
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
    };

    return { articles, API_URL, getArticles, updateArticle, deleteArticle };
  },
  { persist: true }
);
