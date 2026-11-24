"""리콜 대상 판별과 진행 현황 — legacy 리콜 함수의 현대화 구현."""

import os
import sqlite3
from contextlib import closing


def _db_path() -> str:
    """DB 경로를 환경 변수 MAINT_DB에서 읽는다 (기본값 data/maintenance.db)."""
    return os.environ.get("MAINT_DB", "data/maintenance.db")


def _recall_vehicles(code: str) -> list[tuple[str, bool]] | None:
    """리콜 대상 차량과 조치 여부를 한 번의 쿼리로 돌려준다. 없는 리콜 코드면 None.

    대상: 리콜 차종이면서 생산일이 기간 안(시작일·종료일 포함)인 차량.
    조치 여부: 작업 내용에 리콜 코드가 들어 있는 정비 기록이 있으면 조치 완료.
    """
    with closing(sqlite3.connect(_db_path())) as conn:
        period = conn.execute(
            "SELECT model, prod_from, prod_to FROM recalls WHERE code = ?", (code,)
        ).fetchone()
        if period is None:
            return None
        rows = conn.execute(
            "SELECT v.plate, EXISTS ("
            "  SELECT 1 FROM records r WHERE r.plate = v.plate AND r.work LIKE ?"
            ") FROM vehicles v WHERE v.model = ? AND v.prod_date BETWEEN ? AND ?",
            (f"%{code}%", *period),
        ).fetchall()
    return [(plate, bool(fixed)) for plate, fixed in rows]


def find_recall_targets(code: str) -> list[str]:
    """리콜 조치가 아직 안 된 차량번호를 정렬해서 돌려준다. 없는 리콜 코드면 빈 리스트."""
    vehicles = _recall_vehicles(code)
    if vehicles is None:
        return []
    return sorted(plate for plate, fixed in vehicles if not fixed)


def recall_status(code: str) -> dict | None:
    """리콜 진행 현황(전체·조치·남은 대수, 조치율)을 돌려준다. 없는 리콜 코드면 None.

    조치율은 반올림하지 않고 버린다 (2/3 → 66).
    """
    vehicles = _recall_vehicles(code)
    if vehicles is None:
        return None
    total = len(vehicles)
    done = sum(1 for _, fixed in vehicles if fixed)
    rate = int(done * 100 / total) if total else 0
    return {
        "code": code,
        "total": total,
        "done": done,
        "remaining": total - done,
        "rate": rate,
    }
