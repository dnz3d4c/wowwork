---
name: kokr-translation
description: WowVision koKR 번역(vision-locale/koKR/*.lua)을 새로 쓰거나 고칠 때 적용. 원본 병합 뒤 새 키 번역, 사용자 지적으로 기존 번역 수정, 공유 키 문맥 확인, 설치 프로그램 payload 재생성까지의 순서와 각 단계의 기준 문서를 짚는다. "koKR", "번역", "번역 수정", "새 키", "sync_locale", "용어집", "조사", "payload" 작업에 사용.
---

# koKR 번역

이 스킬은 **순서와 위치만** 가집니다. 규칙 본문은 아래 문서에 있고, 여기에 베끼지 않습니다(`CLAUDE.md` `## 도구를 늘리지 않는다`). 규칙과 이 스킬이 다르면 문서가 맞습니다.

| 무엇 | 어디 |
|------|------|
| 번역 규칙(파일 형식, 서식 지정자, 용어, 문체) | `docs/translation-guide.md` |
| 평가 절차(번역자와 평가자 분리, 두 회사 판정) | `docs/review-process.md` |
| 사용자 결정 | `docs/decisions.tsv` |
| 확정 용어, 되돌린 번역 | `docs/glossary.tsv` |
| payload와 설치 프로그램 재빌드 | `docs/builds.md` `## 다시 만드는 법` |

모든 명령은 wowwork 루트에서 실행합니다. 번역 파일은 `../wowvision-ko/vision-locale/koKR/`에 있고 그 저장소의 `main` 브랜치에 커밋합니다.

## 0. 시작 전에

1. `uv run pytest -q`가 초록인지 봅니다. 빨간 상태에서 시작하면 내가 깨뜨렸는지 원래 그랬는지 가릴 수 없습니다.
2. 고칠 키가 `docs/decisions.tsv`에 사용자 결정으로 있는지 찾습니다. 있으면 그 결정을 따르고 다시 정하지 않습니다.
3. 많은 키에 걸리는 방침(문체, 용어 하나를 여러 곳에서 바꾸기)이면 대량 작업 전에 사용자 결정을 받습니다(`review-process.md` 원칙 7).

## 1. koKR은 `tools.sync_locale`로만 고친다

손으로 `koKR/*.lua`를 일괄 치환하지 않습니다. 같은 값을 쓰는 다른 키를 잘못 바꾼 사례가 있고, 손으로 고치면 설명서 인용이 따라가지 않습니다.

- 새 키: `translation-guide.md` `## upstream 업데이트 절차` 2~3단계(`cache/missing.tsv`의 `ko` 열을 채워 다시 실행).
- 기존 번역 수정: 평가 반영 목록(`apply.tsv`)이나 같은 형식의 TSV(열: `file`, `key`, `en`, `ko`)를 `uv run python -m tools.sync_locale <파일>`로 넣습니다. 같은 실행이 설명서 인용과 그 뒤 조사도 새 값에 맞춥니다(`tools/manual.py` `follow_values`). 출력에 "판단 필요"가 있으면 영어 설명서와 대조해 직접 고칩니다. 따옴표 없는 표 칸 같은 곳은 도구가 못 찾으므로(`builds.md` 2026-11-09 Disabled 항목: 4곳) `grep`으로 옛 값을 한 번 더 찾습니다.

## 2. 번역하면서 확인할 것

### 2-1. 공유 키: 사용처를 전부 센다

AceLocale은 키 하나에 값 하나입니다. 영어가 같으면 뜻이 다른 문맥도 같은 번역을 받습니다.

1. `../wowvision-ko/WowVision` 아래에서 `L["키"]`를 검색해 사용처를 전부 셉니다. 한두 곳만 보고 정하지 않습니다.
2. 모든 문맥에 맞는 말이 없으면 일부 문맥에 맞는 말을 고르지 말고 사용자 판단 목록에 올립니다. 원본에 키 분리 PR을 내는 것이 지금까지의 해법입니다(`decisions.tsv` 2026-11-09).

**`Disabled` 사례**: 사용처 16곳 중 14곳은 흐리게 표시된 버튼이고 2곳만 설정 끄기 상태였습니다. 설정 짝("사용함")에 맞춘 "사용 안 함"이 버튼에도 붙어 퀘스트 수락 버튼이 "사용 안 함"으로 들렸습니다. 최종 검수 기록에 이 의문이 적혀 있었는데도 평가자가 지적하지 않아 확정됐습니다. 그래서 **진행 기록에 남긴 의문은 지적이 없어도 사용자에게 넘깁니다**(`review-process.md` 원칙 9).

다른 파일에 이미 있는 키는 그 번역을 따릅니다. 파일 사이 값이 다르면 `test_same_key_same_translation`이 실패합니다.

### 2-2. 용어: 용어집, 게임 공식 용어, 문맥 순서

1. `docs/glossary.tsv`의 확정 용어를 씁니다. 지키지 않으면 `test_glossary_terms_consistent`가 실패합니다. 예외는 그 줄의 `except` 열에 `파일::키`로 적습니다.
2. 게임 공식 한국어는 `cache/game_terms.tsv`와 `cache/gs_koKR.csv`에서 찾습니다. **영어가 같아야 근거입니다**: `cache/gs_enUS.csv`의 같은 ID 영어가 원문 구절과 같은 말인지 확인합니다. "Roll Bonus"에 "Bonus Loot"의 번역 "추가 전리품"을 쓴 것이 반영됐다가 되돌려졌습니다.
3. 영어만 같고 문맥이 다른 공식 번역은 따르지 않습니다(`translation-guide.md` `## 용어` 2번).
4. 셋 다 없으면 지어내지 말고 보고 목록에 올립니다.

### 2-3. 조사: 들어갈 값의 받침을 모르는 곳

- **서식 지정자 바로 뒤**(`%s을`, `"%1$s"로`)에 받침 조사(을/를, 이/가, 은/는, 와/과, 으로/로, 이라고/라고)를 붙이지 않습니다. 들어갈 값마다 맞는 모양이 달라서 어느 쪽을 골라도 일부 값에서 틀립니다. `에게`, `에서`, `의`, `도`처럼 받침과 무관한 조사로 문장을 바꿉니다(`Whisper %s` → `%s에게 귓속말`). `test_no_batchim_josa_after_spec`이 검사합니다.
- **코드가 이어 붙이는 값**: 지정자가 없어도 코드가 `name .. L["키"]`처럼 앞에 값을 붙이면 같은 문제입니다. 2-1에서 사용처를 볼 때 조립 방식도 봅니다. 이 경우는 기계 검사가 없고 평가의 코드 맥락 관점(`tools/review/prompts/lens-context.md`)이 봅니다.
- **값을 바꿀 때 설명서 인용 뒤 조사**는 1단계의 `sync_locale`이 맞춥니다. 받침이 다른 값으로 바꿨으면("경보" → "알림") 결과에서 "알림를" 같은 것이 남지 않았는지 `uv run pytest -q`로 확인합니다.
- 피할 수 없으면 보고 목록에 올립니다(`translation-guide.md` `## 보고 목록`).

## 3. 평가

번역한 쪽이 좋다고 판단한 것으로는 통과가 아닙니다. `review-process.md` `## 단계`대로 묶음을 만들어 `full.js`(2~4단계), `regression.js`(5단계)를 돌리고 `tools.review.decisions`가 쓴 `apply.tsv`를 1단계 방식으로 반영합니다. 평가와 판정에서 **되돌린 번역은 `docs/glossary.tsv`에 넣습니다.** 기록만으로는 다시 제안되는 것을 막지 못했습니다.

## 4. payload, 설치 프로그램, 테스트

koKR이 바뀌면 설치 프로그램이 넣는 koKR도 낡습니다(`test_installer_loc.py`가 실패합니다).

1. `uv run python -m tools.installer_loc payload`
2. `docs/builds.md` `## 다시 만드는 법` 2~4단계(`build.ps1 -RunTests`, 설치 흐름이 바뀌었을 때만 `fullinstall`, 테스터 폴더 교체)
3. `uv run pytest -q` 전체 통과
4. payload를 풀어 새 값이 있고 옛 값이 없는지 확인합니다.
5. `builds.md` 현재 배포 표와 검증 이력을 업데이트합니다. 무엇을 다시 돌렸고 무엇을 왜 안 돌렸는지 적습니다.

## 5. 커밋

- vision-locale `main`과 wowwork에 각각 커밋합니다. 사용자가 정한 것이면 `docs/decisions.tsv`에 날짜와 출처(사용자)를 적습니다. Claude가 정한 것은 적지 않습니다.
- 번역으로 고칠 수 없는 것(코드에 박힌 영어, 설명서와 동작의 차이)은 `docs/upstream-report.md`에 모읍니다.
