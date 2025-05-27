// src/stores/AccountStore.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const accounts = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  // ✅ 계좌 목록 불러오기 (예금/적금 포함)
  const fetchAccounts = async () => {
    try {
      const token = sessionStorage.getItem('authToken')
      const res = await axios.get(`${API_URL}/users/account/`, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      accounts.value = res.data  // 서버에서 받은 전체 계좌 리스트 저장
    } catch (err) {
      console.error('계좌 불러오기 실패:', err.response?.data)
    }
  }

  // ✅ 가장 빠른 만기일의 금액 반환 (예금 전용)
  const getEarliestMaturityAmount = () => {
    // account.deposit_detail.ends_at 기준 정렬 (예금만 고려)
    const sorted = accounts.value.filter(acc => acc.deposit_detail)
      .sort((a, b) => new Date(a.deposit_detail.ends_at) - new Date(b.deposit_detail.ends_at))
    return sorted[0]?.deposit_detail?.principal || 1000000  // principal 없으면 100만원 기본값
  }

  // ✅ 계좌 추가 API (예금 또는 적금 중 선택)
  const addAccount = async (formData) => {
    try {
      const token = sessionStorage.getItem('authToken')
      await axios.post(`${API_URL}/users/account/`, formData, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      await fetchAccounts() // 등록 후 계좌 목록 새로 불러오기
    } catch (err) {
      console.error('계좌 추가 실패:', err.response?.data)
    }
    
  }


  const calendarEvents = ref([])


const fetchCalendarEvents = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/users/calendar/')
    const raw = res.data

    const eventGroups = {}

    raw.forEach(event => {
      const key = event.type
      if (!eventGroups[key]) {
        eventGroups[key] = {
          key: key,
          highlight: key.includes('만기') ? 'red' : 'blue',
          dates: [],
        }
      }
      eventGroups[key].dates.push(event.date)
    })

    // ✅ 오늘 날짜 수동 추가
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const todayStr = today.toISOString().slice(0, 10)

    eventGroups["오늘"] = {
      key: "오늘",
      highlight: {
        contentClass: "today-highlight"
      },
      dates: [todayStr]
    }

    calendarEvents.value = Object.values(eventGroups)
  } catch (err) {
    console.error('캘린더 데이터 fetch 실패:', err)
  }
  
}



  return {
    accounts,  // 전체 계좌 목록
    fetchAccounts,  // 목록 불러오기
    getEarliestMaturityAmount,  // 예금 만기 순 정렬 함수
    addAccount,  // 계좌 추가
    fetchCalendarEvents,
    calendarEvents,
  }
})
