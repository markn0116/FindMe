// axiosライブラリを読み込む（VueからAPIを呼ぶために使用）
import axios from 'axios'

// カテゴリAPIのベースURL（FastAPI側と一致している必要あり）
const BASE_URL = '/api/categories'

/**
 * カテゴリ一覧を取得するAPI
 * メソッド: GET
 * URL: /api/categories
 */
export const getCategories = () => {
  return axios.get(BASE_URL)
}

/**
 * 新しいカテゴリを作成するAPI
 * メソッド: POST
 * URL: /api/categories
 * @param {Object} category - 作成するカテゴリデータ（例：{ name: "帽子", order: 1 }）
 */
export const createCategory = (category) => {
  return axios.post(BASE_URL, category)
}

/**
 * 既存のカテゴリを更新するAPI
 * メソッド: PUT
 * URL: /api/categories/{id}
 * @param {number} id - 更新対象のカテゴリID
 * @param {Object} category - 更新後のカテゴリデータ
 */
export const updateCategory = (id, category) => {
  return axios.put(`${BASE_URL}/${id}`, category)
}

/**
 * 指定したカテゴリを削除するAPI
 * メソッド: DELETE
 * URL: /api/categories/{id}
 * @param {number} id - 削除するカテゴリID
 */
export const deleteCategory = (id) => {
  return axios.delete(`${BASE_URL}/${id}`)
}
