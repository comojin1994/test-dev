# Implementation Plan — task-2026-05-19-005

워크스페이스 절대 경로: `/home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev`

모든 경로는 절대 경로로 표기. **워크스페이스 외부 파일 수정 금지.**

## Step 1 — `index.html` 에 Back-to-Top 버튼 추가
- 파일: `/home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev/index.html`
- 위치: `</footer>` 바로 다음, `<script defer src="scripts.js"></script>` 바로 앞 라인에 다음 한 줄 삽입.
  ```html
  <button id="back-to-top" type="button" aria-label="맨 위로 이동" title="맨 위로">↑</button>
  ```
- 다른 마크업/들여쓰기 변경 금지. 푸터의 `<span id="footer-year">2026</span>` 등은 그대로 유지.

## Step 2 — `styles.css` 끝에 Back-to-Top 스타일 append
- 파일: `/home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev/styles.css`
- 파일 마지막 줄 뒤에 새 섹션 추가:
  ```css
  /* Back to Top */
  #back-to-top {
    position: fixed;
    right: 24px;
    bottom: 24px;
    width: 44px;
    height: 44px;
    border: none;
    border-radius: 50%;
    background: var(--color-primary);
    color: #fff;
    font-size: 1.25rem;
    line-height: 1;
    cursor: pointer;
    box-shadow: var(--shadow-md);
    opacity: 0;
    pointer-events: none;
    transform: translateY(8px);
    transition: opacity 0.2s, transform 0.2s, background 0.2s;
    z-index: 200;
  }
  #back-to-top.is-visible {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
  }
  #back-to-top:hover {
    background: var(--color-primary-dark);
  }
  #back-to-top:focus-visible {
    outline: 2px solid var(--color-primary-dark);
    outline-offset: 2px;
  }
  @media (max-width: 600px) {
    #back-to-top {
      right: 16px;
      bottom: 16px;
    }
  }
  ```
- 기존 룰 수정/삭제 금지.

## Step 3 — `scripts.js` 에 setupBackToTop 추가
- 파일: `/home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev/scripts.js`
- 기존 IIFE의 `setYear` 정의 다음, `if (document.readyState === 'loading')` 분기 이전에 `setupBackToTop` 함수 정의 추가. 그리고 분기 안의 호출을 `init`(둘 다 호출)로 묶음.
- 최종 결과는 다음과 동일하게.
  ```js
  (function () {
    function setYear() {
      var el = document.getElementById('footer-year');
      if (el) {
        el.textContent = String(new Date().getFullYear());
      }
    }

    function setupBackToTop() {
      var btn = document.getElementById('back-to-top');
      if (!btn) return;
      function onScroll() {
        if (window.scrollY > 200) {
          btn.classList.add('is-visible');
        } else {
          btn.classList.remove('is-visible');
        }
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
      onScroll();
    }

    function init() {
      setYear();
      setupBackToTop();
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  })();
  ```

## Step 4 — smoke 테스트 보강
- 파일: `/home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev/tests/smoke/test_homepage.py`
- 파일 상단 fixture 영역에 신규 fixture 두 개 추가 (기존 `html_source`, `parsed`는 변경하지 않음):
  ```python
  @pytest.fixture(scope="module")
  def css_source() -> str:
      return CSS_FILE.read_text(encoding="utf-8")

  @pytest.fixture(scope="module")
  def js_source() -> str:
      return JS_FILE.read_text(encoding="utf-8")
  ```
- `TestHomepageStructure` 클래스 **끝**에 다음 4개 메서드 추가 (기존 메서드 시그니처/순서 불변):
  ```python
  def test_back_to_top_button_present(self, html_source):
      assert 'id="back-to-top"' in html_source, (
          "<button id=\"back-to-top\"> must exist in index.html"
      )

  def test_back_to_top_has_aria_label(self, html_source):
      assert 'aria-label="맨 위로 이동"' in html_source, (
          "Back-to-top button must expose Korean aria-label for a11y"
      )

  def test_back_to_top_styles_defined(self, css_source):
      assert "#back-to-top" in css_source, (
          "styles.css must define #back-to-top rules"
      )
      assert ".is-visible" in css_source, (
          "styles.css must define .is-visible toggle rule"
      )

  def test_back_to_top_script_logic(self, js_source):
      assert "back-to-top" in js_source, (
          "scripts.js must reference back-to-top element"
      )
      assert "scrollTo" in js_source, (
          "scripts.js must call window.scrollTo for smooth scroll"
      )
  ```

## Step 5 — 테스트 실행
- 명령:
  ```
  cd /home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev && python -m pytest -m smoke -v
  ```
- 기대: 기존 9개 + 신규 4개 = 13개 테스트 모두 PASS.

## Step 6 — 커밋
- 스테이지: `git add index.html styles.css scripts.js tests/smoke/test_homepage.py`
- 커밋 메시지: `feat: 맨 위로 이동 버튼 + smoke 테스트 보강 (task-2026-05-19-005)`
- 푸시는 review/CI 단계에서 처리. Implementation 단계에서는 로컬 커밋까지만.

## 검증 체크리스트
- [ ] FR-1 ~ FR-6 모두 구현됨
- [ ] `pytest -m smoke` 0 failure (13개 PASS)
- [ ] 브라우저에서 `index.html` 열고 스크롤 시 우측 하단 버튼 등장/사라짐 + 클릭 시 최상단으로 부드럽게 스크롤
- [ ] 워크스페이스 외부 파일 수정 없음
- [ ] 기존 푸터 연도 자동 갱신 기능 정상 (회귀 없음)
- [ ] 커밋 메시지에 task ID 포함

## Implementation 단계가 절대 하지 말아야 할 것
- 외부 패키지 설치 (`npm install`, `pip install` 등).
- `_loopd/task-2026-05-19-005/` 외에 새로운 문서(.md) 파일 생성.
- 기존 smoke 테스트 메서드 시그니처/이름 변경(추가만 허용).
- `scripts.js`의 기존 `setYear` 동작 변경.
- `styles.css`의 기존 룰(특히 `.header`, `.footer`, `.hero`, `.card`) 수정.
- `index.html`의 기존 섹션 마크업 수정.
