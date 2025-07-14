/**
 * 共通バリデーションルール定義 (Element Plus + Vue 3)
 * - 各フォームで再利用可能な関数形式のバリデーションルール
 */

import type { RuleItem } from 'element-plus'

/**
 * 必須項目チェック
 * @param message エラーメッセージ（省略時はデフォルト）
 */
export const required = (message = '必須項目です'): RuleItem => ({
  required: true,
  message,
  trigger: 'blur',
})

/**
 * 正の整数チェック（例：ID、表示順など）
 * @param message エラーメッセージ
 */
export const positiveInteger = (message = '正の整数を入力してください'): RuleItem => ({
  type: 'number',
  min: 1,
  message,
  trigger: 'blur',
})

/**
 * 最大文字数チェック
 * @param max 最大文字数（例：50）
 * @param message 任意のエラーメッセージ（`${max}文字以内で入力してください`がデフォルト）
 */
export const maxLength = (max: number, message?: string): RuleItem => ({
  validator: (_rule, value, callback) => {
    if (typeof value === 'string' && value.length > max) {
      callback(new Error(message || `${max}文字以内で入力してください`))
    } else {
      callback()
    }
  },
  trigger: 'blur',
})

/**
 * コードの重複チェック（数値IDを対象）
 * @param existingIds 現在存在するIDリスト（数値配列）
 * @param message エラーメッセージ
 */
export const uniqueId = (
  existingIds: number[],
  message = 'このコードは既に使用されています'
): RuleItem => ({
  validator: (_rule, value, callback) => {
    if (value === '' || value == null) return callback() // 空は許可（submit時に補完される想定）
    const numeric = Number(value)
    if (!Number.isInteger(numeric) || numeric <= 0) return callback() // 無効な数値は別バリデーションに任せる
    if (existingIds.includes(numeric)) {
      callback(new Error(message))
    } else {
      callback()
    }
  },
  trigger: 'blur',
})
