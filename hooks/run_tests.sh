#!/usr/bin/env bash
# [PostToolUse / File Save Hook] Python 파일이 바뀔 때마다 특성 테스트를 자동 실행한다.
# - 통과: exit 0 + 한 줄 요약
# - 실패: exit 2 + 실패 내용을 STDERR로 → 에이전트가 읽고 스스로 고치게 한다
cd "$(dirname "$0")/.." || exit 0

input="$(cat 2>/dev/null)"
# 도구 정보가 들어왔는데 .py 파일과 관계없으면 건너뛴다 (문서 수정 등)
if [ -n "$input" ] && ! printf '%s' "$input" | grep -q '\.py'; then
  exit 0
fi

if [ ! -x .venv/bin/pytest ]; then
  echo "⚠️ [Hook] .venv 가 없습니다. ./setup.sh 를 먼저 실행하세요." >&2
  exit 0
fi

out="$(.venv/bin/pytest -q -p no:cacheprovider 2>&1)"; rc=$?
summary="$(printf '%s\n' "$out" | tail -1)"

if [ $rc -eq 0 ]; then
  echo "✅ [Hook] 특성 테스트 통과 — $summary"
  exit 0
fi

{
  echo "❌ [Hook] 특성 테스트 실패 — 기존 동작이 바뀌었습니다. 원인을 찾아 고치세요."
  printf '%s\n' "$out" | tail -30
} >&2
exit 2
