---
name: modernize-function
description: 레거시 함수 하나를 app/ 패키지의 새 구현으로 옮겨 현대화한다. 특성 테스트로 기존 동작을 지키면서 SQL 인젝션과 닫지 않는 DB 연결을 고친다. 사용자가 legacy 함수의 현대화, 이전, 리팩터링, app/으로 옮기기를 요청할 때 사용한다.
---

# 레거시 함수 현대화

legacy/maintenance.py의 함수 하나를 app/ 안의 새 구현으로 바꾼다. 기존 동작은 그대로 둔다.

## Workflow

- [ ] legacy/maintenance.py에서 대상 함수를, tests/test_characterization.py에서 그 함수의 특성 테스트를 읽는다
- [ ] 지켜야 할 현재 동작(반환 형식, 정렬, 경계값, 없는 값 처리)을 3줄 이내로 정리해 먼저 보여 준다
- [ ] app/<주제>.py에 새로 구현한다 (아래 구현 규칙)
- [ ] app/__init__.py에서 그 함수만 새 모듈에서 가져오도록 바꾼다. 나머지는 legacy 그대로 둔다
- [ ] .venv/bin/pytest -q 로 특성 테스트 15개가 전부 통과하는지 확인한다
- [ ] 결과를 표로 요약한다: | 바꾼 것 | 지킨 동작 | 테스트 결과 |

## 구현 규칙

- SQL은 `?` 파라미터 바인딩만 쓴다
- DB 연결은 `contextlib.closing`으로 반드시 닫는다
- DB 경로는 함수가 호출될 때 환경 변수 `MAINT_DB`에서 읽는다 (기본값 `data/maintenance.db`)
- 타입 힌트와 한국어 docstring을 쓴다
- 고객 이름·전화번호는 print나 로그에 남기지 않는다

## Example

**입력**: "get_history를 현대화해 줘"

**기대 결과**: app/history.py 생성(바인딩 + 연결 닫기 + 최신순 정렬 유지), app/__init__.py에서 get_history만 app.history에서 가져옴, 15 passed, 요약 표 한 개

## Constraints

- legacy/ 폴더는 수정하지 않는다
- 테스트를 고쳐서 통과시키지 않는다. 실패하면 구현을 고친다
- 한 번에 함수 하나만 옮긴다
