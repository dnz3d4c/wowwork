---
name: kokr-translation
description: WowVision koKR 번역(vision-locale/koKR/*.lua)을 새로 쓰거나 고치는 순서와, 단계마다 따를 기준 문서를 안내한다. 원본을 병합한 뒤 새 문자열을 번역할 때, 사용자 지적으로 기존 번역을 고칠 때, 공유 키의 문맥을 확인할 때, 번역을 고친 뒤 설치 프로그램 payload를 다시 만들 때 사용한다. "koKR", "번역", "번역 수정", "새 키", "sync_locale", "용어집", "조사", "payload"가 나오는 작업에 해당한다.
---

# koKR 번역

이 스킬에는 작업 순서와 확인 방법만 둔다. 번역 규칙은 [`CLAUDE.md` `## 번역을 고칠 때`](../../../CLAUDE.md#번역을-고칠-때)와 아래 문서에 있다.

| 무엇 | 어디 |
|------|------|
| 번역 규칙(파일 형식, 서식 지정자, 용어, 문체, 낱말 표) | [`docs/translation-guide.md`](../../../docs/translation-guide.md) |
| 사용자 결정 | [`docs/decisions.tsv`](../../../docs/decisions.tsv) |
| 확정 용어, 되돌린 번역 | [`docs/glossary.tsv`](../../../docs/glossary.tsv) |
| payload와 설치 프로그램 다시 만들기 | [`docs/builds.md` `## 다시 만드는 법`](../../../docs/builds.md#다시-만드는-법) |

모든 명령은 wowwork 폴더에서 실행한다. 번역 파일은 `../wowvision-ko/vision-locale/koKR/`에 있고, vision-locale 저장소의 `main` 브랜치에 커밋한다.

## 0. 시작 전에

1. `uv run pytest -q`가 모두 통과하는지 확인한다. 실패한 상태에서 시작하면 새로 깨뜨린 것과 원래 깨져 있던 것을 가릴 수 없다.
2. 고칠 키가 [`docs/decisions.tsv`](../../../docs/decisions.tsv)에 결정으로 있는지 찾는다. 있으면 기록된 결정을 따른다.
3. 여러 키에 걸리는 방침이면 [`CLAUDE.md` `## 번역을 고칠 때`](../../../CLAUDE.md#번역을-고칠-때)대로 작업 전에 사용자 결정을 받는다.

## 1. koKR 고치기

- 새 키: [`docs/translation-guide.md` `## upstream 업데이트 절차`](../../../docs/translation-guide.md#upstream-업데이트-절차) 4~5단계(`cache/missing.tsv`의 `ko` 열을 채워 다시 실행).
- 기존 번역 수정: 열이 `file`, `key`, `en`, `ko`인 TSV를 만들어 `uv run python -m tools.sync_locale <파일>`로 넣는다. 같은 실행이 설명서의 인용과 그 뒤 조사도 새 값에 맞춘다([`tools/manual.py`](../../../tools/manual.py) `follow_values`).
- 출력에 "판단 필요"가 있으면 영어 설명서와 대조해 직접 고친다.
- 따옴표 없는 표 칸처럼 도구가 찾지 못하는 곳이 있으므로, 옛 값을 `grep`으로 한 번 더 찾는다.

## 2. 번역하면서 확인할 것

### 2-1. 공유 키: 사용처를 전부 센다

1. `../wowvision-ko/WowVision` 아래에서 `L["키"]`를 검색해 사용처를 전부 센다. 한두 곳만 보고 정하지 않는다.
2. 사용처를 센 결과로 [`docs/translation-guide.md` `## 용어`](../../../docs/translation-guide.md#용어) 3번에 따라 번역을 정한다. 모든 문맥에 맞는 말이 없으면 원본에 키를 나누는 PR을 제안한다.
3. 다른 파일에 같은 키가 있으면 기존 번역을 따른다([`docs/translation-guide.md` `## 파일 형식`](../../../docs/translation-guide.md#파일-형식)). 파일 사이 값이 다르면 `test_same_key_same_translation`이 실패한다.

### 2-2. 용어: 용어집, 게임 공식 용어, 문맥 순서

1. 용어를 고르는 순서는 [`docs/translation-guide.md` `## 용어`](../../../docs/translation-guide.md#용어)를 따른다.
2. 확정 용어는 [`docs/glossary.tsv`](../../../docs/glossary.tsv)에 있다. 지키지 않으면 `test_glossary_terms_consistent`가 실패한다. 예외는 용어집 줄의 `except` 열에 `파일::키`로 적는다.
3. 게임 공식 한국어는 `cache/game_terms.tsv`와 `cache/gs_koKR.csv`에서 찾는다. 근거로 삼는 조건은 [`CLAUDE.md` `## 번역을 고칠 때`](../../../CLAUDE.md#번역을-고칠-때)에 있다.
4. 근거가 없으면 지어내지 말고 보고 목록에 올린다.

### 2-3. 조사: 들어갈 값의 받침을 모르는 곳

- 서식 지정자 바로 뒤의 조사 규칙은 [`docs/translation-guide.md` `## 서식 지정자`](../../../docs/translation-guide.md#서식-지정자)에 있다. `test_no_batchim_josa_after_spec`이 검사한다.
- 코드가 값을 이어 붙이는 키(`name .. L["키"]`)도 같은 문제다. 2-1에서 사용처를 볼 때 조립 방식도 본다. 기계 검사가 없으므로 검수할 때 코드 맥락을 함께 본다.
- 1단계의 `sync_locale`로 값을 변경하면 설명서 인용 뒤의 조사도 맞춰진다. 받침이 다른 값으로 변경했으면("경보" → "알림") "알림를" 같은 표현이 남지 않았는지 `uv run pytest -q`로 확인한다.
- 피할 수 없으면 보고 목록에 올린다([`docs/translation-guide.md` `## 보고 목록`](../../../docs/translation-guide.md#보고-목록)).

## 3. 검수

검수 방식은 관리자가 정한다. 검수 결과는 [`CLAUDE.md` `## 번역을 고칠 때`](../../../CLAUDE.md#번역을-고칠-때)에 따라 반영한다(되돌린 번역의 용어집 등록, 남은 의문 넘기기, 지적의 유형 처리).

## 4. payload, 설치 프로그램, 테스트

koKR을 변경하면 설치 프로그램에 든 koKR과 달라져 `test_installer_loc.py`가 실패한다.

1. `uv run python -m tools.installer_loc payload`
2. [`docs/builds.md` `## 다시 만드는 법`](../../../docs/builds.md#다시-만드는-법) 2~4단계(설치 프로그램 빌드와 자체 검사, 실제 흐름 검사, 테스터 폴더 교체)
3. `uv run pytest -q` 전체 통과
4. payload를 풀어 새 값이 있고 옛 값이 없는지 확인한다.
5. [`docs/builds.md`](../../../docs/builds.md)의 현재 배포 표와 검증 이력을 업데이트한다. 실행한 검사, 실행하지 않은 검사와 이유를 적는다.

## 5. 커밋

- vision-locale `main`과 wowwork에 각각 커밋한다. payload를 다시 만들었으면 wowvision-installer `ko`에도 커밋한다. 저장소별 목록은 [`docs/builds.md` `## 다시 만드는 법`](../../../docs/builds.md#다시-만드는-법) 5단계에 있다.
- 사용자가 정한 것은 [`docs/decisions.tsv`](../../../docs/decisions.tsv)에 날짜와 출처(사용자)를 적는다. 사용자 결정이 아닌 것은 적지 않는다.
