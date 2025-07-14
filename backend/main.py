# app/main.py
from fastapi import FastAPI
from routers import category    #カテゴリマスタ用ルーター

# FastAPIアプリケーションの作成
app = FastAPI()

# ルーターを登録（これにより /categories 系のAPIが有効になる）
app.include_router(category.router)

# 動作確認用：ルートアクセスで簡単なメッセージを返す
@app.get("/")
def read_root():
    return {"message": "FindMe API is running"}
