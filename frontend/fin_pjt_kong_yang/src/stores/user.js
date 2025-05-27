import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRoute, useRouter } from "vue-router";
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
    const router = useRouter()
    const API_URL = 'http://127.0.0.1:8000'


    const token = ref(sessionStorage.getItem('authToken') || null)
    const user = ref(null)
  

    //회원가입입
    const signUp = async function (payload) {
    const {
      username, email, password, password2, first_name, last_name, phone_number
    } = payload

    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/users/signup/`,
        data: {
          username,
          email,
          password,
          password2,
          first_name,
          last_name,
          phone_number
        }
      })

      console.log('회원가입 성공!', res.data)
      // 원하는 작업 실행 (ex: 자동 로그인, 이동 등)

    } catch (err) {
      console.error('회원가입 실패:', err.response?.data || err.message)
      throw err  // 뷰 컴포넌트에서 처리하도록 throw
    }
  }

  // 로그인
  const logIn = async function ({ username, password }) {
    try {
      const res = await axios.post(`${API_URL}/users/login/`, {
        username,
        password
      })

      token.value = res.data.key
      sessionStorage.setItem('authToken', token.value)

      await fetchUserInfo()
      router.push({ name: 'Home' })
    } catch (err) {
      console.error('❌ 로그인 실패:', err.response?.data)
      throw err
    }
  }

  // ✅ 유저 정보 불러오기
  const fetchUserInfo = async function () {
    try {
      const res = await axios.get(`${API_URL}/users/user/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      user.value = res.data
      console.log('👤 유저 정보:', user.value)
    } catch (err) {
      console.error('❌ 유저 정보 불러오기 실패:', err)
    }
  }

  const logOut = async function () {
  try {
    // 서버에 로그아웃 요청
    await axios.post(`${API_URL}/users/logout/`, {}, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
  } catch (err) {
    console.warn('⚠️ 서버 로그아웃 실패 (무시 가능):', err.response?.data)
    // 토큰이 만료돼도 로컬에서 지워야 하므로 catch는 무시 가능
  }
  // 토큰 및 사용자 정보 초기화
  token.value = null
  user.value = null
  sessionStorage.removeItem('token')
  
  // 홈으로 이동
  router.push({ name: 'Home' })
  console.log('로그아웃 완료')
} 

const updateUserInfo = async function (payload) {
  try {
    const res = await axios.patch(`${API_URL}/users/user/`, {
      first_name: payload.first_name,
      last_name: payload.last_name,
      email: payload.email,
      phone_number: payload.phone_number
    }, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })

    user.value = res.data  // 스토어 정보 갱신
    return { success: true }
  } catch (err) {
    console.error('❌ 회원 정보 수정 실패:', err.response?.data || err)
    return { success: false, message: err.response?.data || '알 수 없는 오류' }
  }
}

const changePassword = async function (payload) {
  try {
    const res = await axios.post(`${API_URL}/users/password/change/`, payload, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    return { success: true }
  } catch (err) {
    return {
      success: false,
      message: err.response?.data || '알 수 없는 오류'
    }
  }
}

const deleteUser = async () => {
  const token = sessionStorage.getItem('authToken')
  try {
    await axios.delete(`${API_URL}/accounts/user/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    // 토큰 삭제하고 홈으로 이동
    sessionStorage.removeItem('authToken')
    router.push({ name: 'Home' })
  } catch (err) {
    console.error('회원 탈퇴 실패:', err.response?.data)
  }
}

  return { token, user, signUp, logIn, logOut, fetchUserInfo, changePassword, updateUserInfo, deleteUser }
},{ persist: true })