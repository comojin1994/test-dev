# Architecture — task-2026-05-19-003

## 변경 대상 파일
| 파일 | 상태 | 변경 내용 |
|------|------|-----------|
| `index.html` | 수정 | 푸터 연도 영역에 `<span id="footer-year">` 추가, 인라인 또는 외부 `<script>` 태그 삽입 |
| `scripts.js` | 신규 (선택) | `document.getElementById('footer-year').textContent = new Date().getFullYear();` |
| `tests/smoke/test_homepage.py` | 수정 | 푸터 연도 관련 smoke 테스트 추가 |
| `_loopd/task-2026-05-19-003/*.md` | 신규 | PRD / Architecture / Plan 문서 |

## 데이터 흐름
```
[페이지 로드]
   └── HTML 파싱 → <footer> 내 <span id="footer-year">2026</span> 기본값 렌더
   └── <script defer src="scripts.js"> 실행
        └── DOM 준비 후 span.textContent ← new Date().getFullYear()
   └── 사용자는 항상 최신 연도를 본다
```

## 모듈/의존성
- **런타임**: 브라우저 표준 DOM API만 사용. 외부 라이브러리 없음.
- **테스트**: 기존 pytest + html.parser(stdlib). 추가 의존성 없음.
- **빌드**: 없음. 정적 파일 그대로 서빙.

## 디자인 결정
- **결정 1: 인라인 vs 외부 파일** → 외부 파일(`scripts.js`)을 선택. 추후 확장성과 캐시 효율을 위해.
- **결정 2: defer vs DOMContentLoaded** → `<script defer>`로 단순화. 별도 이벤트 리스너 불필요.
- **결정 3: fallback 텍스트** → 작성 시점 연도("2026")를 그대로 유지. JS 비활성 환경에서도 의미 있는 값을 보여줌.

## 위험 요소 & 완화
- **R-1**: JS가 동작하지 않는 경우 — fallback 정적 텍스트로 해결(FR-3).
- **R-2**: pytest가 실제 JS 실행을 검증하지 못함 — 정적 HTML 검증(span 존재, script 링크)으로 우회.
- **R-3**: 워크스페이스 외부 변경 위험 — Plan 단계에서 모든 파일 경로를 절대 경로로 명시.

## 테스트 전략
- 기존: `TestHomepageStructure` 클래스 → 그대로 유지, 절대 깨지 않는다.
- 신규: 동일 클래스에 다음 케이스 추가
  - `test_footer_year_span_exists`
  - `test_scripts_js_linked`
  - `test_footer_has_fallback_year`
- `scripts.js` 파일 존재 검증도 추가.

## 롤백 계획
loopd hook 또는 사용자가 작업을 거부할 경우, brunch `loopd/task-2026-05-19-003`를 폐기하면 main에 영향 없음.
