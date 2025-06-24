#!/bin/bash

# -e: 途中でエラーが発生したらスクリプトを即終了
# -x: 実行される各コマンドを表示（デバッグ用）
set -ex

# 作業ディレクトリへ移動（Viteプロジェクトのルート）
cd /frontend

echo "実行ユーザー: $(id -u):$(id -un)"

# 初回のみ Vite プロジェクトを自動生成（template: vue）
if [ ! -f "package.json" ]; then
  echo "Viteプロジェクトを作成中..."

  # 非対話でプロジェクトを生成
  create-vite vite-tmp --template vue --no

  # 必要なファイルだけルートへ移動（2>/dev/null || true で移動失敗時も無視）
  mv vite-tmp/README.md vite-tmp/index.html vite-tmp/package.json vite-tmp/public vite-tmp/src vite-tmp/vite.config.js . 2>/dev/null || true
  mv vite-tmp/.gitignore vite-tmp/.vscode . 2>/dev/null || true

  # 一時フォルダ削除
  rm -rf vite-tmp
fi

# 所有権を node ユーザーに変更（WSLやVSCodeから編集可能にするため）
if [ "$(id -u)" = "0" ]; then
  chown -R node:node /frontend
fi

# 開発サーバを起動（ホストからアクセス可能に）
echo "開発サーバを起動中..."
npm run dev -- --host
