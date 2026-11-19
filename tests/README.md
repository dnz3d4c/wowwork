# 테스트 안내

`uv run pytest -q`가 실행하는 검사의 목적, 실패했을 때 할 일, 테스트마다 생긴 이유를 적은 문서입니다. 테스트 코드의 설명(docstring)에는 사고 날짜와 세부 사례가 있습니다.

## 무엇을 지키는가

검사는 두 종류입니다.

- 도구 검사: `tools/`의 함수에 작은 가짜 입력을 넣어 결과를 확인합니다. 도구를 고쳤을 때 예전에 고친 버그가 다시 생기지 않았는지 봅니다.
- 실물 검사: 옆 폴더 `../wowvision-ko/`의 실제 번역 파일, 한국어 설명서, 설치 프로그램 소스, payload를 읽어 서로 어긋난 곳을 찾습니다. 실물 검사가 실패하면 대개 도구가 아니라 작업물(번역, 설명서, payload, 테스터 안내)을 고쳐야 합니다.

이 저장소의 결과물은 게임 안에서 화면 낭독기로 듣는 문장과 테스터에게 보내는 설치 프로그램입니다. 번역 키 하나가 빠지거나 낡은 payload를 배포해도 눈에 보이는 오류가 나지 않고 조용히 영어가 나오거나 옛 번역이 설치됩니다. 실물 검사는 이런 실수를 배포 전에 잡으려고 만들었습니다.

## 언제 실행하는가

- 커밋하기 전(`CLAUDE.md` `## 검증`)
- 번역을 고친 뒤, payload를 다시 만든 뒤, 원본 새 릴리스를 병합한 뒤
- 처음 내려받은 뒤 준비가 끝났는지 확인할 때(`README.md` `### 확인`)

작업을 시작하기 전에도 한 번 실행해 모두 통과하는지 봅니다. 실패한 상태에서 시작하면 새로 깨뜨린 것과 원래 깨져 있던 것을 가릴 수 없습니다.

## 실패하면

자주 실패하는 검사와 할 일입니다. 실패 메시지에 키 이름이나 파일 이름이 나옵니다.

