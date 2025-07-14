from sqlalchemy.orm import Session
from models import m_categories
from schemas.category import CategoryCreate, CategoryUpdate
from typing import List
from datetime import datetime

# 🔍 カテゴリ一覧を取得する（表示順でソート）
def get_all_categories(db: Session):
    # 全件取得して表示順で並べ替え
    return db.query(m_categories).order_by(m_categories.mctg_order).all()

# ➕ 新しいカテゴリを登録する（単体）
def create_category(db: Session, category: CategoryCreate):
    # Pydanticモデル（CategoryCreate）を辞書に変換し、ORMモデルに展開
    db_obj = m_categories(**category.dict())
    # セッションに追加 → コミット → 登録内容を反映（refresh）
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj  # 登録されたカテゴリ情報を返す

# ➕ 複数カテゴリを一括登録する（bulk insert）
def create_categories_bulk(db: Session, categories: List[CategoryCreate]):
    db_objs = [m_categories(**c.dict(), mctg_created_at=datetime.now(), mctg_updated_at=datetime.now()) for c in categories]
    db.add_all(db_objs)
    db.commit()
    return db_objs

# ✏️ 指定されたカテゴリコードのデータを更新する
def update_category(db: Session, category_code: int, update: CategoryUpdate):
    # 対象のカテゴリを取得（存在しなければ None）
    db_obj = db.query(m_categories).filter(m_categories.mctg_code == category_code).first()
    if db_obj is None:
        return None

    # 更新対象のフィールドを1つずつ上書き
    for key, value in update.dict().items():
        setattr(db_obj, key, value)

    # 更新内容を反映
    db.commit()
    db.refresh(db_obj)
    return db_obj  # 更新後のカテゴリ情報を返す

# ❌ 指定されたカテゴリを削除する
def delete_category(db: Session, category_code: int):
    # 削除対象のカテゴリを取得
    db_obj = db.query(m_categories).filter(m_categories.mctg_code == category_code).first()
    if db_obj is None:
        return None

    # セッションから削除してコミット
    db.delete(db_obj)
    db.commit()
    return db_obj  # 削除したカテゴリ情報を返す
