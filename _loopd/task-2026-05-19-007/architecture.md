# Architecture — task-2026-05-19-007

## 변경 범위 한 줄 요약

테스트 전용 보강 + 진입 스크립트 추가. 런타임 코드(`index.html`, `styles.css`,
`scripts.js`) 는 **수정하지 않는다**.

## 추가/수정 파일 목록

| 경로 | 작업 | 비고 |
|---|---|---|
| `tests/smoke/test_homepage.py` | 수정 (append-only) | 4개 메서드 추가. 기존 fixture 재사용. |
| `scripts/run-tests.sh` | 신규 | 워크스페이스 루트에서 pytest 진입점. |
| `_loopd/task-2026-05-19-007/prd.md` | 신규 | 본 PRD. |
| `_loopd/task-2026-05-19-007/architecture.md` | 신규 | 본 문서. |
| `_loopd/task-2026-05-19-007/plan.md` | 신규 | Implementation step-by-step. |

수정 금지 파일: `index.html`, `styles.css`, `scripts.js`, `pytest.ini`,
`README.md`, 기존 smoke 테스트 메서드.

## 모듈 / 데이터 흐름

```
+----------------------+        +-------------------------+
| scripts/run-tests.sh | -----> | python -m pytest        |
+----------------------+        |   -m smoke -v           |
                                +------------+------------+
                                             |
                                             v
                          +------------------+-------------------+
                          | tests/smoke/test_homepage.py         |
                          |   fixtures: html_source, parsed,     |
                          |             css_source, js_source    |
                          +------------------+-------------------+
                                             |
                                  reads (read-only)
                                             v
                          +------------------+-------------------+
                          | index.html / styles.css / scripts.js |
                          +--------------------------------------+
```

- 테스트는 모두 file read + 문자열/HTMLParser 검증. 네트워크/브라우저 없음.
- `scripts/run-tests.sh` 는 pure bash, 외부 의존 없음.

## 새 테스트 메서드 설계 (FR-2 매핑)

| 메서드 | 사용 fixture | 검증 내용 |
|---|---|---|
| `test_viewport_meta_present` | `html_source` | `<meta name="viewport"` 부분 문자열 매칭. |
| `test_nav_links_match_section_ids` | `parsed` | `nav-links` 안 href 3개(about/features/contact)가 모두 `parsed.ids` 에 포함. 단, 기존 `test_internal_anchor_links_resolve` 와 중복되지 않도록 **헤더 nav 한정**으로 검사. 이를 위해 추가 HTMLParser 서브클래스 없이 `html_source` 정규식(`<ul class="nav-links">.*?</ul>`)으로 nav 블록만 추출 후 href 수집. |
| `test_scripts_loaded_with_defer` | `html_source` | `'<script defer src="scripts.js">'` 부분 문자열 매칭. |
| `test_css_design_tokens_defined` | `css_source` | `'--color-primary:'` 와 `'--color-bg:'` 두 토큰 모두 존재. |

> 메모: `test_nav_links_match_section_ids` 는 nav 블록만 분리하기 위해 메서드
> 내부 로컬 HTMLParser 를 사용하지 않고, `re.search(r"<ul class=\"nav-links\">(.*?)</ul>", html_source, re.S)` + `re.findall(r'href="#([^"]+)"', block)` 로 처리한다.
> 그리고 추출한 anchor 들은 기존 `parsed.ids` 와 교차 검증.

## 진입 스크립트 설계 (FR-3)

`scripts/run-tests.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"
exec python -m pytest -m smoke -v "$@"
```

- 추가 인자(`"$@"`)를 그대로 pytest 에 전달.
- `exec` 로 PID 절약.

## 의존성

- Python 3.10+ (기존 코드가 `set[str]` 타입 힌트 사용 — 변경 없음).
- pytest (이미 사용 중). 추가 패키지 설치 없음.
- bash 4+ (스크립트).

## 테스트 영향도

- 신규 4개 추가 → 총 17개 PASS 예상.
- 기존 13개는 코드 변경이 없으므로 영향 없음.
- 신규 메서드는 모두 read-only 파일 검증이라 부작용 없음.

## 롤백 전략

문제가 생기면 다음 두 파일만 되돌리면 안전하게 원복:

- `tests/smoke/test_homepage.py` (append 만 제거)
- `scripts/run-tests.sh` (파일 삭제)

런타임 코드(`index.html` 등) 는 건드리지 않으므로 사이트 동작 회귀 위험 0.
