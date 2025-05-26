// src/stores/CommodityStore.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCommodityStore = defineStore('commodity', {
  state: () => ({
    data: [],
  }),
  actions: {
    async fetchCommodityHistory(symbol) {
      const res = await axios.get(`http://127.0.0.1:8000/api/commodity-history`, {
        params: { symbol }
      })
      this.data = res.data
    }
  }
})