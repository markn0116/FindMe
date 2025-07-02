// 必須
export const required = (message = '必須項目です') => ({
  required: true,
  message,
  trigger: 'blur',
})

// 数値の正の整数
export const positiveInteger = (message = '正の整数を入力してください') => ({
  type: 'number',
  min: 1,
  message,
  trigger: 'blur',
})

// コード重複チェック（既存コードリストを受け取る）
export const uniqueId = (existingIds, message = 'このコードは既に使用されています') => ({
  validator: (_, value, callback) => {
    if (value === '' || value == null) return callback() // 空はOK（submitで補完）
    const numeric = Number(value)
    if (!Number.isInteger(numeric) || numeric <= 0) return callback() // 数値でない場合は他のバリデーションに任せる
    if (existingIds.includes(Number(value))) {
      callback(new Error(message))
    } else {
      callback()
    }
  },
  trigger: 'blur'
})
