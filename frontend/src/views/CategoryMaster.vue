<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">📁 カテゴリマスタ保守</h2>

    <!-- カテゴリ一覧テーブル -->
    <el-table :data="categories" border style="width: 100%">
      <el-table-column prop="MCTG_ID" label="ID" width="80" />
      <el-table-column prop="MCTG_NAME" label="カテゴリ名" />
      <el-table-column prop="MCTG_ORDER" label="表示順" width="100" />
      <el-table-column prop="MCTG_VALID" label="有効" width="80">
        <template #default="{ row }">
          <el-tag type="success" v-if="row.MCTG_VALID">有効</el-tag>
          <el-tag type="info" v-else>無効</el-tag>
        </template>
      </el-table-column>
    </el-table>

    <!-- 再読み込みボタン -->
    <el-button class="mt-4" type="primary" @click="fetchCategories">
      再読み込み
    </el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories } from '@/api/masterCategoriesApi'

// カテゴリ一覧を保持する状態変数
const categories = ref([])

// APIからカテゴリ一覧を取得する関数
const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('カテゴリ一覧の取得に失敗しました', error)
  }
}

// 初期表示時にデータを取得
onMounted(() => {
  fetchCategories()
})
</script>
