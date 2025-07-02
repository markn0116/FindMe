# このファイルは、忘れ物管理システム『FindMe』で使用するSQLAlchemyモデル定義です。
# PostgreSQL上に構築するデータベース構造をPythonコードで表現しています。
# テーブルごとにクラスを分け、外部キーや制約、型情報を設計書に基づいて記述しています。
# Alembicと連携することでマイグレーションによるテーブル作成・変更も可能になります。

# SQLAlchemyで使用する必要な型や制約をインポート
from sqlalchemy import Column, Integer, String, Date, DateTime, SmallInteger, Text, ForeignKey
# SQLAlchemyのベースクラスを作成（全モデルはこれを継承）
from sqlalchemy.ext.declarative import declarative_base
# default値にnow()を使用するためにインポート
from sqlalchemy.sql import func

Base = declarative_base()  # モデル定義の基盤となるクラス

# 忘れ物情報テーブル
class D_ITEMS(Base):
    __tablename__ = 'D_ITEMS'

    DITM_ID = Column(Integer, primary_key=True)  # 忘れ物ID
    DITM_NAME = Column(String(30), nullable=False)  # 名称
    DITM_CATEGORY_CODE = Column(Integer, ForeignKey("M_CATEGORIES.MCTG_CODE"), nullable=False)  # カテゴリコード
    DITM_FOUND_AT = Column(Integer, ForeignKey("M_LOCATIONS.MLCT_CODE"), nullable=False)  # 発見場所
    DITM_FOUND_AT_NOTE = Column(Text)  # 発見場所補足
    DITM_FOUND_DATE = Column(Date, nullable=False)  # 発見日
    DITM_STORAGE_CODE = Column(Integer, ForeignKey("M_STORAGES.MSTR_CODE"), nullable=False)  # 保管場所コード
    DITM_STAFF_CODE = Column(Integer, ForeignKey("M_STAFFS.MSTF_CODE"), nullable=False)  # 職員コード
    DITM_IS_RETURNED = Column(SmallInteger, nullable=False, default=0)  # 返却済フラグ
    DITM_RETURN_DATE = Column(Date)  # 返却日
    DITM_RETURNED_BY = Column(Integer, ForeignKey("M_STAFFS.MSTF_CODE"))  # 返却対応職員コード
    DITM_MEMO = Column(Text)  # その他メモ
    DITM_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    DITM_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 忘れ物画像データ
class D_ITEM_IMAGES(Base):
    __tablename__ = 'D_ITEM_IMAGES'

    DIMG_ITEM_ID = Column(Integer, ForeignKey("D_ITEMS.DITM_ID"), primary_key=True)  # 忘れ物ID
    DIMG_SEQ = Column(SmallInteger, primary_key=True)  # 表示順
    DIMG_PATH = Column(Text, nullable=False)  # 画像パス
    DIMG_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    DIMG_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# システムマスタ
class M_SYSTEM(Base):
    __tablename__ = 'M_SYSTEM'

    MSYS_ID = Column(Integer, primary_key=True)  # ID
    MSYS_IMGCOUNT = Column(SmallInteger)  # 画像最大枚数
    MSYS_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    MSYS_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# カテゴリマスタ
class M_CATEGORIES(Base):
    __tablename__ = 'M_CATEGORIES'

    MCTG_CODE = Column(Integer, primary_key=True)  # コード
    MCTG_NAME = Column(String(20), nullable=False)  # 名称
    MCTG_ORDER = Column(SmallInteger, nullable=False, server_default=1)  # 表示順
    MCTG_VALID = Column(SmallInteger, nullable=False, server_default=1)  # 有効フラグ
    MCTG_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    MCTG_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 発見場所マスタ
class M_LOCATIONS(Base):
    __tablename__ = 'M_LOCATIONS'

    MLCT_CODE = Column(Integer, primary_key=True)  # コード
    MLCT_NAME = Column(String(20), nullable=False)  # 名称
    MLCT_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    MLCT_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 保管場所マスタ
class M_STORAGES(Base):
    __tablename__ = 'M_STORAGES'

    MSTR_CODE = Column(Integer, primary_key=True)  # コード
    MSTR_NAME = Column(String(20), nullable=False)  # 名称
    MSTR_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    MSTR_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 職員マスタ
class M_STAFFS(Base):
    __tablename__ = 'M_STAFFS'

    MSTF_CODE = Column(Integer, primary_key=True)  # コード
    MSTF_NAME = Column(String(30), nullable=False)  # 名称
    MSTF_CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    MSTF_UPDATED_AT = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時
