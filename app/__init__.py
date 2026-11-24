"""현대화 대상 패키지.

legacy/maintenance.py의 함수를 app/ 안의 새 구현으로 하나씩 바꾸는 중이다.
tests/test_characterization.py는 계속 전부 통과해야 한다.

현대화 완료: get_history (app/history.py)
"""

from app.history import get_history  # noqa: F401
from legacy.maintenance import (  # noqa: F401
    add_record,
    find_recall_targets,
    monthly_report,
    recall_status,
)
