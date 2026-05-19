# Implementation Plan — task-2026-05-19-003

워크스페이스 절대 경로: `/home/sungjin/.loopd/workspaces/task-2026-05-19-003--comojin1994__test-dev`

## Step 1 — `scripts.js` 신규 작성
- 경로: `/home/sungjin/.loopd/workspaces/task-2026-05-19-003--comojin1994__test-dev/scripts.js`
- 내용 (대략):
  ```js
  (function () {
    function setYear() {
      var el = document.getElementById('footer-year');
      if (el) {
        el.textContent = String(new Date().getFullYear());
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', setYear);
    } else {
      setYear();
    }
  })();
  ```

## Step 2 — `index.html` 푸터 마크업 수정
- 경로: `/home/sungjin/.loopd/workspaces/task-2026-05-19-003--comojin1994__test-dev/index.html`
- 변경: 푸터의 `&copy; 2026 MyPage. All rights reserved.` →
  `&copy; <span id="footer-year">2026</span> MyPage. All rights reserved.`
- `</body>` 직전에 `<script defer src="scripts.js"></script>` 추가.

## Step 3 — smoke 테스트 보강
- 경로: `/home/sungjin/.loopd/workspaces/task-2026-05-19-003--comojin1994__test-dev/tests/smoke/test_homepage.py`
- `TestHomepageStructure` 클래스 안에 다음 메서드 추가:
  - `test_footer_year_span_exists(self, html_source)` — `id="footer-year"` 존재 확인.
  - `test_scripts_js_linked(self, html_source)` — `src="scripts.js"` 포함 확인.
  - `test_scripts_js_file_exists(self)` — `ROOT / "scripts.js"` 존재 확인.
  - `test_footer_has_fallback_year(self, html_source)` — span 내부에 4자리 연도 정규식(`\b20\d{2}\b`) 매칭 확인.

## Step 4 — 테스트 실행
- 명령: `cd /home/sungjin/.loopd/workspaces/task-2026-05-19-003--comojin1994__test-dev && python -m pytest -m smoke -v`
- 모든 테스트 통과 확인.

## Step 5 — 커밋
- `git add index.html scripts.js tests/smoke/test_homepage.py`
- 커밋 메시지: `feat: 푸터 연도 자동 갱신 + smoke 테스트 보강 (task-2026-05-19-003)`

## 검증 체크리스트
- [ ] FR-1 ~ FR-5 모두 구현됨
- [ ] `pytest -m smoke` 0 failure
- [ ] 브라우저에서 `index.html` 열 때 푸터 연도가 정상 표시
- [ ] 워크스페이스 외부 파일 수정 없음
- [ ] 커밋 메시지에 task ID 포함

## Implementation 단계가 절대 하지 말아야 할 것
- 외부 패키지 설치 (`npm install`, `pip install` 등).
- `_loopd/` 디렉토리 외에 새로운 문서 파일 생성.
- 기존 smoke 테스트 메서드 시그니처 변경(추가만 허용).
