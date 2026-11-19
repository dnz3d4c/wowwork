---
name: kokr-translation
description: WowVision koKR 번역(vision-locale/koKR/*.lua)을 새로 쓰거나 고치는 순서와, 단계마다 따를 기준 문서를 안내한다. 원본을 병합한 뒤 새 문자열을 번역할 때, 사용자 지적으로 기존 번역을 고칠 때, 공유 키의 문맥을 확인할 때, 번역을 고친 뒤 설치 프로그램 payload를 다시 만들 때 사용한다. "koKR", "번역", "번역 수정", "새 키", "sync_locale", "용어집", "조사", "payload"가 나오는 작업에 해당한다.
---

# koKR 번역

이 스킬은 작업 순서와 확인 방법을 담는다. 규칙 본문은 `CLAUDE.md` `## 번역을 고칠 때`와 아래 문서에 있고, 이 스킬과 다르면 그쪽을 따른다.

| 무엇 | 어디 |
|------|------|
| 번역 규칙(파일 형식, 서식 지정자, 용어, 문체, 낱말 표) | `docs/translation-guide.md` |
| 사용자 결정 | `docs/decisions.tsv` |
| 확정 용어, 되돌린 번역 | `docs/glossary.tsv` |
| payload와 설치 프로그램 다시 만들기 | `docs/builds.md` `## 다시 만드는 법` |

모든 명령은 wowwork 폴더에서 실행한다. 번역 파일은 `../wowvision-ko/vision-locale/koKR/`에 있고, 그 저장소의 `main` 브랜치에 커밋한다.

## 0. 시작 전에

1. `uv run pytest -q`가 모두 통과하는지 확인한다. 실패한 상태에서 시작하면 새로 깨뜨린 것과 원래 깨져 있던 것을 가릴 수 없다.
2. 고칠 키가 `docs/decisions.tsv`에 결정으로 있는지 찾는다. 있으면 그 결정을 따른다.
3. 여러 키에 걸리는 방침(문체, 여러 곳에 쓰인 용어)이면 작업 전에 사용자 결정을 받는다.

## 1. koKR은 `tools.sync_locale`로만 고친다

- 새 키: `docs/translation-guide.md` `## upstream 업데이트 절차` 4~5단계(`cache/missing.tsv`의 `ko` 열을 채워 다시 실행).
- 기존 번역 수정: 열이 `file`, `key`, `en`, `ko`인 TSV를 만들어 `uv run python -m tools.sync_locale <파일>`로 넣는다. 같은 실행이 설명서의 인용과 그 뒤 조사도 새 값에 맞춘다(`tools/manual.py` `follow_values`).
- 출력에 "판단 필요"가 있으면 영어 설명서와 대조해 직접 고친다.
- 따옴표 없는 표 칸처럼 도구가 찾지 못하는 곳이 있으므로, 옛 값을 `grep`으로 한 번 더 찾는다.

## 2. 번역하면서 확인할 것

### 2-1. 공유 키: 사용처를 전부 센다

AceLocale은 키 하나에 값 하나다. 영어가 같으면 뜻이 다른 문맥도 같은 번역을 받는다.

1. `../wowvision-ko/WowVision` 아래에서 `L["키"]`를 검색해 사용처를 전부 센다. 한두 곳만 보고 정하지 않는다.
2. 모든 문맥에 맞는 말이 없으면 일부 문맥에만 맞는 말을 고르지 않는다. 사용자 판단 목록에 올리고, 해법으로 원본에 키를 나누는 PR을 제안한다.

예: `Disabled`는 대부분 흐리게 표시된 버튼에 쓰이고 일부만 설정 끄기 상태에 쓰였다. 설정에 맞춘 "사용 안 함"을 쓰면 퀘스트 수락 버튼이 "사용 안 함"으로 들렸다.

다른 파일에 이미 있는 키는 그 번역을 따른다. 파일 사이 값이 다르면 `test_same_key_same_translation`이 실패한다.

### 2-2. 용어: 용어집, 게임 공식 용어, 문맥 순서

1. `docs/glossary.tsv`의 확정 용어를 쓴다. 지키지 않으면 `test_glossary_terms_consistent`가 실패한다. 예외는 그 줄의 `except` 열에 `파일::키`로 적는다.
2. 게임 공식 한국어는 `cache/game_terms.tsv`와 `cache/gs_koKR.csv`에서 찾는다. 근거로 쓰는 조건은 `CLAUDE.md` `## 번역을 고칠 때`에 있다.
3. 영어만 같고 문맥이 다른 공식 번역은 따르지 않는다(`docs/translation-guide.md` `## 용어` 2번).
4. 셋 다 없으면 지어내지 말고 보고 목록에 올린다.

### 2-3. 조사: 들어갈 값의 받침을 모르는 곳

- 서식 지정자 바로 뒤의 조사 규칙은 `docs/translation-guide.md` `## 서식 지정자`에 있다. `test_no_batchim_josa_after_spec`이 검사한다.
- 코드가 값을 이어 붙이는 키(`name .. L["키"]`)도 같은 문제다. 2-1에서 사용처를 볼 때 조립 방식도 본다. 기계 검사가 없으므로 검수할 때 코드 맥락을 함께 본다.
- 값을 바꾸면 1단계의 `sync_locale`이 설명서 인용 뒤 조사를 맞춘다. 받침이 다른 값으로 바꿨으면("경보" → "알림") "알림를" 같은 것이 남지 않았는지 `uv run pytest -q`로 확인한다.
- 피할 수 없으면 보고 목록에 올린다(`docs/translation-guide.md` `## 보고 목록`).

## 3. 검수

번역한 쪽이 좋다고 판단한 것으로는 끝나지 않는다. 번역한 사람과 다른 검토자가 번역을 검수한다. 검수 방식은 관리자가 정한다. 1.0 때 쓴 방식(Claude와 GPT의 교차 판정)은 `docs/review-process.md`에 기록으로 있다. 검수 결과를 반영할 때는 `CLAUDE.md` `## 번역을 고칠 때`를 따른다(되돌린 번역의 용어집 등록, 남은 의문 넘기기, 지적의 유형 처리).

## 4. payload, 설치 프로그램, 테스트

koKR이 바뀌면 설치 프로그램에 넣는 koKR도 낡는다(`test_installer_loc.py`가 실패한다).

1. `uv run python -m tools.installer_loc payload`
2. `docs/builds.md` `## 다시 만드는 법` 2~4단계(설치 프로그램 빌드와 자체 검사, 설치 흐름이 바뀌었을 때만 `fullinstall`, 테스터 폴더 교체)
3. `uv run pytest -q` 전체 통과
4. payload를 풀어 새 값이 있고 옛 값이 없는지 확인한다.
5. `docs/builds.md`의 현재 배포 표와 검증 이력을 업데이트한다. 무엇을 다시 돌렸고 무엇을 왜 돌리지 않았는지 적는다.

## 5. 커밋

- vision-locale `main`과 wowwork에 각각 커밋한다.
- 사용자가 정한 것은 `docs/decisions.tsv`에 날짜와 출처(사용자)를 적는다. Claude가 정한 것은 적지 않는다.
