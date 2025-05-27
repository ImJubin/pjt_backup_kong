import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMapStore = defineStore('map', () => {
  const mapData = ref([])
  const bankList = ref([])
  const sido = ref('')
  const sigungu = ref('')
  const bank = ref('')

  const fetchData = async () => {
    try {
      const res = await fetch('/data.json')
      const json = await res.json()
      mapData.value = json.mapInfo
      bankList.value = json.bankInfo
    } catch (error) {
      console.error('지도 데이터 fetch 실패:', error)
    }
  }

  return {
    mapData,
    bankList,
    sido,
    sigungu,
    bank,
    fetchData,
  }
}, {
  persist: true
})
