from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import category as schema
from crud import category as crud

# カテゴリマスタのルーター設定
router = APIRouter(
    prefix="/categories",  # すべて /categories から始まる
    tags=["カテゴリ"]       # OpenAPI上のグループ名
)

# 🔍 一覧取得：GET /categories
@router.get("/", response_model=list[schema.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)

# ➕ 新規登録：POST /categories
@router.post("/", response_model=schema.CategoryOut)
def create_category(category: schema.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

# ✏️ 更新：PUT /categories/{code}
@router.put("/{code}", response_model=schema.CategoryOut)
def update_category(code: int, category: schema.CategoryUpdate, db: Session = Depends(get_db)):
    result = crud.update_category(db, code, category)
    if not result:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")
    return result

# ❌ 削除：DELETE /categories/{code}
@router.delete("/{code}", response_model=schema.CategoryOut)
def delete_category(code: int, db: Session = Depends(get_db)):
    result = crud.delete_category(db, code)
    if not result:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")
    return result
