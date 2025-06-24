// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 各画面（コンポーネント）をインポート
import Home from '../views/Home.vue'
import CategoryMaster from '../views/CategoryMaster.vue'

// ルーティングの定義
const routes = [
  { path: '/', component: Home },
  { path: '/master/category', component: CategoryMaster }
]

// ルーターインスタンスを作成
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
