"""정비 이력 조회 — legacy get_history의 현대화 구현."""

import os
import sqlite3
from contextlib import closing


def _db_path() -> str:
    """DB 경로를 환경 변수 MAINT_DB에서 읽는다 (기본값 data/maintenance.db)."""
    return os.environ.get("MAINT_DB", "data/maintenance.db")


def get_history(plate: str) -> list[dict]:
    """차량번호의 정비 이력을 정비일 최신순으로 돌려준다.

    legacy와 같은 형식의 딕셔너리 목록을 돌려준다 (id, date, km, work, cost).
    이력이 없거나 없는 차량이면 빈 리스트를 돌려준다.
    """
    with closing(sqlite3.connect(_db_path())) as conn:
        rows = conn.execute(
            "SELECT id, service_date, mileage, work, cost FROM records "
            "WHERE plate = ? ORDER BY service_date DESC",
            (plate,),
        ).fetchall()
    return [
        {"id": r[0], "date": r[1], "km": r[2], "work": r[3], "cost": r[4]} for r in rows
    ]
