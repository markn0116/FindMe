from pydantic import BaseModel
from datetime import datetime
from typing import Literal

# 共通スキーマ：新規・更新で共通する項目
class CategoryBase(BaseModel):
    mctg_name: str              # カテゴリ名
    mctg_order: int             # 表示順
    mctg_valid: Literal[0, 1]   # 有効フラグ

# 新規登録時のスキーマ
class CategoryCreate(CategoryBase):
    mctg_code: int           # カテゴリコード

# 更新時のスキーマ（IDはパスパラメータで受ける）
class CategoryUpdate(CategoryBase):
    pass

# レスポンス用：全項目＋作成日時・更新日時
class CategoryOut(CategoryCreate):
    mctg_created_at: datetime
    mctg_updated_at: datetime