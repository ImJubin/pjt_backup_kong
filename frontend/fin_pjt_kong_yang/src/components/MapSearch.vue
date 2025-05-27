<template>
    <div style="margin: 10px 0;">
<button @click="searchMode = 'atm'; searchNearbyBanks()">ATM 보기</button>
<button @click="searchMode = 'branch'; searchNearbyBanks()">지점 보기</button>
<button @click="searchMode = 'all'; searchNearbyBanks()">전체 보기</button>
</div>


  <div class="search_main">
    <div class="search_drop">
      <div>
        <p>광역시 / 도</p>
        <select v-model="store.sido">
          <option disabled value="">광역시 / 도를 선택하세요</option>
          <option v-for="region in store.mapData" :key="region.name" :value="region.name">
            {{ region.name }}
          </option>
        </select>
      </div>
      <div>
        <p>시 / 군 / 구</p>
        <select v-model="store.sigungu" :disabled="!sigunguOptions.length">
          <option disabled value="">시 / 군 / 구를 선택하세요</option>
          <option v-for="s in sigunguOptions" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div>
        <p>은행</p>
        <select v-model="store.bank" :disabled="!store.sigungu">
          <option disabled value="">은행을 선택하세요</option>
          <option v-for="b in store.bankList" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>
      <button class="orange-color search-btn" :disabled="!isMapReady" @click="search">검색</button>
    </div>
    <div id="map" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useMapStore } from '@/stores/findMap.js'

const store = useMapStore()
const sigunguOptions = ref([])
const isMapReady = ref(false)
const searchMode = ref('branch') // 'branch' | 'atm' | 'all'
let ignoreNextCenterChange = false


let map = null
let ps = null
let infowindow = null
let markerList = []

onMounted(async () => {
  await store.fetchData()
  await loadKakaoMap()
})

watch(() => store.sido, (newVal) => {
  const region = store.mapData.find(r => r.name === newVal)
  sigunguOptions.value = region?.countries || []
  store.sigungu = ''
  store.bank = ''
})

const loadKakaoMap = async () => {
  if (window.kakao && window.kakao.maps) {
    // 이미 로딩되어 있으면 바로 실행
    await initUserPosition()
    return
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API}&autoload=false&libraries=services`
    script.onload = async () => {
      kakao.maps.load(async () => {
        console.log('✅ Kakao 지도 SDK 로드 완료')
        await initUserPosition()
        resolve()
      })
    }
    script.onerror = () => {
      console.error('❌ Kakao 지도 스크립트 로드 실패')
      alert('지도 로드에 실패했습니다. API 키 또는 인터넷 연결을 확인하세요.')
      reject()
    }
    document.head.appendChild(script)
  })
}

const initMap = (lat, lng) => {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(lat, lng),
    level: 3
  }
  map = new kakao.maps.Map(container, options)
  ps = new kakao.maps.services.Places()
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })

  const myMarker = new kakao.maps.Marker({
    map,
    position: new kakao.maps.LatLng(lat, lng),
    title: '현재 위치'
  })
  markerList.push(myMarker)

  isMapReady.value = true
  kakao.maps.event.addListener(map, 'center_changed', () => {
  if (ignoreNextCenterChange) {
    ignoreNextCenterChange = false
    return
  }
  searchNearbyBanks()
})



}

const search = () => {
  const { sido, sigungu, bank } = store

  if (!sido || !sigungu || !bank) {
    alert('모든 조건을 선택해주세요.')
    return
  }

  if (!isMapReady.value || !ps) {
    alert('지도가 아직 준비되지 않았습니다.')
    return
  }

  // 기존 마커 제거
  markerList.forEach(marker => marker.setMap(null))
  markerList = []

  const keyword = `${sido} ${sigungu} ${bank}`
  ps.keywordSearch(keyword, placesSearchCB)
}

const placesSearchCB = (data, status, moveMap = true) => {
  if (status !== kakao.maps.services.Status.OK) {
    // alert('검색 결과가 없습니다.')
    return
  }
  

  markerList.forEach(m => m.setMap(null))
  markerList = []

  const bounds = new kakao.maps.LatLngBounds()

  // ✅ 필터링
  const filtered = data.filter(place => {
  const name = place.place_name.toLowerCase()
  const category = place.category_name?.toLowerCase() || ''

  if (searchMode.value === 'atm') {
    return name.includes('atm') || category.includes('자동입출금기') || category.includes('atm') || category.includes('365')
  }

  if (searchMode.value === 'branch') {
    return !name.includes('atm') && !category.includes('자동입출금기') && !category.includes('365') && !category.includes('코너')
  }

  return true // all
})


  filtered.forEach(place => {
    const marker = new kakao.maps.Marker({
      map,
      position: new kakao.maps.LatLng(place.y, place.x)
    })

    kakao.maps.event.addListener(marker, 'click', () => {
      infowindow.setContent(`<div style="padding:5px;font-size:12px;">${place.place_name}</div>`)
      infowindow.open(map, marker)
    })

    markerList.push(marker)
    bounds.extend(new kakao.maps.LatLng(place.y, place.x))
  })

//   if (filtered.length) {
//   ignoreNextCenterChange = true
//   map.setBounds(bounds)
// }
if (filtered.length && moveMap) {
    ignoreNextCenterChange = true
    map.setBounds(bounds)
  }
}


const initUserPosition = () => {
  return new Promise((resolve) => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude
        const lng = pos.coords.longitude
        initMap(lat, lng)
        // ✅ 위치 주변 자동 검색 실행
        searchNearbyBanks(lat, lng)
        resolve()
      },
      () => {
        initMap(37.49818, 127.027386)
        resolve()
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    )
  })
}
const searchNearbyBanks = () => {
  if (!ps || !map) return

  const center = map.getCenter()
  const bounds = map.getBounds()
  const ne = bounds.getNorthEast()

  const radius = getDistance(center.getLat(), center.getLng(), ne.getLat(), ne.getLng())

  ps.keywordSearch('은행', (data, status) => {
    placesSearchCB(data, status, false)  // ❌ 지도 중심 이동 안 함
  }, {
    location: center,
    radius
  })
}


const getDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371000
  const toRad = x => x * Math.PI / 180

  const dLat = toRad(lat2 - lat1)
  const dLng = toRad(lng2 - lng1)

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}





</script>

<style scoped>
.search_main {
  display: flex;
  gap: 1rem;
}
.search_drop {
  width: 33%;
  display: flex;
  flex-direction: column;
}
.orange-color {
  background-color: rgb(255, 147, 85);
  color: white;
}
.search-btn {
  margin-top: 50px;
  padding: 10px;
  border: none;
  border-radius: 3px;
}
</style>
