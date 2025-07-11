import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .envから読み込まれるDATABASE_URLを使用
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemyのエンジン作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# セッション生成（リクエストごとにDB接続を確保するため）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル定義の基盤クラス
Base = declarative_base()

# FastAPIで使うDB依存注入用関数（エンドポイントで使う）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
