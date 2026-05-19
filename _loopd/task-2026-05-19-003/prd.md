# PRD — task-2026-05-19-003: dev-task 파이프라인 테스트

## 배경
사용자 요청: "dev-task 테스트해줘"

이 task의 목적은 loopd 파이프라인(Planning → Implementation → Review)의 end-to-end 동작을 검증할 수 있는 **작고 안전한 코드 변경**을 수행하는 것이다. 기존 정적 홈페이지(`index.html`, `styles.css`) 위에 의미 있는 작은 기능을 추가하여 파이프라인이 정상적으로 흘러가는지 확인한다.

선택한 검증용 변경: **홈페이지 푸터에 현재 연도를 자동으로 반영하는 JavaScript 스니펫 추가 + 관련 스모크 테스트 보강**. 이 변경은 다음 이유로 적합하다.
- 정적 사이트 구조를 깨지 않는다.
- 기존 pytest 기반 smoke 테스트와 자연스럽게 연결된다.
- 사람이 눈으로 확인할 수 있는 가시적 효과가 있다(연도 표기).

## Functional Requirements
- **FR-1**: `index.html` 푸터의 연도 표기는 하드코딩된 "2026" 대신 페이지 로드 시점에 현재 연도가 자동 렌더링되어야 한다.
- **FR-2**: JavaScript는 외부 의존성 없이 인라인 `<script>` 또는 별도 파일(`scripts.js`)로 제공한다. 추가 빌드 단계가 없어야 한다.
- **FR-3**: JavaScript가 비활성화된 환경에서도 푸터에 fallback 텍스트(기본 연도)가 표시되어야 한다.
- **FR-4**: 푸터 연도 영역은 식별 가능한 DOM 요소(`<span id="footer-year">` 등)로 마킹되어, 추후 검사/테스트가 용이해야 한다.
- **FR-5**: smoke 테스트에 다음 항목을 추가한다.
  - 푸터 연도 span이 존재한다.
  - 연도 갱신 스크립트(혹은 파일)가 페이지에 연결되어 있다.
  - fallback 텍스트가 비어있지 않다.

## Non-Functional Requirements
- **NFR-1 (성능)**: 추가 JavaScript는 1KB 미만이며, 페이지 렌더링을 차단하지 않아야 한다.
- **NFR-2 (호환성)**: 최신 Chrome/Firefox/Safari에서 동작해야 한다. ES5 수준의 단순 문법 사용.
- **NFR-3 (테스트)**: 기존 smoke 테스트(`pytest -m smoke`)가 통과해야 하며, 신규 테스트 포함 전체 통과해야 한다.
- **NFR-4 (안전성)**: workspace 외부 파일을 수정하지 않는다. `index.html`, `styles.css`(필요 시), `tests/smoke/test_homepage.py`, 선택적으로 `scripts.js`만 다룬다.

## User Stories
- **US-1**: 사이트 방문자로서, 푸터의 저작권 연도가 항상 현재 연도로 표시되어 사이트가 관리되고 있다고 신뢰할 수 있다.
- **US-2**: 개발자로서, smoke 테스트로 자동 연도 기능이 회귀 없이 동작하는지 확인할 수 있다.
- **US-3**: loopd 사용자로서, dev-task 파이프라인이 plan/implement/review 모든 단계를 무사히 통과하는지 확인할 수 있다.

## Acceptance Criteria
- **AC-1**: `index.html`을 브라우저에서 열면 푸터의 연도가 현재 연도로 표시된다.
- **AC-2**: `pytest -m smoke`가 0 failure로 통과한다.
- **AC-3**: 신규 smoke 테스트가 최소 3개 추가되어 FR-5의 항목들을 검증한다.
- **AC-4**: `git log`에 plan/implement 단계의 커밋이 명확히 남는다.
- **AC-5**: 코드 변경 diff가 워크스페이스 내부 파일에만 한정된다.

## Out of Scope
- 백엔드/서버 도입.
- 빌드 시스템(webpack, vite 등) 도입.
- 다국어, i18n, 디자인 리뉴얼.
