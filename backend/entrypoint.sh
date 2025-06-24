#!/bin/bash
set -e

echo "DBが起動するのを待機中..."
until nc -z db 5432; do
  sleep 1
done

echo "DBマイグレーションを実行中..."

# Alembic マイグレーション：初期テーブル作成
alembic upgrade head

if [ "$APP_ENV" = "development" ]; then
  echo "開発モード（--reload）で起動"
  exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
  echo "本番モードで起動"
  exec uvicorn main:app --host 0.0.0.0 --port 8000
fi
