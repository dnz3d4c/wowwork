# 지시어·되풀이·"대상" 점검 (2026-11-14)

계기: 사용자 지적 "그 종류의 대상에 사용할 수 있는 템플릿 목록"(basics/menu-and-settings.md, 원문 for that kind of object).

- 에이전트 4개가 51개 파일을 나눠 `brief.md` 기준으로 찾았다. 139건, 메인이 검토해 137건 반영(5건은 수정안을 고침, `findings.tsv` status 열).
- 반영하지 않은 2건: reference/commands.md 169(`/wv quests go`의 "대상"은 koKR 화면 문구 "대상 없음"과 짝이라 설명서만 바꾸면 어긋남), information/monitors.md 270(수정안이 원문에 없는 사실을 더함).
- 유형: 1 지시어 불명, 2 같은 명사 되풀이, 3 target이 아닌 "대상", 4 "그것"·"하나" 직역.

## 원인

1. 번역 단계: 지시어를 명사로 되돌리는 것을 "허용"으로만 적었고 금지 규칙이 없었다. 번역자는 it/that/one을 그대로 옮겼다.
2. 평가 단계: 2026-11-13 독자 관점(유형 ②에 지시어 포함)이 menu-and-settings를 평가했지만 Claude·GPT 모두 이 문장을 통과시켰고 회귀도 놓쳤다(`reviews/2026-11-13-manual-reader/basics/menu-and-settings/`). 여러 유형을 한 번에 보는 관점은 이 부류를 놓친다. 11-13 시험에서 독자 관점 검출이 8건 중 최대 3건이었는데, 고정 표현은 용어집 avoid로 막았지만 지시어처럼 기계로 못 잡는 부류는 대책이 없었다.
3. 기계 검사: 되풀이 패턴 정규식을 시험했으나 고치기 전 본문에서 11건만 잡았고 남은 10건은 자연스러운 쓰임이었다. 정밀도가 낮아 검사로 넣지 않았다.

## 바꾼 것

- `docs/translation-guide.md` 문체: 지시어·대명사·"대상" 금지 조항.
- `tools/review/prompts/manual-translate.md`: 번역 뒤 지시어 자기 점검.
- `tools/review/prompts/manual-lens-style.md`: 지시어·되풀이 따로 한 번 더 보기, 나쁜 예·고친 예.
- `docs/review-process.md` 원칙 6에 ⑥: 만든 단계와 놓친 단계의 지침을 고친다.
- 합치거나 지운 것: 없음. 새 도구·검사는 만들지 않았다.
