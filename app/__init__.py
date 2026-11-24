"""현대화 대상 패키지.

legacy/maintenance.py의 함수를 app/ 안의 새 구현으로 하나씩 바꾸는 중이다.
tests/test_characterization.py는 계속 전부 통과해야 한다.

현대화 완료: get_history (app/history.py), find_recall_targets · recall_status (app/recall.py)
"""

from app.history import get_history  # noqa: F401
from app.recall import find_recall_targets, recall_status  # noqa: F401
from legacy.maintenance import (  # noqa: F401
    add_record,
    monthly_report,
)
