import { defineStore } from 'pinia'
import axios from 'axios'

export const useAmountStore = defineStore('amount', {
  state: () => ({
    amount: null,
    defaultAmount: null,
  }),
  actions: {
    async fetchInitialAmount() {
      try {
        const token = sessionStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:8000/products/recommend/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.amount = res.data.amount
        this.defaultAmount = res.data.amount
      } catch (err) {
        console.error('초기 금액 불러오기 실패:', err)
        this.amount = 1000000
        this.defaultAmount = 1000000
      }
    },
    setAmount(val) {
      this.amount = val
    }
  }
})
