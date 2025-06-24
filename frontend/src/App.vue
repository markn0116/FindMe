<template>
  <div id="app">
    <h1>📦 FindMe システム</h1>
    <nav>
      <router-link to="/">ホーム</router-link> |
      <router-link to="/master/category">カテゴリマスタ</router-link>
    </nav>

    <!-- 🔽 URLに対応する画面がここに表示される -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
nav {
  margin-bottom: 1rem;
}
router-link {
  margin-right: 1rem;
}
</style>
