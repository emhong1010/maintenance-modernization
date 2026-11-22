"""특성 테스트 (Characterization Tests).

레거시 코드가 '지금 실제로 어떻게 동작하는지'를 그대로 고정한 테스트다.
동작이 이상해 보여도(예: 비율을 반올림하지 않고 버림) 일단은 현재 동작이 기준이다.
현대화 후에도 이 테스트가 전부 통과해야 '기존 동작을 깨지 않았다'고 말할 수 있다.
"""
import app


# ---------- 정비 이력 조회 ----------

def test_get_history_returns_latest_first():
    """이력은 정비일 기준 최신순으로 돌려준다."""
    history = app.get_history("12가3456")
    assert [h["date"] for h in history] == ["2024-03-05", "2023-09-14", "2023-03-02"]


def test_get_history_record_fields():
    """각 이력은 id, date, km, work, cost 키를 가진 dict다."""
    latest = app.get_history("12가3456")[0]
    assert latest == {"id": 3, "date": "2024-03-05", "km": 30150, "work": "엔진오일 교환", "cost": 85000}


def test_get_history_unknown_plate_returns_empty():
    """없는 차량은 빈 리스트를 돌려준다."""
    assert app.get_history("00없0000") == []


# ---------- 정비 이력 등록 ----------

def test_add_record_returns_new_id_and_appears_first():
    """등록하면 새 id를 돌려주고, 조회 시 가장 앞에 나온다."""
    new_id = app.add_record("12가3456", "2024-06-01", 32000, "엔진오일 교환", 85000)
    assert new_id == 20
    assert app.get_history("12가3456")[0]["id"] == 20


def test_add_record_unknown_plate_returns_minus_one():
    """없는 차량이면 -1을 돌려주고 아무것도 저장하지 않는다."""
    assert app.add_record("00없0000", "2024-06-01", 1000, "정기 점검", 50000) == -1
    assert app.get_history("00없0000") == []


def test_add_record_invalid_mileage_is_saved_as_zero():
    """주행거리가 숫자가 아니면 0으로 저장한다."""
    app.add_record("12가3456", "2024-06-01", "abc", "정기 점검", 50000)
    assert app.get_history("12가3456")[0]["km"] == 0


def test_add_record_negative_cost_is_saved_as_zero():
    """비용이 음수면 0으로 저장한다."""
    app.add_record("12가3456", "2024-06-01", 32000, "정기 점검", -5000)
    assert app.get_history("12가3456")[0]["cost"] == 0


# ---------- 리콜 대상 판별 ----------

def test_recall_targets_include_boundary_dates():
    """생산일이 리콜 기간 경계(시작일·종료일)와 같아도 대상에 포함한다."""
    assert app.find_recall_targets("R2024-01") == ["45라6789", "56마7890"]


def test_recall_targets_exclude_already_fixed():
    """이미 리콜 조치 이력이 있는 차량은 제외한다."""
    assert app.find_recall_targets("R2024-02") == ["89아0123"]


def test_recall_targets_unknown_code_returns_empty():
    """없는 리콜 코드는 빈 리스트를 돌려준다."""
    assert app.find_recall_targets("R9999-99") == []


def test_recall_target_disappears_after_fix_is_recorded():
    """리콜 조치를 등록하면 대상에서 빠진다."""
    app.add_record("45라6789", "2024-06-10", 30000, "리콜 R2024-01 브레이크 호스 교체", 0)
    assert app.find_recall_targets("R2024-01") == ["56마7890"]


# ---------- 리콜 진행 현황 ----------

def test_recall_status_rate_is_truncated_not_rounded():
    """조치율은 반올림하지 않고 버린다 (2/3 = 66.6% → 66)."""
    assert app.recall_status("R2024-02") == {
        "code": "R2024-02", "total": 3, "done": 2, "remaining": 1, "rate": 66,
    }


def test_recall_status_unknown_code_returns_none():
    """없는 리콜 코드는 None을 돌려준다."""
    assert app.recall_status("R9999-99") is None


# ---------- 월별 리포트 ----------

def test_monthly_report():
    """월별 건수, 총비용, 평균비용(버림), 가장 많은 작업을 돌려준다."""
    assert app.monthly_report(2024, 3) == {
        "month": "2024-03", "count": 7, "total": 350000, "avg": 50000, "top_work": "엔진오일 교환",
    }


def test_monthly_report_empty_month():
    """정비가 없는 달은 0과 None을 돌려준다."""
    assert app.monthly_report(2022, 1) == {
        "month": "2022-01", "count": 0, "total": 0, "avg": 0, "top_work": None,
    }
