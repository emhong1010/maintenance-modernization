"""리콜 대상 판별과 진행 현황 — legacy 리콜 함수의 현대화 구현."""

import os
import sqlite3
from contextlib import closing


def _db_path() -> str:
    """DB 경로를 환경 변수 MAINT_DB에서 읽는다 (기본값 data/maintenance.db)."""
    return os.environ.get("MAINT_DB", "data/maintenance.db")


def _recall_period(conn: sqlite3.Connection, code: str):
    """리콜 코드의 대상 차종과 생산 기간을 돌려준다. 없으면 None."""
    return conn.execute(
        f"SELECT model, prod_from, prod_to FROM recalls WHERE code = '{code}'"
    ).fetchone()


def find_recall_targets(code: str) -> list[str]:
    """리콜 조치가 아직 안 된 차량번호를 정렬해서 돌려준다."""
    try:
        with closing(sqlite3.connect(_db_path())) as conn:
            period = _recall_period(conn, code)
            if period is None:
                return []
            model, prod_from, prod_to = period
            rows = conn.execute(
                "SELECT plate, owner_name, owner_phone FROM vehicles "
                "WHERE model = ? AND prod_date BETWEEN ? AND ?",
                (model, prod_from, prod_to),
            ).fetchall()
            targets = []
            for plate, name, phone in rows:
                fixed = conn.execute(
                    "SELECT COUNT(*) FROM records WHERE plate = ? AND work LIKE ?",
                    (plate, f"%{code}%"),
                ).fetchone()[0]
                if fixed == 0:
                    print(f"[리콜 대상] {plate} {name} {phone}")
                    targets.append(plate)
            return sorted(targets)
    except:
        return []


def recall_status(code):
    conn = sqlite3.connect(_db_path())
    period = _recall_period(conn, code)
    if period is None:
        return None
    model, prod_from, prod_to = period
    plates = [
        r[0]
        for r in conn.execute(
            "SELECT plate FROM vehicles WHERE model = ? AND prod_date BETWEEN ? AND ?",
            (model, prod_from, prod_to),
        )
    ]
    done = 0
    for plate in plates:
        n = conn.execute(
            "SELECT COUNT(*) FROM records WHERE plate = ? AND work LIKE ?",
            (plate, f"%{code}%"),
        ).fetchone()[0]
        if n > 0:
            done += 1
    total = len(plates)
    rate = int(done * 100 / total) if total else 0
    return {"code": code, "total": total, "done": done, "remaining": total - done, "rate": rate}
