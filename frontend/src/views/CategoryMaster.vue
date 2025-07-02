<template>
  <div class="p-6">
    <!-- タイトルと追加ボタン -->
    <div class="text-left">
      <h2 class="text-2xl font-bold">📁 カテゴリマスタ保守</h2>
    </div>
    <div class="mb-4 text-right">
      <el-button type="primary" size="large" @click="openAddDialog">＋ 新規追加</el-button>
    </div>

    <!-- カテゴリ一覧テーブル -->
    <div class="mb-4">
    <el-table
      :data="categories"
      border
      size="small"
      class="rounded-lg shadow-md bg-white text-sm"
      style="width: 100%"
    >
      <el-table-column prop="MCTG_CODE" label="コード" width="80" />
      <el-table-column prop="MCTG_NAME" label="カテゴリ名" min-width="180" />
      <el-table-column prop="MCTG_ORDER" label="表示順" width="100" align="center" />
      <el-table-column prop="MCTG_VALID" label="有効" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="row.MCTG_VALID ? 'success' : 'info'" effect="plain">
            {{ row.MCTG_VALID ? '有効' : '無効' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" align="center">
        <template #default="{ row }">
          <el-button size="small" type="primary" plain @click="openEditDialog(row)">編集</el-button>
          <el-button size="small" type="danger" plain @click="confirmDelete(row)">削除</el-button>
        </template>
      </el-table-column>
    </el-table>
    </div>

    <!-- 新規追加ダイアログ -->
    <el-dialog v-model="addDialogVisible" title="カテゴリ新規追加" width="500px">
      <el-form :model="addForm" :rules="rules" ref="addFormRef" label-width="100px">
        <el-form-item label="コード" prop="MCTG_CODE">
           <el-input-number v-model="addForm.MCTG_CODE" :min="1" />
        </el-form-item>
        <el-form-item label="カテゴリ名" prop="MCTG_NAME">
          <el-input v-model="addForm.MCTG_NAME" />
        </el-form-item>
        <el-form-item label="表示順" prop="MCTG_ORDER">
          <el-input-number v-model="addForm.MCTG_ORDER" :min="1" />
        </el-form-item>
        <el-form-item label="有効" prop="MCTG_VALID">
          <el-switch v-model="addForm.MCTG_VALID" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addDialogVisible = false">キャンセル</el-button>
        <el-button type="primary" @click="submitAdd">追加</el-button>
      </template>
    </el-dialog>

    <!-- 編集ダイアログ -->
    <el-dialog v-model="editDialogVisible" title="カテゴリ編集" width="500px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="コード">
            <el-input-number v-model="editForm.MCTG_CODE" :min="1" disabled />
        </el-form-item>
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
    <div class="text-right">
      <el-button type="default" size="large" @click="fetchCategories">再読み込み</el-button>
    </div>
  </div>
</template>


<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory
} from '@/api/masterCategoriesApi'
import { ElMessageBox, ElMessage } from 'element-plus'

// 共通化したバリデーションルールをインポート（自作の @/validators/commonRules から）
import { required, positiveInteger } from '@/validators/commonRules'
import { uniqueId } from '../validators/commonRules'

// 新規追加 状態定義
const addDialogVisible = ref(false)
const addForm = ref({
  MCTG_CODE: null, 
  MCTG_NAME: '',
  MCTG_ORDER: 1,
  MCTG_VALID: true
})
const addFormRef = ref()

// カテゴリ一覧の ID を格納（重複チェック用）
const existingIds = ref([])

// バリデーションルールを定義（prop に応じたルール）
const rules = reactive({
  MCTG_CODE: [
    positiveInteger(),
    {
      validator: (_, value, callback) => {
        const numeric = Number(value)
        if (!Number.isInteger(numeric) || numeric <= 0) return callback()
        if (existingIds.value.includes(numeric)) {
          callback(new Error('このコードは既に使用されています'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  MCTG_NAME: [required()],
  MCTG_ORDER: [positiveInteger()]
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
    existingIds.value = response.data.map(item => Number(item.MCTG_CODE))
  } catch (error) {
    console.error('カテゴリ一覧の取得に失敗しました', error)
  }
}

// 新規追加ダイアログを開く
const openAddDialog = () => {
  // 現在のID最大値を求める（空の場合は0）
  const maxId = categories.value.length > 0
    ? Math.max(...categories.value.map(c => Number(c.MCTG_CODE) || 0))
    : 0
  // 初期値を最大＋1。ただし、最低値は 1
  const nextId = Math.max(1, maxId + 1)

    addForm.value = {
    MCTG_CODE: nextId,
    MCTG_NAME: '',
    MCTG_ORDER: 1,
    MCTG_VALID: true
  }
  addDialogVisible.value = true
}

// 新規追加ダイアログで保存
const submitAdd = async () => {
  try {
    await addFormRef.value.validate()

    // IDが空なら最大＋1に補完
    if (!addForm.value.MCTG_CODE) {
      const maxId = Math.max(0, ...categories.value.map(c => Number(c.MCTG_CODE)))
      addForm.value.MCTG_CODE = maxId + 1
    }

    await createCategory(addForm.value)
    ElMessage.success('カテゴリを追加しました')
    addDialogVisible.value = false
    await fetchCategories()
  } catch (error) {
    console.error('エラー全体', error)
    // エラー内容に応じて分岐
    const idErrors = error?.MCTG_CODE || error?.response?.data?.MCTG_CODE
    if (Array.isArray(idErrors) && idErrors.length > 0) {
      const msg = idErrors[0]?.message || String(idErrors[0])
      ElMessage.error(msg)
    } else {
      ElMessage.error('追加に失敗しました')
    }
  }
}

// 編集ダイアログを開く
const openEditDialog = (row) => {
  Object.assign(editForm.value, row)
  editDialogVisible.value = true
}

// 編集ダイアログで保存
const submitEdit = async () => {
  try {
    const { MCTG_CODE, ...payload } = editForm.value
    await updateCategory(Number(editForm.value.MCTG_CODE), editForm.value)
    editDialogVisible.value = false
    await fetchCategories()
  } catch (error) {
    if (error.response) {
      console.error('カテゴリ更新失敗: ', error.response.status, error.response.data)
    } else {
      console.error('カテゴリ更新失敗: ', error.message)
    }
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
      await deleteCategory(row.MCTG_CODE)
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

<style scoped>
/* テーブルヘッダのデザイン調整 */
:deep(.el-table__header th) {
  font-weight: 600;
  color: #334155;
  background-color: #f9fafb;
}

:deep(.el-table__row:hover) {
  background-color: #f1f5f9;
}
</style>