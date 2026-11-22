#!/usr/bin/env python3
"""Lab 4용 Hook 설치 스크립트.

  python3 hooks/install.py claude   # .claude/settings.json 에 hooks 블록을 합친다
  python3 hooks/install.py kiro     # .kiro/hooks/ 에 Hook 파일을 복사한다
  python3 hooks/install.py remove   # 둘 다 제거 (실습 초기화)
"""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = ROOT / "hooks" / "config"
CLAUDE_SETTINGS = ROOT / ".claude" / "settings.json"
KIRO_HOOKS = ROOT / ".kiro" / "hooks"


def install_claude() -> None:
    settings = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8")) if CLAUDE_SETTINGS.exists() else {}
    settings["hooks"] = json.loads((CONFIG / "claude-hooks.json").read_text(encoding="utf-8"))["hooks"]
    CLAUDE_SETTINGS.parent.mkdir(exist_ok=True)
    CLAUDE_SETTINGS.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Claude Code Hook 설치: {CLAUDE_SETTINGS.relative_to(ROOT)}  → 새 채팅을 시작하세요")


def install_kiro() -> None:
    KIRO_HOOKS.mkdir(parents=True, exist_ok=True)
    for f in (CONFIG / "kiro").glob("*.json"):
        shutil.copy(f, KIRO_HOOKS / f.name)
        print(f"✅ Kiro Hook 설치: .kiro/hooks/{f.name}")
    print("   → kiro-cli chat 을 다시 시작하세요")


def remove() -> None:
    if CLAUDE_SETTINGS.exists():
        settings = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8"))
        if settings.pop("hooks", None) is not None:
            CLAUDE_SETTINGS.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("🧹 Claude Code Hook 제거")
    for f in (CONFIG / "kiro").glob("*.json"):
        (KIRO_HOOKS / f.name).unlink(missing_ok=True)
    print("🧹 Kiro Hook 제거")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    {"claude": install_claude, "kiro": install_kiro, "remove": remove}.get(
        action, lambda: print(__doc__)
    )()
