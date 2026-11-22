"""모든 테스트가 매번 새 샘플 DB로 시작하도록 준비한다."""
import pytest

from data.seed import build


@pytest.fixture(autouse=True)
def fresh_db(tmp_path, monkeypatch):
    """임시 폴더에 샘플 DB를 만들고 MAINT_DB 환경 변수로 연결한다."""
    path = build(str(tmp_path / "maintenance.db"))
    monkeypatch.setenv("MAINT_DB", path)
    return path
