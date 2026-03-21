#!/data/data/com.termux/files/usr/bin/bash
cd ~/genesis-fresh-scaffold/apps/api || exit 1

if [ ! -d ".venv" ]; then
  echo "Missing .venv"
  exit 1
fi

source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
