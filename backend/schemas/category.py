from pydantic import BaseModel

# 共通スキーマ：新規・更新で共通する項目
class CategoryBase(BaseModel):
    MCTG_NAME: str         # カテゴリ名
    MCTG_ORDER: int        # 表示順
    MCTG_VALID: bool       # 有効フラグ

# 新規登録時のスキーマ
class CategoryCreate(CategoryBase):
    MCTG_CODE: int           # カテゴリコード

# 更新時のスキーマ（IDはパスパラメータで受ける）
class CategoryUpdate(CategoryBase):
    pass

# レスポンス用：全項目＋作成日時・更新日時
class CategoryOut(CategoryCreate):
    MCTG_CREATED_AT: datetime
    MCTG_UPDATED_AT: datetime