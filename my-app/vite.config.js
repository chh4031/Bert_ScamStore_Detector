import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5001,  // 원하는 포트 번호로 고정
    strictPort: false, // 이 옵션을 켜면, 사용 중일 경우 에러 발생 (자동 변경 안 함)
    proxy :{
      '/api': 'http://localhost:5000',
    }
  },
})
