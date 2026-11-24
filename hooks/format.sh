#!/bin/bash
# [PostToolUse Hook] Claude가 고친 .py 파일을 ruff로 자동 포매팅한다.
# 도구 정보가 JSON으로 STDIN에 들어온다 → tool_input.file_path 에 고친 파일 경로가 있다.
file=$(jq -r '.tool_input.file_path // empty')
if [[ "$file" == *.py ]]; then
  uvx ruff format --quiet "$file" >/dev/null 2>&1
  echo "$(date +%H:%M:%S) [PostToolUse] 🎨 포매팅: ${file##*/}" >> "$CLAUDE_PROJECT_DIR/hooks/hook.log"
fi
exit 0
