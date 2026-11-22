"""현대화 대상 패키지.

지금은 legacy/maintenance.py를 그대로 감싸고만 있다.
목표: 이 함수들을 app/ 안의 새 구현으로 하나씩 바꾸되,
tests/test_characterization.py는 계속 전부 통과해야 한다.
"""
from legacy.maintenance import (  # noqa: F401
    add_record,
    find_recall_targets,
    get_history,
    monthly_report,
    recall_status,
)
