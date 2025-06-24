# ベースイメージとして Python 3.11 を使用（軽量で公式）
FROM python:3.11

# 作業ディレクトリを /app に設定（以後の作業はこの中で行う）
WORKDIR /backend

# 依存関係ファイル（requirements.txt）だけ先にコピー
# → キャッシュ効率を上げるため（パッケージ変更がなければ再ビルド不要）
COPY requirements.txt .

# pip をアップグレードし、必要パッケージをインストール
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 起動時にDBが使えるようになるまで待機するためのコマンド（nc）をインストール
RUN apt-get update \
  && apt-get install -y netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*

# アプリケーション本体をコピー（FastAPIのコードなど）
COPY . .

# スクリプトに実行権限を付与
RUN chmod +x entrypoint.sh

# appuser ユーザーを作成し、/app ディレクトリの所有権を変更
RUN useradd -m appuser \
    && chown -R appuser:appuser /backend

# appuserで実行
USER appuser

# コンテナ起動時にスクリプトを自動実行する
ENTRYPOINT ["./entrypoint.sh"]

