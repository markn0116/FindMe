<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">📁 カテゴリマスタ保守</h2>

    <!-- 新規追加ボタン -->
    <el-button class="mb-4" type="success" @click="openAddDialog">
      ＋ 新規追加
    </el-button>

    <!-- カテゴリ一覧テーブル -->
    <el-table :data="categories" border style="width: 100%">
      <el-table-column prop="MCTG_ID" label="ID" width="80" />
      <el-table-column prop="MCTG_NAME" label="カテゴリ名" />
      <el-table-column prop="MCTG_ORDER" label="表示順" width="100" />
      <el-table-column prop="MCTG_VALID" label="有効" width="80">
        <template #default="{ row }">
          <el-tag :type="row.MCTG_VALID ? 'success' : 'info'">
            {{ row.MCTG_VALID ? '有効' : '無効' }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- 編集・削除ボタン列 -->
      <el-table-column label="操作" width="160">
        <template #default="scope">
          <el-button size="small" type="primary" @click="openEditDialog(scope.row)">編集</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(scope.row)">削除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新規追加ダイアログ -->
    <el-dialog v-model="addDialogVisible" title="カテゴリ新規追加" width="500px">
      <el-form :model="addForm" label-width="100px">
        <el-form-item label="カテゴリ名">
          <el-input v-model="addForm.MCTG_NAME" />
        </el-form-item>
        <el-form-item label="表示順">
          <el-input-number v-model="addForm.MCTG_ORDER" :min="1" />
        </el-form-item>
        <el-form-item label="有効">
          <el-switch v-model="addForm.MCTG_VALID" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addDialogVisible.value = false">キャンセル</el-button>
        <el-button type="primary" @click="submitAdd">追加</el-button>
      </template>
    </el-dialog>

    <!-- 編集ダイアログ -->
    <el-dialog v-model="editDialogVisible" title="カテゴリ編集">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="カテゴリ名">
          <el-input v-model="editForm.MCTG_NAME" />
        </el-form-item>
        <el-form-item label="表示順">
          <el-input-number v-model="editForm.MCTG_ORDER" :min="0" />
        </el-form-item>
        <el-form-item label="有効">
          <el-switch v-model="editForm.MCTG_VALID" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">キャンセル</el-button>
        <el-button type="primary" @click="submitEdit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 再読み込みボタン -->
    <el-button class="mt-4" type="primary" @click="fetchCategories">
      再読み込み
    </el-button>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory
} from '@/api/masterCategoriesApi'
import { ElMessageBox, ElMessage } from 'element-plus'

// 新規追加用状態
const addDialogVisible = ref(false)
const addForm = ref({
  MCTG_NAME: '',
  MCTG_ORDER: 1,
  MCTG_VALID: true
})

// カテゴリ一覧を保持する状態変数
const categories = ref([])

// 編集用状態
const editDialogVisible = ref(false)
const editForm = ref({})

// カテゴリ一覧取得
const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('カテゴリ一覧の取得に失敗しました', error)
  }
}

// 新規追加ダイアログを開く
const openAddDialog = () => {
  addForm.value = {
    MCTG_NAME: '',
    MCTG_ORDER: 1,
    MCTG_VALID: true
  }
  addDialogVisible.value = true
}

// 新規追加ダイアログで保存
const submitAdd = async () => {
  try {
    await createCategory(addForm.value)
    ElMessage.success('カテゴリを追加しました')
    addDialogVisible.value = false
    await fetchCategories()
  } catch (error) {
    console.error('追加に失敗しました', error)
    ElMessage.error('追加に失敗しました')
  }
}

// 編集ダイアログを開く
const openEditDialog = (row) => {
  editForm.value = { ...row }
  editDialogVisible.value = true
}

// 編集ダイアログで保存
const submitEdit = async () => {
  try {
    await updateCategory(editForm.value.MCTG_ID, editForm.value)
    editDialogVisible.value = false
    await fetchCategories()
  } catch (error) {
    console.error('カテゴリ更新失敗', error)
  }
}

// 削除処理：確認のうえ実行
const confirmDelete = (row) => {
  ElMessageBox.confirm(
    `「${row.MCTG_NAME}」を本当に削除しますか？`,
    '確認',
    {
      confirmButtonText: '削除',
      cancelButtonText: 'キャンセル',
      type: 'warning',
    }
  )
    .then(async () => {
      await deleteCategory(row.MCTG_ID)
      await fetchCategories()
      ElMessage.success('削除しました')
    })
    .catch(() => {
      ElMessage.info('キャンセルしました')
    })
}

// 初期表示時にデータを取得
onMounted(() => {
  fetchCategories()
})
</script>
