# Implementation Plan — task-2026-05-19-007

워크스페이스 절대 경로:
`/home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev`

모든 파일 경로는 절대 경로로 표기. **워크스페이스 외부 파일 수정 금지.**

## Step 0 — 베이스라인 smoke 테스트 실행 (FR-1)

명령:

```
cd /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev \
  && python -m pytest -m smoke -v
```

기대: 13개 PASS, 0 fail. 결과 줄 (`13 passed`) 를 콘솔에서 확인. 실패 시
바로 중단하고 review 단계로 사유 전달.

## Step 1 — `scripts/run-tests.sh` 신규 작성 (FR-3)

- 디렉토리 생성:
  ```
  mkdir -p /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev/scripts
  ```
- 파일 작성:
  파일: `/home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev/scripts/run-tests.sh`
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  cd "$HERE"
  exec python -m pytest -m smoke -v "$@"
  ```
- 실행 권한:
  ```
  chmod +x /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev/scripts/run-tests.sh
  ```

## Step 2 — `tests/smoke/test_homepage.py` 에 회귀 테스트 4개 추가 (FR-2)

- 파일: `/home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev/tests/smoke/test_homepage.py`
- `TestHomepageStructure` 클래스의 **마지막 메서드
  (`test_back_to_top_script_logic`) 바로 다음** 라인에 아래 4개 메서드를
  순서대로 추가. 기존 메서드는 단 한 글자도 수정 금지.
  ```python
      def test_viewport_meta_present(self, html_source):
          assert '<meta name="viewport"' in html_source, (
              "Responsive viewport meta tag must be present in <head>"
          )

      def test_nav_links_match_section_ids(self, html_source, parsed):
          import re
          block = re.search(
              r'<ul class="nav-links">(.*?)</ul>', html_source, re.S
          )
          assert block, "<ul class=\"nav-links\"> block not found"
          hrefs = re.findall(r'href="#([^"]+)"', block.group(1))
          assert hrefs, "nav-links must contain at least one anchor href"
          missing = [h for h in hrefs if h not in parsed.ids]
          assert not missing, (
              f"Nav links point to missing section ids: {missing}"
          )

      def test_scripts_loaded_with_defer(self, html_source):
          assert '<script defer src="scripts.js"></script>' in html_source, (
              "scripts.js must be loaded with defer attribute"
          )

      def test_css_design_tokens_defined(self, css_source):
          assert '--color-primary:' in css_source, (
              "styles.css must define --color-primary design token"
          )
          assert '--color-bg:' in css_source, (
              "styles.css must define --color-bg design token"
          )
  ```
- 새 import 가 모듈 상단에 필요 없도록, `re` 는 `test_nav_links_match_section_ids`
  메서드 내부에서 `import re` 로 처리 (기존 상단 import 영역 미수정).
  > 단, 파일 상단에 이미 `import re` 가 존재하므로 메서드 내부 `import re` 는
  > 실질적으로 no-op. 그래도 명시적 import 를 메서드 본문에 두는 것은 기존
  > 메서드 시그니처/순서 보존 원칙 때문이며, 상단 import 영역을 건드리지
  > 않기 위함이다.

## Step 3 — 신규 테스트 포함 실행 검증 (FR-1, AC-1)

명령:

```
cd /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev \
  && python -m pytest -m smoke -v
```

기대 출력 마지막 줄: `17 passed`. 실패 시 즉시 멈추고 원인 보고.

## Step 4 — 진입 스크립트 동작 검증 (AC-2)

명령:

```
bash /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev/scripts/run-tests.sh
```

기대: Step 3 와 동일하게 17 passed. 추가 인자 패스스루도 동작해야 하므로
선택적으로:

```
bash /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev/scripts/run-tests.sh -k viewport
```

기대: 1 passed, 16 deselected.

## Step 5 — 커밋 (FR-5, AC-4)

- 변경 파일 확인:
  ```
  cd /home/sungjin/.loopd/workspaces/task-2026-05-19-007--comojin1994__test-dev \
    && git status --short
  ```
  기대 항목 (정확히 이 집합):
  - `M tests/smoke/test_homepage.py`
  - `?? scripts/run-tests.sh`
  - `?? _loopd/task-2026-05-19-007/`
- 스테이지:
  ```
  git add tests/smoke/test_homepage.py \
          scripts/run-tests.sh \
          _loopd/task-2026-05-19-007/prd.md \
          _loopd/task-2026-05-19-007/architecture.md \
          _loopd/task-2026-05-19-007/plan.md
  ```
- 커밋 메시지(heredoc):
  ```
  test: smoke 회귀 4종 + 테스트 진입 스크립트 추가 (task-2026-05-19-007)
  ```

## 검증 체크리스트

- [ ] Step 0 베이스라인 13 passed.
- [ ] Step 3 최종 17 passed (기존 13 + 신규 4).
- [ ] Step 4 진입 스크립트로도 17 passed, 인자 패스스루 동작.
- [ ] `index.html`, `styles.css`, `scripts.js`, `pytest.ini`, `README.md` 미수정
      (`git diff -- index.html styles.css scripts.js pytest.ini README.md` 가
      비어 있어야 함).
- [ ] `_loopd/task-2026-05-19-007/` 외부에 새로운 .md 생성 없음.
- [ ] 커밋 메시지에 task ID 포함.

## Implementation 단계가 절대 하지 말아야 할 것

- 런타임 파일(`index.html`/`styles.css`/`scripts.js`) 수정.
- 기존 smoke 테스트 메서드 이름/시그니처/순서 변경.
- 새 pytest 마커 추가 또는 `pytest.ini` 수정.
- 외부 패키지 설치(`pip install`, `npm install` 등).
- 워크스페이스 밖 파일 수정.
- `_loopd/task-2026-05-19-007/` 외에 새 문서 파일 생성.
- 푸시(push)나 PR 생성 — 그건 review 단계 책임.
