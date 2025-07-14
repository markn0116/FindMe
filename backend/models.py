# このファイルは、忘れ物管理システム『FindMe』で使用するSQLAlchemyモデル定義です。
# PostgreSQL上に構築するデータベース構造をPythonコードで表現しています。
# テーブルごとにクラスを分け、外部キーや制約、型情報を設計書に基づいて記述しています。
# Alembicと連携することでマイグレーションによるテーブル作成・変更も可能になります。

# SQLAlchemyで使用する必要な型や制約をインポート
from sqlalchemy import Column, Integer, String, Date, DateTime, SmallInteger, Text, ForeignKey, text
# SQLAlchemyのベースクラスを作成（全モデルはこれを継承）
from sqlalchemy.ext.declarative import declarative_base
# default値にnow()を使用するためにインポート
from sqlalchemy.sql import func

Base = declarative_base()  # モデル定義の基盤となるクラス

# 忘れ物情報テーブル
class d_items(Base):
    __tablename__ = 'd_items'

    ditm_id = Column(Integer, primary_key=True)  # 忘れ物ID
    ditm_name = Column(String(30), nullable=False)  # 名称
    ditm_category_code = Column(Integer, ForeignKey("m_categories.mctg_code"), nullable=False)  # カテゴリコード
    ditm_found_at = Column(Integer, ForeignKey("m_locations.mlct_code"), nullable=False)  # 発見場所
    ditm_found_at_note = Column(Text)  # 発見場所補足
    ditm_found_date = Column(Date, nullable=False)  # 発見日
    ditm_storage_code = Column(Integer, ForeignKey("m_storages.mstr_code"), nullable=False)  # 保管場所コード
    ditm_staff_code = Column(Integer, ForeignKey("m_staffs.mstf_code"), nullable=False)  # 職員コード
    ditm_isreturned = Column(SmallInteger, nullable=False, default=0)  # 返却済フラグ
    ditm_return_date = Column(Date)  # 返却日
    ditm_returned_by = Column(Integer, ForeignKey("m_staffs.mstf_code"))  # 返却対応職員コード
    ditm_memo = Column(Text)  # その他メモ
    ditm_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    ditm_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 忘れ物画像データ
class d_item_images(Base):
    __tablename__ = 'd_item_images'

    dimg_item_id = Column(Integer, ForeignKey("d_items.ditm_id"), primary_key=True)  # 忘れ物ID
    dimg_seq = Column(SmallInteger, primary_key=True)  # 表示順
    dimg_path = Column(Text, nullable=False)  # 画像パス
    dimg_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    dimg_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# システムマスタ
class m_system(Base):
    __tablename__ = 'm_system'

    msys_id = Column(Integer, primary_key=True)  # ID
    msys_imgcount = Column(SmallInteger)  # 画像最大枚数
    msys_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    msys_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# カテゴリマスタ
class m_categories(Base):
    __tablename__ = 'm_categories'

    mctg_code = Column(Integer, primary_key=True)  # コード
    mctg_name = Column(String(20), nullable=False)  # 名称
    mctg_order = Column(SmallInteger, nullable=False, server_default=text("1"))  # 表示順
    mctg_valid = Column(SmallInteger, nullable=False, server_default=text("1"))  # 有効フラグ
    mctg_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    mctg_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 発見場所マスタ
class m_locations(Base):
    __tablename__ = 'm_locations'

    mlct_code = Column(Integer, primary_key=True)  # コード
    mlct_name = Column(String(20), nullable=False)  # 名称
    mlct_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    mlct_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 保管場所マスタ
class m_storages(Base):
    __tablename__ = 'm_storages'

    mstr_code = Column(Integer, primary_key=True)  # コード
    mstr_name = Column(String(20), nullable=False)  # 名称
    mstr_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    mstr_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時

# 職員マスタ
class m_staffs(Base):
    __tablename__ = 'm_staffs'

    mstf_code = Column(Integer, primary_key=True)  # コード
    mstf_name = Column(String(30), nullable=False)  # 名称
    mstf_created_at = Column(DateTime, nullable=False, server_default=func.now())  # 作成日時
    mstf_updated_at = Column(DateTime, nullable=False, server_default=func.now())  # 更新日時
