#!/usr/bin/env python3
"""[PreToolUse Hook] legacy/ 폴더 수정을 막는다. Claude Code · Kiro CLI 공용.

에이전트가 도구를 쓰기 직전에 실행된다. 도구 정보가 JSON으로 STDIN에 들어온다.
- legacy/ 안의 파일을 쓰거나 고치려 하면 → exit 2 (차단) + 이유를 STDERR로 전달
- 그 외 → exit 0 (허용)

※ 교육용 예시다. 모든 우회 경로를 막는 완벽한 보안 장치는 아니다.
"""
import json
import re
import sys

PATH_KEYS = ("file_path", "path", "filePath", "notebook_path", "target_file")

# 셸 명령 중 legacy/ 를 '변경'하는 패턴만 잡는다 (읽기·실행은 허용)
SHELL_WRITE = [
    r">>?\s*['\"]?[\w./~-]*legacy/",          # 리다이렉션으로 덮어쓰기
    r"\bsed\b[^|;&]*\s-i[^|;&]*legacy/",      # sed -i
    r"\b(rm|mv|truncate|tee|chmod)\b[^|;&]*legacy/",
]

MESSAGE = (
    "🚫 [Hook] legacy/ 폴더는 수정할 수 없습니다 (원본 보존 규칙).\n"
    "   변경은 app/ 폴더에서 하고, legacy/ 는 동작 비교용으로만 읽으세요."
)


def touches_legacy_path(value: str) -> bool:
    v = value.replace("\\", "/")
    return v.startswith("legacy/") or "/legacy/" in v


def collect_paths(obj):
    """tool_input 안의 경로 값을 모두 찾는다 (도구마다 키 이름이 달라서)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in PATH_KEYS and isinstance(v, str):
                yield v
            else:
                yield from collect_paths(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from collect_paths(item)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0  # 입력을 못 읽으면 막지 않는다

    tool_input = event.get("tool_input") or {}

    if any(touches_legacy_path(p) for p in collect_paths(tool_input)):
        print(MESSAGE, file=sys.stderr)
        return 2

    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if isinstance(command, str) and any(re.search(p, command) for p in SHELL_WRITE):
        print(MESSAGE, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