| 실패한 검사 | 뜻 | 할 일 |
|-------------|----|-------|
| `test_installer_loc.py`의 `..._payload_matches_...` | 설치 프로그램에 넣을 payload가 현재 번역, 음성 팩, 로그인 툴과 다릅니다. 이대로 빌드하면 옛 파일이 배포됩니다 | `uv run python -m tools.installer_loc payload`로 다시 만들고 `docs/builds.md` `## 다시 만드는 법`대로 빌드합니다 |
| `test_kokr.py`의 `test_keys_match` | 원본에 새 키가 생겼거나 키가 사라졌습니다 | `docs/translation-guide.md` `## upstream 업데이트 절차`대로 `tools.sync_locale`을 실행합니다 |
| `test_kokr.py`의 `test_values_valid` | 번역이 비었거나 `%s`, `%d` 같은 서식 지정자가 원문과 다릅니다. 지정자가 다르면 게임에서 Lua 오류가 납니다 | 메시지에 나온 키의 번역을 고칩니다 |
| `test_kokr.py`의 `test_no_batchim_josa_after_spec` | `%s을`처럼 지정자 바로 뒤에 받침에 따라 달라지는 조사가 있습니다 | 문장 구조를 변경합니다(`docs/translation-guide.md` `## 서식 지정자`) |
| `test_kokr.py`의 `test_same_key_same_translation` | 같은 키가 두 파일에서 다르게 번역되었습니다. 게임은 나중 파일의 값만 사용하므로 한쪽 번역이 사라집니다 | 두 값을 하나로 맞춥니다 |
| `test_kokr.py`의 `test_glossary_terms_consistent` | 확정 용어(`docs/glossary.tsv`)를 지키지 않은 번역이 있습니다 | 용어집대로 고칩니다. 문맥상 예외면 `docs/glossary.tsv`의 `except` 열에 실패 메시지 맨 앞의 `파일::키`를 적습니다. 여러 개는 `;`로 구분합니다 |
| `test_manual.py`의 `test_translated_manual_passes_check` | 한국어 설명서의 제목 수준, 표, 목록, 링크, 용어, 문체가 원문이나 규칙과 다릅니다 | `uv run python -m tools.manual check <쪽 경로>`로 자세한 내용을 보고 고칩니다. 쪽 경로는 WowVision `docs/src/user/ko` 폴더 기준입니다(예: `basics/interface.md`) |
| `test_manual.py`의 `test_korean_summary_titles_match_page_headings` | 설명서 목차의 제목과 페이지 제목이 다릅니다 | `SUMMARY.md`나 페이지 제목을 맞춥니다 |
| `test_tester_guide.py` | 테스터 안내(`docs/tester-guide.md`)가 설치 프로그램 화면과 다릅니다. 새 옵션이 빠졌거나, 인용한 화면 문구가 변경되었습니다 | 안내를 설치 프로그램 화면에 맞춥니다 |
| `test_docs_style.py` | 저장소 문서에 "그 X", "해당 X", "~것입니다", 해요체가 있습니다 | 메시지에 나온 표현을 고칩니다(`CLAUDE.md` `## 검증`) |
| `test_voice_pack.py`의 `test_pack_files_follow_upstream_voice_pack` | 원본 음성 팩(`core/audio/AudioPack.lua`)에서 읽은 파일 목록이 108개가 아니거나 방향, 숫자 파일이 빠졌습니다 | 먼저 원본 `AudioPack.lua`가 실제로 변경되었는지 확인합니다. 변경되지 않았으면 목록을 읽는 `tools/voice_pack.py`의 고장입니다. 원본에 파일이 늘었으면 한국어 음성 팩을 다시 녹음하고 payload를 다시 만든 뒤(`docs/builds.md` `## 다시 만드는 법` 1단계), 이 테스트와 `test_installer_loc.py`의 `test_installer_voice_payload_matches_current_pack`에 적힌 108을 새 개수로 변경합니다 |
| `test_kokr.py`의 `test_lua_syntax` | 번역 파일에 Lua 문법 오류가 있습니다. 게임에서 이 파일의 번역이 모두 사라집니다 | 출력에 나온 파일과 줄에서 따옴표와 `\` 이스케이프를 확인합니다. 번역은 `tools.sync_locale`로 고칩니다 |
| `test_voice_registration.py` | 설치 프로그램이 `audio/voice.lua`에 덧붙이는 한국어 음성 등록 줄이 실행되지 않거나, 음성 세 개가 등록되지 않습니다 | 설치 프로그램 `KoreanVoice.cs`의 `RegisterLine`과, 원본 `audio/voice.lua`가 최근에 변경되었는지 확인합니다 |

표에 없는 검사가 실패하면, 특히 가짜 입력을 사용하는 도구 검사가 실패하면 최근에 고친 `tools/` 코드를 먼저 의심합니다. 원인을 찾지 못하면 출력 전체와 고친 내용을 저장해 개발을 맡은 사람에게 보냅니다.

여러 검사가 한꺼번에 실패하면 먼저 폴더 배치를 확인합니다(`README.md` `### 폴더 배치`). 옆 폴더의 저장소가 없거나 다른 브랜치에 있으면 실물 검사가 모두 실패합니다.

## 건너뛰는 검사

조건이 맞지 않으면 실패하지 않고 `skipped`로 건너뜁니다.

| 검사 | 건너뛰는 조건 |
|------|---------------|
| `test_kokr.py`의 `test_lua_syntax`, `test_voice_registration.py` | LuaJIT이 설치되지 않았을 때 |
| `test_logintool_ko.py` | `Sku-WoW-Addon-TBC` 복제본이 없을 때 |
| `test_manual.py`의 `test_translated_manual_passes_check` | 한국어 설명서가 없을 때 |

LuaJIT이 없으면 번역 파일의 Lua 문법을 검사하지 못합니다. 번역을 고칠 일이 있으면 LuaJIT을 설치합니다(`README.md` `### 작업에 따라 필요한 프로그램`).

## 파일별 설명

### 번역 파일

- `test_kokr.py`: koKR 번역 파일을 원본 enUS와 대조합니다. 파일과 머리말이 있는지, 키가 같은지, 빈 값과 서식 지정자, 지정자 뒤 조사, 파일 사이의 같은 키, `modules.xml` 목록, Lua 문법, 확정 용어를 봅니다. 번역 품질이 아니라 게임에서 깨지거나 조용히 영어로 돌아가는 실수를 잡습니다. `test_upstream_found`는 enUS를 못 찾아 나머지 검사가 0개로 통과하는 일을 막습니다.
- `test_glossary.py`: 용어집 검사 함수(`tools/glossary.py`)를 확인합니다. 두 번째 테스트는 실제 `docs/glossary.tsv`를 읽어 한 번 되돌린 번역 두 개("카메라 따라가기 방식", "추가 전리품 주사위")를 잡는지 봅니다. 용어집을 읽는 부분이 고장 나면 `test_glossary_terms_consistent`가 아무것도 잡지 못한 채 통과하므로, 이 테스트가 그런 고장을 알려 줍니다.
- `test_sync_locale.py`: 번역을 넣고 고치는 도구 `tools.sync_locale`을 확인합니다. 기존 번역 유지, enUS 줄 순서 따르기, 따옴표와 줄바꿈 처리, 원문 영어가 바뀐 키를 다시 번역하게 하기, 여러 파일 가운데 하나라도 쓰기에 실패하면 아무것도 쓰지 않기, enUS에 없는 키를 알리기를 봅니다.

