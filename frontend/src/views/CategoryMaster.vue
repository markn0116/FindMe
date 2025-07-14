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
      <el-table-column prop="mctg_code" label="コード" width="80" />
      <el-table-column prop="mctg_name" label="カテゴリ名" min-width="180" />
      <el-table-column prop="mctg_order" label="表示順" width="100" align="center" />
      <el-table-column prop="mctg_valid" label="有効" width="100" align="center">
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
        <el-form-item label="コード" prop="mctg_code">
           <el-input-number v-model="addForm.mctg_code" :min="1" />
        </el-form-item>
        <el-form-item label="カテゴリ名" prop="mctg_name">
          <el-input v-model="addForm.mctg_name" />
        </el-form-item>
        <el-form-item label="表示順" prop="mctg_order">
          <el-input-number v-model="addForm.mctg_order" :min="1" />
        </el-form-item>
        <el-form-item label="有効" prop="mctg_valid">
          <el-switch v-model="addForm.mctg_valid" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addDialogVisible = false">キャンセル</el-button>
        <el-button type="primary" @click="submitAdd">追加</el-button>
      </template>
    </el-dialog>

    <!-- 編集ダイアログ -->
    <el-dialog v-model="editDialogVisible" title="カテゴリ編集" width="500px">
      <el-form :model="editForm" :rules="rules" ref="editFormRef" label-width="100px">
        <el-form-item label="コード" prop="mctg_code">
            <el-input-number v-model="editForm.mctg_code" :min="1" disabled />
        </el-form-item>
        <el-form-item label="カテゴリ名" prop="mctg_name">
          <el-input v-model="editForm.mctg_name" />
        </el-form-item>
        <el-form-item label="表示順" prop="mctg_order">
          <el-input-number v-model="editForm.mctg_order" :min="0" />
        </el-form-item>
        <el-form-item label="有効" prop="mctg_valid">
          <el-switch v-model="editForm.mctg_valid" />
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
import { required, positiveInteger, maxLength, uniqueId } from '@/validators/commonRules'

// 新規追加 状態定義
const addDialogVisible = ref(false)
// 初期値
const addForm = ref({
  mctg_code: null, 
  mctg_name: '',
  mctg_order: 1,
  mctg_valid: true
})
const addFormRef = ref()

// カテゴリ一覧の ID を格納（重複チェック用）
const existingIds = ref([])

// バリデーションルールを定義（prop に応じたルール）
const rules = reactive({
  mctg_code: [
    required(),
    positiveInteger(),
    uniqueId(existingIds.value)
  ],
  mctg_name: [
    required(),
    maxLength(20)
  ],
  mctg_order: [
    required(),
    positiveInteger()
  ]
})


// カテゴリ一覧を保持する状態変数
const categories = ref([])

// 編集 状態定義
const editDialogVisible = ref(false)
// 初期値
const editForm = ref({
  mctg_code: null,
  mctg_name: '',
  mctg_order: 1,
  mctg_valid: true
})
// カテゴリ一覧取得
const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = response.data
    existingIds.value = response.data.map(item => Number(item.mctg_code))
  } catch (error) {
    console.error('カテゴリ一覧の取得に失敗しました', error)
  }
}

// 新規追加ダイアログを開く
const openAddDialog = () => {
  // 現在のID最大値を求める（空の場合は0）
  const maxId = categories.value.length > 0
    ? Math.max(...categories.value.map(c => Number(c.mctg_code) || 0))
    : 0
  // 初期値を最大＋1。ただし、最低値は 1
  const nextId = Math.max(1, maxId + 1)

    addForm.value = {
    mctg_code: nextId,
    mctg_name: '',
    mctg_order: 1,
    mctg_valid: true
  }
  addDialogVisible.value = true
}

// 新規追加ダイアログで保存
const submitAdd = async () => {
  try {
    await addFormRef.value.validate()

    // IDが空なら最大＋1に補完
    if (!addForm.value.mctg_code) {
      const maxId = Math.max(0, ...categories.value.map(c => Number(c.mctg_code)))
      addForm.value.mctg_code = maxId + 1
    }

    await createCategory(addForm.value)
    ElMessage.success('カテゴリを追加しました')
    addDialogVisible.value = false
    addFormRef.value.resetFields()
    await fetchCategories()
  } catch (error) {
    console.error('APIエラー', error)

    // FastAPIなどからのレスポンスが object 形式か確認（バリデーションエラーを想定）
    const apiErrors = error?.response?.data

    if (apiErrors && typeof apiErrors === 'object') {
      const messages: string[] = []

      // 各フィールドごとにエラーメッセージを取り出して結合
      for (const key in apiErrors) {
        const fieldErrors = apiErrors[key]

        // 複数エラー（配列）の場合
        if (Array.isArray(fieldErrors)) {
          messages.push(`${key}: ${fieldErrors.join(', ')}`)
        }
        // 単一メッセージの場合
        else if (typeof fieldErrors === 'string') {
          messages.push(`${key}: ${fieldErrors}`)
        }
      }

      // 1つでもメッセージがあれば、結合して表示
      if (messages.length > 0) {
        ElMessage.error(messages.join(' / '))
        return
      }
    }

    // 上記で処理できなければ、汎用エラーとして表示
    ElMessage.error('登録に失敗しました（原因不明）')
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
    await editFormRef.value.validate()

    const { mctg_code, ...payload } = editForm.value
    await updateCategory(Number(editForm.value.mctg_code), editForm.value)
    ElMessage.success('カテゴリを編集しました')
    editDialogVisible.value = false
    editFormRef.value.resetFields()
    await fetchCategories()
  } catch (error) {
    console.error('カテゴリ更新時のエラー', error)

    // FastAPIのレスポンスデータを取得（バリデーションエラーやNotFoundを含む想定）
    const apiErrors = error?.response?.data

    // 1. 該当IDが存在しない（PUT対象が見つからない）などの明示的なエラーを最初に処理
    if (apiErrors?.detail === 'Not Found') {
      ElMessage.error('対象のカテゴリが見つかりませんでした')
      return
    }

    // 2. フィールドごとのバリデーションエラーがある場合に処理
    if (apiErrors && typeof apiErrors === 'object') {
      const messages: string[] = []

      // 各フィールド（例：mctg_name, mctg_order）に対してメッセージを生成
      for (const key in apiErrors) {
        const fieldErrors = apiErrors[key]

        // エラーが配列（複数メッセージ）の場合
        if (Array.isArray(fieldErrors)) {
          messages.push(`${key}: ${fieldErrors.join(', ')}`)
        }
        // 単一文字列で返ってくる場合
        else if (typeof fieldErrors === 'string') {
          messages.push(`${key}: ${fieldErrors}`)
        }
      }

      // いずれかのエラーが存在していれば、まとめて表示
      if (messages.length > 0) {
        ElMessage.error(messages.join(' / '))
        return
      }
    }

    // 上記のどれにも該当しない場合の最終的なフォールバックエラーメッセージ
    ElMessage.error('カテゴリ更新に失敗しました（原因不明）')
  }
}

// 削除処理：確認のうえ実行
const confirmDelete = (row) => {
  ElMessageBox.confirm(
    `「${row.mctg_name}」を本当に削除しますか？`,
    '確認',
    {
      confirmButtonText: '削除',
      cancelButtonText: 'キャンセル',
      type: 'warning',
    }
  )
    .then(async () => {
      await deleteCategory(row.mctg_code)
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