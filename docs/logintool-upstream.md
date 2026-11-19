# WoW Login Tool 한국어 지원: 원본 저장소 기여 절차

원본은 `Sku75/Sku-WoW-Addon-TBC`의 `logintool/`이다. 원본 규약(`dev/FOREVER-PRS.md`)에 따라 큰 주제는 PR 전에 이슈로 원본 관리자(JeanStiletto)와 먼저 상의한다.

## 진행 상황

| 단계 | 누가 | 상태 |
|------|------|------|
| 1. `ko`를 원본 `main` 위로 정리하고 PR 단위로 브랜치를 나눔 | 작업자 | 완료(2026-11-07): `logintool-fixes` 3커밋, `logintool-korean` 6커밋 |
| 2. 이슈 초안 작성 | 작업자 | 완료(아래 [`## 이슈 초안`](#이슈-초안)) |
| 3. 이슈 게시 | 관리자 승인 후 작업자 | 완료(2026-11-07): https://github.com/Sku75/Sku-WoW-Addon-TBC/issues/37 |
| 4. GitHub 포크 생성(공개), PR 열기(동시에 2개까지) | 원본 관리자 답변 뒤, 관리자 승인 후 작업자 | 대기 |
| 5. 두 클라이언트 게임 테스트(Forever 기능, Anniversary 또는 Era는 변화 없음) | 관리자 | 대기 |

## PR 전에 남은 확인

- 로그인 화면 판별 문구 5개가 리테일 GlobalStrings와 다르다(`로그인`/`접속` 등). 실제 Forever 로그인 화면 캡처로 확정해야 한다.
- 경험 사전 설정 카드의 한국어 문구(`gFvPresetCards` "ko")는 화면에서 확인한 기록이 없다. 실제 화면 문구로 바꿔야 한다.
- 게임 종류 고정 시 pid 수정 뒤에도 SAPI2SR 말 기록 링이 비어 있었다(`last=0`). 게임 낭독이 실제로 들리는지 사용자 확인이 필요하다.
- `koKR.txt` 번역 품질 평가: 완료(2026-11-07). 평가 구조 검증 통과, 지적 178건 중 변경 85건, 지시문 합니다체 변환 36건, 회귀 확인 3회차 통과. 기록 `reviews/2026-11-07-logintool/`

## 이슈 초안

제목: Login tool: Korean (koKR) on WoW Forever - proposal, and three fixes for all clients found on the way

```
Hi JeanStiletto,

I maintain a Korean localization of WowVision and want Korean players on
WoW Forever (Korean client) to use the login tool. I have it working on a
branch and would like to ask how you want it before opening PRs.

## Fixes that affect all clients (would come first, as their own PR)

1. A pinned game type never records the client's pid. The first-start
   setup always pins (GametypeSelectAction), and ApplyDetectedGametype
   returns before gDetectedPid is set. On Forever the speech history is
   asked for by that pid, so it is never asked for: the log has no
   "speech history asked for WoW pid" line and every hover counts as a
   silent repeat. With the fix the pid and the request show up at start-up.
2. Character cards are keyed by their OCR label. A silent repeat looks the
   client's narration up by target key, so a name that OCR reads
   differently between reads misses it and the tool says the misread name.
   The fix gives a card an id from its place and level, like the name
   boxes and race slots already have.
3. After a helper "sense error" the page state is dropped and the helper
   restarted (it stayed on a stale page before).

## Korean support

- koKR tool strings, "Korean" in the setup, a Korea region, ko-KR OCR,
  the Korean window title, Korean screen anchors and colour words in
  forever.ahk (same Map pattern as de/fr).
- The helper enlarges the capture 2x and inverts it before Korean OCR.
- The Korean level line is "%d 레벨 %s". OCR reads the level word wrongly in
  small windows, and names may contain it, so for koKR the level line is
  known by its shape (a level and two words).

Measurement: 1300 Korean names (all 2350 common syllables, rare syllables,
real words, Latin names) drawn in game with the character-select fonts
(GlueFontNormalHuge / GlueFontNormalLarge, card atlas) at five scales,
read by the helper. Names are read exactly only 17-27 % of the time,
whatever the preprocessing (none, 2x, 3x, inverted, grey, threshold) -
a limit of Windows OCR for Korean. That is why the tool has to rely on
the client's own narration for names, and why fixes 1 and 2 matter.

## Questions

1. Is Korean welcome in the login tool, and in which form (one PR for
   Korean, after the fixes)?
2. Fine to gate the helper's 2x/invert step on the ko OCR language as it
   is now, or do you prefer it for all languages?
3. Observation, not fixed: on the ruleset page the card titles are looked
   for with the default scale (height/900 = 1.2 here) while this client
   measures 1.019 on the character list, so the cards were missed.

Not yet verified on screen: the Korean login-page anchors and the Korean
experience-preset card texts.
```
