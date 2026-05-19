# PRD — task-2026-05-19-005: dev-task 파이프라인 재검증 (Back-to-Top 버튼)

## 배경
사용자 요청: "dev-task 테스트해줘"

이 task의 목적은 loopd 파이프라인(Planning → Implementation → Review)의 end-to-end 동작을 재차 검증하는 것이다. 이전 task(`task-2026-05-19-003`)에서 푸터 연도 자동 갱신 + 스모크 테스트 보강이 이미 머지되어 main에 반영되어 있다. 이번에는 **이전 변경과 충돌하지 않는 또 다른 작고 안전한 가시적 개선**을 수행해 파이프라인을 다시 검증한다.

선택한 검증용 변경: **"맨 위로(Back to Top)" 부드러운 스크롤 버튼 추가 + 관련 스모크 테스트 보강**. 이 변경은 다음 이유로 적합하다.

- 기존 정적 사이트 구조를 깨지 않고, 새로운 DOM 노드/스타일/스크립트가 모두 부가적이다.
- 기존 `scripts.js` 모듈 위에 자연스럽게 얹을 수 있다.
- 이미 `html { scroll-behavior: smooth; }`가 있어 동작이 즉시 시각적으로 확인된다.
- 신규 smoke 테스트로 회귀 보호가 명확하다.

## Functional Requirements
- **FR-1**: 페이지 우측 하단에 고정(`position: fixed`) "Back to Top" 버튼이 존재한다. 식별자는 `id="back-to-top"`.
- **FR-2**: 버튼을 클릭하면 페이지가 최상단(`scrollY = 0`)으로 부드럽게 스크롤된다(`window.scrollTo({ top: 0, behavior: 'smooth' })`).
- **FR-3**: 페이지 최상단(스크롤 ≤ 200px)에서는 버튼이 숨겨지고(`display: none` 또는 `opacity: 0; pointer-events: none`), 그 이상 스크롤하면 표시된다. 토글은 `is-visible` 클래스로 제어한다.
- **FR-4**: 버튼은 키보드 포커스 가능해야 하며 (`<button>` 요소 사용), 접근성 라벨 `aria-label="맨 위로 이동"`을 가진다.
- **FR-5**: JavaScript는 외부 의존성 없이 기존 `scripts.js`에 추가한다. 추가 빌드 단계가 없어야 한다.
- **FR-6**: smoke 테스트에 다음 항목을 추가한다.
  - `id="back-to-top"` 버튼이 `index.html`에 존재한다.
  - 버튼의 `aria-label` 속성이 `"맨 위로 이동"`이다.
  - `styles.css`에 `#back-to-top` 셀렉터와 `.is-visible` 토글 룰이 정의되어 있다.
  - `scripts.js`에 `back-to-top`이라는 문자열과 `scrollTo`가 포함되어 있다.

## Non-Functional Requirements
- **NFR-1 (성능)**: 신규 JavaScript는 추가 1KB 미만이며, scroll 핸들러는 `passive: true`로 등록해 스크롤 성능을 저해하지 않는다.
- **NFR-2 (호환성)**: 최신 Chrome/Firefox/Safari에서 동작한다. ES5/ES6 단순 문법만 사용.
- **NFR-3 (테스트)**: `pytest -m smoke`가 0 failure로 통과한다(기존 + 신규 모두).
- **NFR-4 (안전성)**: 워크스페이스 외부 파일은 절대 수정하지 않는다. 다루는 파일은 `index.html`, `styles.css`, `scripts.js`, `tests/smoke/test_homepage.py` 4개로 제한.
- **NFR-5 (회귀 방지)**: 기존 푸터 연도 기능, 기존 섹션/네비게이션 마크업은 절대 변경하지 않는다.

## User Stories
- **US-1**: 사이트 방문자로서, 긴 페이지를 스크롤한 뒤 한 번의 클릭으로 페이지 상단으로 돌아갈 수 있어 탐색이 편하다.
- **US-2**: 키보드 사용자로서, Tab 포커스를 통해 Back-to-Top 버튼에 접근하고 Enter로 실행할 수 있다.
- **US-3**: 개발자로서, smoke 테스트로 Back-to-Top 버튼이 정적 마크업/스타일/스크립트 차원에서 회귀 없이 유지되는지 확인할 수 있다.
- **US-4**: loopd 사용자로서, dev-task 파이프라인이 이전 task와 충돌 없이 두 번째 라운드도 plan/implement/review 전부를 무사히 통과함을 확인할 수 있다.

## Acceptance Criteria
- **AC-1**: `index.html`을 브라우저에서 열고 200px 이상 스크롤하면 우측 하단에 버튼이 나타난다. 클릭 시 부드럽게 최상단으로 이동한다.
- **AC-2**: `pytest -m smoke`가 0 failure로 통과한다.
- **AC-3**: 신규 smoke 테스트가 최소 4개 추가되어 FR-6의 항목들을 검증한다.
- **AC-4**: `git log`에 `plan: ...`, 그리고 후속 단계의 `feat: ...` 커밋이 명확히 남는다.
- **AC-5**: diff가 `index.html`, `styles.css`, `scripts.js`, `tests/smoke/test_homepage.py`, `_loopd/task-2026-05-19-005/*` 외 파일을 건드리지 않는다.

## Out of Scope
- 백엔드/서버 도입, 빌드 시스템 도입.
- 디자인 리뉴얼, 다크 모드, i18n.
- 푸터 연도 로직 변경(이전 task의 결과물 보존).
- 분석/트래킹 코드 삽입.
