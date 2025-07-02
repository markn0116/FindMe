# FindMe/frontend/Dockerfile

FROM node:20

WORKDIR /frontend

# create-vite をグローバルにインストール（任意）
RUN npm install -g create-vite

# vue-router をプロジェクトに追加
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# 残りのファイルを全部コピー
COPY . .

# エントリポイントスクリプトをコピー
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# node ユーザーに所有権を変更（開発者が編集しやすくするため）
RUN chown -R node:node /frontend

# nodeユーザーとして実行（セキュアに）
USER node

CMD ["/entrypoint.sh"]
