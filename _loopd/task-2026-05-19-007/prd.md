# PRD — task-2026-05-19-007

## 배경 / 사용자 요청

원문: "dev-task 테스트해줘"

`test-dev` 리포는 정적 홈페이지(`index.html` / `styles.css` / `scripts.js`)와
`tests/smoke/test_homepage.py`(13개 케이스) 로 구성된 dev-task 샘플
프로젝트다. 이 태스크는 loopd 파이프라인을 한 바퀴 돌리며 **개발 태스크 자체를
테스트**하는 것을 목표로 한다. 즉, 코드 추가보다 **기존 동작이 깨지지 않았음을
재확인**하고, 자주 누락되는 회귀 케이스를 보강한다.

## 목표

1. 기존 smoke 테스트가 깨끗하게 통과하는지 검증 (베이스라인 캡처).
2. 현재 홈페이지의 핵심 회귀 포인트를 추가 smoke 테스트로 잠금:
   - viewport meta 태그 존재 (반응형 기준).
   - 헤더 네비게이션 링크 3개가 각각 존재하는 섹션 id 와 일치.
   - `scripts.js` 가 `defer` 속성으로 로드되어 파싱 차단을 일으키지 않음.
   - CSS 변수(`--color-primary`) 존재 — 디자인 토큰 회귀 방지.
4. 개발자가 한 명령으로 테스트를 돌릴 수 있는 `scripts/run-tests.sh`
   진입점을 추가 (외부 패키지 설치 없이 stdlib + pytest 로 동작).

## 비목표

- 새로운 UI/기능 추가.
- 기존 마크업, 스타일, 스크립트 동작 변경.
- 외부 패키지 설치 (`npm`, `pip install`).
- 워크스페이스 외부 파일 수정.

## Functional Requirements

- **FR-1**: 워크스페이스 루트에서 `pytest -m smoke -v` 실행 시 모든 기존
  테스트(13개)가 PASS 해야 한다. 베이스라인 실행 결과를 plan.md 검증 단계에서
  기록한다.
- **FR-2**: `tests/smoke/test_homepage.py` 에 다음 4개 회귀 테스트 메서드를
  `TestHomepageStructure` 클래스 끝에 추가한다.
  - `test_viewport_meta_present` — `<meta name="viewport" ...>` 존재.
  - `test_nav_links_match_section_ids` — 헤더 `<ul class="nav-links">` 안의
    `href="#..."` 3개가 모두 문서 내 id 와 매칭.
  - `test_scripts_loaded_with_defer` — `<script defer src="scripts.js">` 패턴.
  - `test_css_design_tokens_defined` — `styles.css` 에 `--color-primary` 와
    `--color-bg` CSS 변수가 정의돼 있음.
- **FR-3**: `scripts/run-tests.sh` 진입점을 추가한다.
  - 실행 시 워크스페이스 루트에서 `python -m pytest -m smoke -v` 호출.
  - shebang `#!/usr/bin/env bash`, `set -euo pipefail`.
  - 실행 권한(`chmod +x`) 부여.
- **FR-4**: `pytest.ini` 의 `markers` 섹션은 변경하지 않는다 (회귀 방지).
- **FR-5**: 변경된 파일만 정확히 스테이지하고 커밋 메시지에 task ID 포함.

## Non-Functional Requirements

- **NFR-1**: 모든 신규 코드는 Python 표준 라이브러리만 사용.
- **NFR-2**: 신규 테스트는 기존 fixture (`html_source`, `parsed`, `css_source`,
  `js_source`) 를 재사용. 새 fixture 추가 금지 (FR-2 범위 내 처리 가능).
- **NFR-3**: 신규 테스트 4개 모두 1초 미만 실행.
- **NFR-4**: 기존 13개 테스트의 시그니처/이름/순서를 변경하지 않는다.

## User Stories

- **US-1**: 개발자로서 `bash scripts/run-tests.sh` 한 줄로 dev-task 의 회귀
  테스트를 돌리고 싶다. → FR-3.
- **US-2**: 리뷰어로서 현재 홈페이지의 viewport/네비게이션/스크립트 로딩 회귀를
  자동으로 잡고 싶다. → FR-2.
- **US-3**: loopd 운영자로서 planning→implementation→review 파이프라인이
  한 사이클 정상 동작함을 베이스라인 테스트 통과로 확인하고 싶다. → FR-1.

## Acceptance Criteria

- AC-1: `cd <workspace> && python -m pytest -m smoke -v` 실행 시 총 17개
  테스트 PASS (기존 13 + 신규 4). 0 failure / 0 error.
- AC-2: `bash scripts/run-tests.sh` 실행 시 위와 동일하게 17개 PASS.
- AC-3: `git diff` 결과는 다음 파일만 포함:
  - `tests/smoke/test_homepage.py` (메서드 4개 추가)
  - `scripts/run-tests.sh` (신규)
  - `_loopd/task-2026-05-19-007/*.md` (계획 문서)
- AC-4: 커밋 메시지 prefix 가 `plan:` 또는 `test:` 이고 task ID
  `task-2026-05-19-007` 를 포함.
- AC-5: `index.html`, `styles.css`, `scripts.js` 는 단 한 글자도 변경되지
  않는다.
