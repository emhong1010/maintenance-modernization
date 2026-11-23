# CLAUDE.md

이 파일은 Claude Code가 이 저장소에서 작업할 때 참고하는 안내입니다.

## 프로젝트 개요

2009년에 만든 차량 정비 이력 관리 프로그램(`legacy/maintenance.py`)을 현대화하는 프로젝트다.
`app/` 패키지가 새 구현이 들어갈 곳이며, 지금은 legacy 함수를 그대로 다시 내보낸다.
모든 차량·고객 데이터는 실습용 가상 데이터다.

## 자주 쓰는 명령

- 설치 (가상환경 + pytest + mcp, 샘플 DB 생성, 테스트): `./setup.sh`
- 테스트: `.venv/bin/pytest -q`
- 샘플 DB 초기화: `.venv/bin/python data/seed.py`
- 레거시 실행: `.venv/bin/python legacy/maintenance.py [history|add|recall|status|report|admin] ...`
- 정비 이력 표: `.venv/bin/python -m app.cli history <차량번호>`

## 구조

- `legacy/maintenance.py` — 원본 프로그램 (CLI + 함수 5개)
- `app/` — 현대화 대상 패키지 (`app/__init__.py`가 공개 함수 목록)
- `data/seed.py` — 샘플 DB 스키마와 데이터 (vehicles, records, recalls)
- `tests/test_characterization.py` — 기존 동작을 고정한 특성 테스트 15개 (매 테스트마다 임시 DB 사용)
- `hooks/` — 실습용 Hook 스크립트

## 팀 규칙 (반드시 지킬 것)

- `legacy/` 폴더는 절대 수정하지 않는다. 동작 비교용 원본이다.
- 특성 테스트(tests/test_characterization.py) 15개는 항상 통과해야 한다. 테스트를 고쳐서 통과시키지 않는다.
- SQL은 반드시 파라미터 바인딩(`?`)을 쓴다.
- 고객 이름·전화번호 같은 개인정보는 print나 로그에 남기지 않는다.
- DB 경로는 환경 변수 `MAINT_DB`에서 읽는다 (기본값 `data/maintenance.db`).
- 모든 함수에 타입 힌트와 한국어 docstring을 쓴다. 답변도 한국어로 한다.
