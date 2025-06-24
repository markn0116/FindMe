# app/main.py
from fastapi import FastAPI

# FastAPIアプリケーションの作成
app = FastAPI()

# ダミーのカテゴリデータ（本来はDBに置く想定）
CATEGORIES = [
    {"MCTG_ID": 1, "MCTG_NAME": "かばん", "MCTG_ORDER": 1, "MCTG_VALID": True},
    {"MCTG_ID": 2, "MCTG_NAME": "傘", "MCTG_ORDER": 2, "MCTG_VALID": True},
    {"MCTG_ID": 3, "MCTG_NAME": "学生証", "MCTG_ORDER": 3, "MCTG_VALID": False},
]

# 動作確認用：ルートアクセスで簡単なメッセージを返す
@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

# カテゴリ一覧を取得するAPI
@app.get("/api/categories")
def get_categories():
    return CATEGORIES

# カテゴリを新規追加するAPI（POST）
@app.post("/api/categories")
def create_category(data: dict):
    # IDは今ある中で最大のID+1（初回は1）
    new_id = max(item["MCTG_ID"] for item in CATEGORIES) + 1 if CATEGORIES else 1
    # クライアントから渡されたデータでカテゴリを作成
    new_category = {
        "MCTG_ID": new_id,
        "MCTG_NAME": data.get("MCTG_NAME", ""),
        "MCTG_ORDER": data.get("MCTG_ORDER", 1),
        "MCTG_VALID": data.get("MCTG_VALID", True),
    }
    # ダミーデータに追加
    CATEGORIES.append(new_category)
    return new_category

# カテゴリ情報を更新するAPI（MCTG_IDで指定）
@app.put("/api/categories/{category_id}")
def update_category(category_id: int, data: dict):
    for item in CATEGORIES:
        if item["MCTG_ID"] == category_id:
            item.update(data)
            return item
    raise HTTPException(status_code=404, detail="カテゴリが見つかりません")

# カテゴリを削除するAPI（MCTG_IDで指定）
@app.delete("/api/categories/{category_id}")
def delete_category(category_id: int):
    for i, item in enumerate(CATEGORIES):
        if item["MCTG_ID"] == category_id:
            CATEGORIES.pop(i)
            return {"message": "削除しました"}
    raise HTTPException(status_code=404, detail="カテゴリが見つかりません")