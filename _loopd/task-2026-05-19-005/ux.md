# UX Spec — task-2026-05-19-005

## 화면 흐름

1. 사용자가 `index.html`을 연다 → 페이지 최상단(스크롤 0) → Back-to-Top 버튼은 **숨김** (opacity 0, pointer-events none).
2. 사용자가 스크롤을 내려 `window.scrollY > 200`이 되는 순간 → 버튼이 우측 하단에서 **페이드 인 + 살짝 위로 슬라이드**되며 등장.
3. 사용자가 버튼을 클릭(또는 Tab 포커스 후 Enter) → 페이지가 **부드럽게** 최상단으로 스크롤. 스크롤이 200px 이하로 들어오는 순간 버튼 자동 숨김.
4. 모바일(viewport ≤ 600px)에서는 우측/하단 마진이 24px → 16px로 감소.

## 컴포넌트: `#back-to-top`

| 속성 | 값 |
|------|-----|
| 태그 | `<button type="button">` |
| 위치 | `position: fixed; right: 24px; bottom: 24px` (모바일 16px) |
| 크기 | 44×44px (터치 타깃 권장 최소) |
| 모양 | `border-radius: 50%` (원형) |
| 배경 | `var(--color-primary)` = `#4f46e5` |
| 호버 | `var(--color-primary-dark)` = `#4338ca` |
| 텍스트 | 유니코드 화살표 `↑` (font-size 1.25rem, color #fff) |
| 그림자 | `var(--shadow-md)` |
| 가시성 토글 | 클래스 `.is-visible` (opacity 0→1, translateY 8px→0) |
| 트랜지션 | `opacity 0.2s, transform 0.2s, background 0.2s` |
| z-index | 200 (sticky header 100보다 위) |
| a11y | `aria-label="맨 위로 이동"`, `title="맨 위로"`, `:focus-visible` outline |

## 상호작용 상태

| 상태 | 시각 | 키보드 |
|------|------|--------|
| 기본 (scrollY ≤ 200) | `opacity: 0; pointer-events: none` — 시각·클릭·포커스 불가 | Tab 순서에서 사실상 비활성 (pointer-events none + opacity 0) |
| 노출 (scrollY > 200) | 원형 보라색 버튼 + 흰 화살표 + 그림자 | Tab으로 포커스 가능, `:focus-visible` 시 강조 outline |
| 호버 | 배경 어두워짐 + 위로 약간 이동 | — |
| 클릭/Enter | 페이지 최상단으로 smooth scroll | Enter 동일 |

## 시각 와이어 (텍스트 다이어그램)

```
+--------------------------------------------------+
| Header (sticky)                                  |
+--------------------------------------------------+
|                                                  |
|  Hero / Sections ...                             |
|                                                  |
|                                                  |
|                                                  |
|                                          ┌────┐  |
|                                          │ ↑  │  |  ← #back-to-top (스크롤 200px 이상일 때 표시)
|                                          └────┘  |
| Footer                                           |
+--------------------------------------------------+
```

## 모션 가이드

- 등장/사라짐 0.2초, 슬라이드 8px.
- 클릭 시 페이지 스크롤은 브라우저 기본 `behavior: 'smooth'` 사용 (별도 easing 라이브러리 없음).
- 사용자 OS의 `prefers-reduced-motion` 별도 처리는 본 task 범위 외 (필요 시 후속 task에서).

## 접근성 체크리스트

- [x] 시맨틱 `<button>` 사용
- [x] `aria-label`로 의미 제공 (아이콘 전용 버튼)
- [x] `title` 속성으로 마우스 호버 힌트
- [x] `:focus-visible` outline으로 키보드 포커스 표시
- [x] 색 대비: 흰색 텍스트 vs `#4f46e5` 배경 (WCAG AA 충족)
