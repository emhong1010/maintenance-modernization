# 차량 정비 이력 시스템 — 현대화 프로젝트

2009년에 만들어진 정비 이력 관리 프로그램을 현대화하는 실습용 프로젝트입니다.
※ 모든 차량·고객 정보는 가상 데이터입니다.

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `legacy/maintenance.py` | 기존 프로그램 (원본) |
| `app/` | 현대화 대상 패키지 — 지금은 legacy를 감싸고만 있음 |
| `data/seed.py` | 샘플 DB 생성 스크립트 → `data/maintenance.db` |
| `tests/` | 특성 테스트 (기존 동작을 고정한 테스트) |
| `hooks/` | 실습용 Hook 스크립트 |

## 시작하기

```bash
./setup.sh
```

## 레거시 프로그램 실행

```bash
.venv/bin/python legacy/maintenance.py history 12가3456    # 정비 이력 조회
.venv/bin/python legacy/maintenance.py recall R2024-01     # 리콜 미조치 차량
.venv/bin/python legacy/maintenance.py status R2024-02     # 리콜 진행 현황
.venv/bin/python legacy/maintenance.py report 2024 3       # 월별 리포트
```

## 테스트

```bash
.venv/bin/pytest
```