### 한국어 설명서

- `test_manual.py`: 설명서 검사 도구 `tools.manual`을 확인하고, 실제 한국어 설명서 전체에 검사를 적용합니다. 검사 항목은 원문과 같은 구조(제목, 표, 목록, 링크, 인라인 코드), 링크 앵커, 해요체, 확정 용어, "바꾸다" 대신 "변경하다", 쓰지 않기로 정한 직역입니다. 설명서는 사람이 다듬은 문장이 많아서, 원문을 다시 번역하는 대신 바뀐 원문만 보여 주는 `source_diff`도 여기서 검사합니다.- `test_manual_follow.py`: 번역 값을 변경했을 때 설명서의 화면 문구 인용을 따라 고치는 기능을 확인합니다. 값이 같은 다른 키를 잘못 고치거나, 값만 변경하고 조사를 그대로 두어 "알림를"이 남거나, 두 번 실행하면 "안내 안내"가 되는 실제 사고를 하나씩 테스트로 남겼습니다.
- `test_docs_style.py`: 이 저장소의 한국어 문서(README, CLAUDE.md, 스킬, `docs/*.md`, 이 문서)에 지시어 번역투와 "~것입니다", 해요체가 없는지 봅니다. AI 검토로는 같은 표현이 계속 남아서 기계 검사로 막았습니다.

### 설치 프로그램과 테스터 안내

- `test_installer_loc.py`: 설치 프로그램 한국어 문구 표(`Loc.cs`)를 읽고 쓰는 기능과 payload를 확인합니다. 가장 중요한 검사는 payload를 확인하는 `..._payload_matches_...` 네 개입니다. 번역, 음성 팩, 로그인 툴 파일은 현재 작업물과 내용을 하나하나 비교하고, 다르면 payload를 다시 만들라고 실패합니다. 다만 빌드할 때마다 바이트가 달라지는 파일은 내용을 비교하지 못합니다. 로그인 툴 OCR 도우미(`SkuLoginSense.exe`)는 payload에 있는지만 보고, 센스 리더 프록시 DLL은 payload 안의 DLL과 서명 스크립트가 서로 맞는지만 봅니다. 그래서 도우미나 프록시 소스를 고쳤으면 이 검사가 통과해도 payload를 다시 만들어야 합니다. payload를 같은 입력으로 두 번 만들면 바이트까지 같아야 한다는 검사도 있어서, 바뀌지 않은 payload가 git에 변경으로 잡히지 않습니다.
- `test_tester_guide.py`: 테스터 안내가 설치 프로그램 구성 요소 페이지의 모든 옵션을 소개하는지, 안내가 인용한 화면 문구가 한국어 화면에 실제로 있는지, NVDA 브리지 기본값을 맞게 적었는지 봅니다. 2026-11-06에 안내가 NVDA 브리지 설치 방법을 빠뜨린 일이 계기입니다. 옵션 목록은 설치 프로그램 소스에서 읽으므로 원본에 옵션이 생기면 이 검사가 실패합니다(`CLAUDE.md` `## 원본 기능 유지`).
- `test_install.py`: 개발용 도구 `tools.install`(게임 AddOns 폴더에 koKR을 직접 넣기)을 확인합니다. 원본 `modules.xml`에 koKR 줄을 한 번만 넣는지, 옛 koKR 파일을 지우는지 봅니다. 테스터용 설치는 설치 프로그램이 하고, 이 도구는 번역을 게임에서 바로 확인할 때 사용합니다.

### 한국어 음성 팩

- `test_voice_pack.py`: 나침반 방향과 숫자를 한국어로 읽는 음성 팩 도구(`tools/voice_pack.py`)를 확인합니다. 녹음할 파일 목록을 원본 음성 팩 소스에서 읽는지, 숫자를 한글로 읽는지, 잘린 녹음과 너무 큰 녹음을 걸러 내는지 봅니다.
- `test_voice_registration.py`: 설치 프로그램이 원본 `audio/voice.lua`에 덧붙이는 한국어 음성 등록 줄을 LuaJIT으로 실행해, 원본 음성 두 개와 한국어 음성이 함께 등록되는지 봅니다. 등록 줄의 Lua 오류는 게임을 켜야 드러나므로, 게임 없이 미리 잡으려고 만들었습니다.

