"""정비 이력을 터미널에서 컬러 표로 보여주는 명령.

실행: .venv/bin/python -m app.cli history <차량번호>
"""
import sys
import unicodedata

from app import get_history

_COLOR = sys.stdout.isatty()  # 터미널일 때만 색을 쓴다 (파일 저장·파이프에서는 끔)
BOLD = "\033[1m" if _COLOR else ""
CYAN = "\033[36m" if _COLOR else ""
DIM = "\033[2m" if _COLOR else ""
RESET = "\033[0m" if _COLOR else ""
HIGH_COST = 100_000  # 이 금액 이상은 굵게 강조


def _width(text: str) -> int:
    """터미널에서 차지하는 폭을 계산한다 (한글 등 전각 문자는 2칸)."""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def _pad(text: str, width: int, right: bool = False) -> str:
    """전각 문자를 고려해 지정한 폭으로 맞춘다."""
    space = " " * max(0, width - _width(text))
    return space + text if right else text + space


def render_history(plate: str) -> str:
    """차량번호의 정비 이력을 테두리가 있는 컬러 표 문자열로 만든다."""
    rows = [
        (r["date"], f"{r['km']:,} km", r["work"], f"{r['cost']:,}원", r["cost"])
        for r in get_history(plate)
    ]
    if not rows:
        return f"{plate}: 정비 이력이 없습니다."

    headers = ("날짜", "주행거리", "작업", "비용")
    right_align = (False, True, False, True)
    widths = [max(_width(h), *(_width(row[i]) for row in rows)) for i, h in enumerate(headers)]

    def line(left: str, mid: str, end: str) -> str:
        return left + mid.join("─" * (w + 2) for w in widths) + end

    def cells(values, style: str = "") -> str:
        parts = [f" {style}{_pad(v, widths[i], right_align[i])}{RESET if style else ''} "
                 for i, v in enumerate(values)]
        return "│" + "│".join(parts) + "│"

    out = [line("┌", "┬", "┐"), cells(headers, BOLD + CYAN), line("├", "┼", "┤")]
    for *values, cost in rows:
        out.append(cells(values, BOLD if cost >= HIGH_COST else ""))
    out.append(line("└", "┴", "┘"))
    total = sum(row[4] for row in rows)
    out.append(f"{DIM}총 {len(rows)}회 · {total:,}원{RESET}")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    """명령줄 인자를 처리한다."""
    if len(argv) != 2 or argv[0] != "history":
        print("사용법: python -m app.cli history <차량번호>")
        return 1
    print(render_history(argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
