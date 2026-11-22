#!/usr/bin/env bash
# [PostToolUse / File Save Hook] Python 파일이 바뀔 때마다 특성 테스트를 자동 실행한다.
# - 통과: exit 0 + 화면 메시지(JSON) → 에이전트도 결과를 알게 된다
# - 실패: exit 2 + 실패 내용을 STDERR로 → 에이전트가 읽고 스스로 고치게 한다
# - 실행할 때마다 hooks/hook.log 에 한 줄 기록 →  tail -f hooks/hook.log  로 실시간 확인
cd "$(dirname "$0")/.." || exit 0
LOG=hooks/hook.log

input="$(cat 2>/dev/null)"
event="$(printf '%s' "$input" | grep -o '"hook_event_name" *: *"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')"
file="$(printf '%s' "$input" | grep -oE '[^"]*\.py' | head -1)"
log() { echo "$(date +%H:%M:%S) [${event:-hook}] $*" >> "$LOG"; }

# 도구 정보가 들어왔는데 .py 파일과 관계없으면 건너뛴다 (문서 수정 등)
if [ -n "$input" ] && [ -z "$file" ]; then
  log "⏭  .py 파일 아님 → 테스트 건너뜀"
  exit 0
fi

if [ ! -x .venv/bin/pytest ]; then
  log "⚠️  .venv 없음 → ./setup.sh 필요"
  echo "⚠️ [Hook] .venv 가 없습니다. ./setup.sh 를 먼저 실행하세요." >&2
  exit 0
fi

out="$(.venv/bin/pytest -q -p no:cacheprovider 2>&1)"; rc=$?
summary="$(printf '%s\n' "$out" | tail -1)"

if [ $rc -eq 0 ]; then
  msg="✅ [Hook] 특성 테스트 통과 — $summary"
  log "✅ ${file##*/} 변경 → $summary"
  # Claude Code: systemMessage = 사용자 화면, additionalContext = 에이전트에게 전달
  printf '{"systemMessage": "%s", "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "%s"}}\n' "$msg" "$msg"
  exit 0
fi

log "❌ ${file##*/} 변경 → $summary"
{
  echo "❌ [Hook] 특성 테스트 실패 — 기존 동작이 바뀌었습니다. 원인을 찾아 고치세요."
  printf '%s\n' "$out" | tail -30
} >&2
exit 2