### 로그인 툴

- `test_logintool_ko.py`: 로그인 툴 한국어판이 캐릭터 선택 화면에서 레벨 줄을 알아보는 규칙(`flows.ahk`의 정규식)을 실제 OCR 결과로 검사합니다. AutoHotkey에는 테스트 도구가 없어서 파이썬에서 정규식을 꺼내 검사합니다. OCR이 "레벨"을 "해일"로 잘못 읽어도 알아보고, 이름에 "레벨"이 포함된 캐릭터는 레벨 줄로 오인하지 않아야 합니다.
- `test_logintool_loc.py`: 로그인 툴 번역 파일(`koKR.txt`)과 `forever.ahk` 안의 한국어 낱말을 읽고 고치는 기능을 확인합니다. 화면 판별에 사용하는 문구는 게임 화면 글자와 같아야 하므로 번역 대상에서 빼는지도 봅니다.
### 저장소 관리

- `test_pr_cleanup.py`: 원본에 병합된 PR 브랜치를 지우는 도구 `tools.pr_cleanup`의 판단을 확인합니다. 병합된 브랜치만 지우고, 병합 없이 닫혔거나 병합 뒤 새 커밋이 있으면 남기고 알리며, `main` 같은 보호 브랜치와 `origin` 밖의 원격은 건드리지 않아야 합니다. 브랜치 삭제는 되돌리기 어려워서 판단 규칙을 테스트로 고정했습니다.

## 정리 기록

2026-11-19에 인계를 앞두고 테스트를 정리하면서 아래 테스트를 지웠습니다.

- `test_logintool_bench.py`와 측정 도구 `tools/logintool_bench/`: 2026-11-07에 로그인 툴 OCR 인식률을 한 번 잰 도구입니다. 측정 결과는 `flows.ahk`의 레벨 줄 판정 규칙과 `test_logintool_ko.py`의 OCR 문자열로 남아 있고, 다시 재려면 게임 안 애드온과 화면 캡처 준비가 필요해서 현재 절차에는 쓰이지 않습니다. 도구를 다시 쓰려면 `git log --diff-filter=D -- tools/logintool_bench`로 삭제 커밋을 찾아 직전 커밋에서 꺼냅니다.
- `test_manual.py`의 `test_term_sheet_finds_ui_strings_with_korean_values`, `test_batch_hides_english_from_style_lens`, `test_changed_ko_lines_maps_english_hunks_to_korean_lines`와 `tools.manual`의 `batch`, `terms`, `list` 명령: AI 검수 파이프라인(`docs/archive/review-pipeline/`)에만 쓰이던 기능이라 코드와 함께 지웠습니다.

- `test_tester_guide.py`의 `test_guide_quotes_match_installer_text`: 안내의 인용 문구가 설치 프로그램 네 언어 표 가운데 하나에 있는지 보는 검사였습니다. 같은 파일의 `test_guide_quotes_only_korean_screen_text`가 더 좁은 한국어 표만 허용하므로, 지운 검사가 잡는 문제는 남은 검사도 모두 잡습니다. 지운 검사의 사고 기록은 남은 검사의 설명으로 옮겼습니다.
- `test_voice_pack.py`의 `test_defaults_rate_and_volume`: 녹음 속도 5와 볼륨 60이라는 상수 값을 테스트에 한 번 더 적고, 녹음 스크립트에 볼륨 지정 줄이 있는지 글자로 확인하는 검사였습니다. 상수 값은 누가 일부러 변경할 때만 달라지고, 그때 테스트는 같은 값을 한 번 더 고치게 할 뿐입니다. 값을 정한 이유는 `tools/voice_pack.py`의 주석과 `docs/builds.md` 배포 기록(2026-11-08 음성 팩 다시 녹음)에 있습니다. 볼륨 지정 줄이 빠지면 SAPI 기본 볼륨 100으로 녹음되어 소리가 잘리고(2026-11-08 실측), 음성 팩을 만드는 `tools.voice_pack build`가 피크 검사(`too_loud`)에서 실패합니다. 2026-11-19 GPT 교차 검토는 볼륨 검사를 남기자고 했지만, 같은 실수를 빌드가 잡으므로 지운 상태를 유지했습니다.
