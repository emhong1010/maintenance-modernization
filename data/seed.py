"""샘플 정비 DB 생성 스크립트.

실행: python data/seed.py  →  data/maintenance.db 생성
테스트는 build(path)를 호출해 매번 새 DB를 만든다.
※ 모든 차량·고객 정보는 실습용 가상 데이터입니다.
"""
import os
import sqlite3
import sys

SCHEMA = """
CREATE TABLE vehicles (
    plate       TEXT PRIMARY KEY,   -- 차량번호
    model       TEXT NOT NULL,      -- 차종
    prod_date   TEXT NOT NULL,      -- 생산일 (YYYY-MM-DD)
    owner_name  TEXT NOT NULL,      -- 고객명 (개인정보)
    owner_phone TEXT NOT NULL       -- 고객 연락처 (개인정보)
);
CREATE TABLE records (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    plate        TEXT NOT NULL REFERENCES vehicles(plate),
    service_date TEXT NOT NULL,     -- 정비일 (YYYY-MM-DD)
    mileage      INTEGER NOT NULL,  -- 주행거리 (km)
    work         TEXT NOT NULL,     -- 작업 내용
    cost         INTEGER NOT NULL   -- 비용 (원)
);
CREATE TABLE recalls (
    code        TEXT PRIMARY KEY,   -- 리콜 코드
    model       TEXT NOT NULL,      -- 대상 차종
    prod_from   TEXT NOT NULL,      -- 대상 생산 시작일
    prod_to     TEXT NOT NULL,      -- 대상 생산 종료일 (포함)
    description TEXT NOT NULL
);
"""

VEHICLES = [
    ("12가3456", "NX-100", "2020-05-10", "김민준", "010-1111-2222"),
    ("23나4567", "VX-200", "2021-02-15", "이서연", "010-2222-3333"),
    ("34다5678", "VX-200", "2021-04-20", "박지호", "010-3333-4444"),
    ("45라6789", "VX-200", "2021-08-05", "최수아", "010-4444-5555"),
    ("56마7890", "VX-200", "2021-12-31", "정하준", "010-5555-6666"),
    ("67바8901", "VX-200", "2022-01-03", "강지우", "010-6666-7777"),
    ("78사9012", "EV-300", "2022-01-01", "조은우", "010-7777-8888"),
    ("89아0123", "EV-300", "2022-03-18", "윤서윤", "010-8888-9999"),
    ("90자1234", "EV-300", "2022-07-01", "장도윤", "010-9999-0000"),
    ("11차2345", "NX-100", "2019-11-30", "임하은", "010-1212-3434"),
    ("22카3456", "EV-300", "2022-05-09", "한시우", "010-5656-7878"),
    ("33타4567", "NX-100", "2023-02-14", "오예린", "010-9090-1212"),
]

RECORDS = [
    ("12가3456", "2023-03-02", 15200, "엔진오일 교환", 80000),
    ("12가3456", "2023-09-14", 22800, "타이어 교환", 520000),
    ("12가3456", "2024-03-05", 30150, "엔진오일 교환", 85000),
    ("23나4567", "2023-06-20", 18000, "브레이크 패드 교환", 150000),
    ("23나4567", "2024-03-11", 27400, "엔진오일 교환", 85000),
    ("34다5678", "2024-02-07", 21000, "리콜 R2024-01 브레이크 호스 교체", 0),
    ("34다5678", "2024-03-19", 23500, "에어컨 필터 교환", 30000),
    ("45라6789", "2023-11-02", 25000, "엔진오일 교환", 80000),
    ("56마7890", "2024-01-15", 9800, "타이어 위치 교환", 40000),
    ("67바8901", "2024-03-22", 12000, "와이퍼 교체", 25000),
    ("78사9012", "2024-02-28", 14000, "리콜 R2024-02 BMS 업데이트", 0),
    ("78사9012", "2024-03-25", 15500, "타이어 위치 교환", 40000),
    ("89아0123", "2023-12-12", 11000, "에어컨 필터 교환", 30000),
    ("90자1234", "2024-04-03", 8000, "정기 점검", 50000),
    ("11차2345", "2023-05-30", 41000, "배터리 교체", 180000),
    ("11차2345", "2024-03-28", 48500, "엔진오일 교환", 85000),
    ("22카3456", "2024-04-17", 7600, "정기 점검", 50000),
    ("33타4567", "2024-03-08", 5200, "정기 점검", 0),
    ("22카3456", "2024-05-02", 8100, "리콜 R2024-02 BMS 업데이트", 0),
]

RECALLS = [
    ("R2024-01", "VX-200", "2021-03-01", "2021-12-31", "브레이크 호스 점검 및 교체"),
    ("R2024-02", "EV-300", "2022-01-01", "2022-06-30", "배터리 관리 시스템(BMS) 소프트웨어 업데이트"),
]


def build(path: str) -> str:
    """path에 샘플 DB를 새로 만든다. 이미 있으면 지우고 다시 만든다."""
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    with con:
        con.executescript(SCHEMA)
        con.executemany("INSERT INTO vehicles VALUES (?, ?, ?, ?, ?)", VEHICLES)
        con.executemany(
            "INSERT INTO records (plate, service_date, mileage, work, cost) VALUES (?, ?, ?, ?, ?)",
            RECORDS,
        )
        con.executemany("INSERT INTO recalls VALUES (?, ?, ?, ?, ?)", RECALLS)
    con.close()
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "maintenance.db")
    build(out)
    print(f"샘플 DB 생성: {out}")
