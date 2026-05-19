# UX Notes — task-2026-05-19-003

## 화면 흐름
사용자는 홈페이지를 방문 → 스크롤 → 푸터에 도달 → 저작권 연도를 본다. 이번 변경은 **푸터에 한해서만** 시각적 영향이 있다.

## 컴포넌트 명세
### Footer
- 위치: `<footer class="footer">` (페이지 최하단, 기존 그대로)
- 내부 마크업:
  ```html
  <p>&copy; <span id="footer-year">2026</span> MyPage. All rights reserved.</p>
  ```
- 스타일: 추가 CSS 없음. 기존 `.footer` 규칙 그대로 적용.
- 동작:
  - 초기 렌더: 정적 fallback 연도 ("2026") 표시.
  - JS 로드 후: `scripts.js`가 `#footer-year`의 텍스트를 `new Date().getFullYear()` 결과로 교체.
  - JS 비활성 환경: fallback 텍스트 유지.

## 접근성
- `<span>`은 의미 정보가 없으므로 별도 `aria-*` 속성 불필요.
- 스크린리더는 일반 텍스트로 연도를 읽어준다.

## 시각적 변화
변경 전: `© 2026 MyPage. All rights reserved.`
변경 후 (예: 실제 연도가 2026이라면): 동일하게 보이지만 차후 연도 변경 시에도 코드 수정 없이 자동 반영됨.

## 디자인 시스템 영향
- 색상/타이포/스페이싱 변경 없음.
- 신규 컴포넌트 없음 (단순 span 추가).
- 다른 화면/페이지 영향 없음 (단일 페이지 사이트).
