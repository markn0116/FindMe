<template>
  <div id="app">
    <!-- タイトル -->
    <header class="app-title">
      <span class="icon">📦</span>
      <h1>FindMe</h1>
    </header>

    <!-- ナビゲーションバー -->
    <el-menu
      :default-active="activeMenu"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#f7f9fb"
      text-color="#2c3e50"
      active-text-color="#409EFF"
      router
    >
    <el-menu-item index="/">ホーム</el-menu-item>
      <el-menu-item index="/master/categories">カテゴリマスタ保守</el-menu-item>
    </el-menu>

    <!-- 画面本体 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const route = useRoute()
    const activeMenu = computed(() => {
      // サブページでも親メニューが選ばれるようにする場合、ここで調整
      return route.path
    })
    return { activeMenu }
  }
}
</script>

<style scoped>
#app {
  box-sizing: border-box;
  font-family: 'Segoe UI', 'Noto Sans JP', sans-serif;
  padding: 40px 24px 24px;
  min-height: 100vh;
  min-width: 600px; /* 最小幅を指定して省略防止 */
}

/* タイトル */
.app-title {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

.app-title .icon {
  font-size: 2rem;
  opacity: 0.8;
}

.app-title h1 {
  font-size: 2.8rem;
  font-weight: 500;
  color: #2f3640;
  margin: 0;
  letter-spacing: 0.5px;
}

/* ナビゲーション */
.nav-menu {
  text-align: left;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  white-space: nowrap;
}

.nav-menu a {
  margin: 0 0.75rem;
  color: #409EFF;
  text-decoration: none;
  font-weight: 500;
}

.nav-menu a:hover {
  text-decoration: underline;
}

.divider {
  color: #ccc;
}

/* コンテンツ領域 */
.main-content {
  padding-top: 8px;
  font-family: 'Segoe UI', sans-serif;
}
</style>
