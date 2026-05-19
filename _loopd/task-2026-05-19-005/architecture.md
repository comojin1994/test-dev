# Architecture — task-2026-05-19-005

워크스페이스 절대 경로: `/home/sungjin/.loopd/workspaces/task-2026-05-19-005--comojin1994__test-dev`

## 영향 받는 파일

| 파일 | 변경 유형 | 설명 |
|------|-----------|------|
| `index.html` | 수정 | `<main>` 종료 직후, `</body>` 직전에 `<button id="back-to-top" aria-label="맨 위로 이동">↑</button>` 추가. 기존 footer/script 태그는 그대로 유지. |
| `styles.css` | 수정 | 파일 끝에 `#back-to-top` 기본 스타일과 `.is-visible` 토글, 반응형 위치 보정을 append-only로 추가. |
| `scripts.js` | 수정 | 기존 즉시실행함수(IIFE) 내부에 `setupBackToTop()` 함수 추가 및 `DOMContentLoaded`/`scroll` 리스너 등록. 기존 `setYear()` 로직은 보존. |
| `tests/smoke/test_homepage.py` | 수정 | 기존 `TestHomepageStructure` 클래스에 신규 메서드 4개 추가. 기존 메서드 시그니처/이름 불변. |

## 데이터 흐름

```
[Browser load]
    │
    ▼
parse index.html ──► <button id="back-to-top"> rendered hidden (no .is-visible)
    │
    ▼
scripts.js IIFE → DOMContentLoaded
    ├── setYear()              (기존)
    └── setupBackToTop()       (신규)
            │
            ├── scroll listener (passive)
            │      └── window.scrollY > 200 ? add('is-visible') : remove
            │
            └── click listener
                   └── window.scrollTo({ top: 0, behavior: 'smooth' })
```

## DOM 구조 (신규 추가 부분)

```html
<button id="back-to-top" type="button" aria-label="맨 위로 이동" title="맨 위로">
  ↑
</button>
```

- `<button>`을 선택: 기본 포커스/Enter 동작을 무료로 얻음.
- 텍스트는 유니코드 화살표(↑). 아이콘 폰트/SVG 불필요 → 의존성 0.

## CSS 토큰/규칙

기존 `:root` 변수(`--color-primary`, `--radius`, `--shadow-md`) 재사용.

```css
#back-to-top {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 44px; height: 44px;
  border: none;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  font-size: 1.25rem;
  cursor: pointer;
  box-shadow: var(--shadow-md);
  opacity: 0;
  pointer-events: none;
  transform: translateY(8px);
  transition: opacity .2s, transform .2s, background .2s;
  z-index: 200;  /* sticky header(100)보다 위 */
}
#back-to-top.is-visible {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}
#back-to-top:hover { background: var(--color-primary-dark); }
@media (max-width: 600px) {
  #back-to-top { right: 16px; bottom: 16px; }
}
```

## JavaScript 구조

기존 IIFE를 유지하면서 함수 두 개를 호출하는 형태로 확장.

```js
(function () {
  function setYear() { /* 기존 */ }

  function setupBackToTop() {
    var btn = document.getElementById('back-to-top');
    if (!btn) return;
    function onScroll() {
      if (window.scrollY > 200) btn.classList.add('is-visible');
      else btn.classList.remove('is-visible');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    onScroll(); // 초기 상태
  }

  function init() { setYear(); setupBackToTop(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

## 의존성

- 신규 외부 의존성 없음. (npm 패키지, CDN, 아이콘 폰트 모두 사용하지 않음.)
- 기존 의존성: Python 표준 라이브러리 + `pytest` (이미 사용 중).

## 테스트 전략

- **정적 검사 위주**: 브라우저 자동화(Playwright/Selenium) 없이 HTML/CSS/JS 텍스트를 정규식·substring으로 검증.
- 기존 `_AnchorCollector` HTMLParser와 호환 — `<button>`에는 `href`가 없어 anchor 링크 검사에 영향 없음.
- 신규 fixture 불필요. 기존 `html_source` fixture 재사용 + 신규 `css_source`, `js_source` 인라인 로드.

## 위험 및 완화

| 위험 | 완화 |
|------|------|
| sticky header(z-index: 100)와 충돌 | `#back-to-top` z-index를 200으로 설정 |
| 모바일에서 footer 텍스트와 겹침 | 우측 하단 24px(모바일 16px) 마진, footer 위에 떠 있어도 클릭 영역 보장 |
| scroll listener 성능 저하 | `{ passive: true }`로 등록 |
| 기존 smoke 테스트 회귀 | 기존 메서드 절대 변경 금지. append-only 정책 |
| 기존 푸터 연도 기능 회귀 | `setYear()` 로직 불변, 호출만 `init()`로 묶음 |
