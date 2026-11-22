#!/usr/bin/env bash
# 실습 환경 준비: 가상환경 + pytest 설치 → 샘플 DB 생성 → 특성 테스트 실행
set -e
cd "$(dirname "$0")"

PY="${PYTHON:-python3.13}"
command -v "$PY" >/dev/null 2>&1 || PY=python3

echo "▶ 1/3 가상환경 만들기 + pytest · mcp 설치 ($PY)"
"$PY" -m venv .venv
# pytest: 특성 테스트 / mcp<2: Lab 4 MCP 서버 구축용 (mcp 2.x는 FastMCP → MCPServer로 API가 바뀜)
.venv/bin/pip install -q --disable-pip-version-check pytest "mcp<2"

echo "▶ 2/3 샘플 DB 만들기"
.venv/bin/python data/seed.py

echo "▶ 3/3 특성 테스트 실행"
.venv/bin/pytest -q

touch hooks/hook.log   # Hook 실행 기록 (tail -f hooks/hook.log 로 확인)

echo ""
echo "🎉 준비 완료! 레거시 프로그램 실행해 보기:"
echo "   .venv/bin/python legacy/maintenance.py history 12가3456"
