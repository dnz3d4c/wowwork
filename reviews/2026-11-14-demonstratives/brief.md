# 지시어·메아리 점검 지침

대상: WowVision 한국어 설명서 `C:\project\games\wowvision-ko\WowVision\docs\src\user\ko\` (원문은 같은 경로의 `en\`, 코드는 `C:\project\games\wowvision-ko\WowVision\`, 화면 문구 한국어 값은 `C:\project\games\wowvision-ko\vision-locale\koKR\*.lua`). 파일은 **읽기만** 한다. 고치지 않는다.

독자는 스크린리더로 한 번 듣고 따라 하는 한국어 사용자다. 한국어 게임 설명서를 잘 쓰는 사람이라면 고칠 문장을 찾는다.

## 실제 사례 (사용자 지적)

원문: Enter on Template opens a list of the templates that exist for that kind of object. Press Enter on one to use it. Default means the standard wording.
번역(나쁨): 템플릿에서 Enter를 누르면 그 종류의 대상에 사용할 수 있는 템플릿 목록이 열립니다. 원하는 템플릿에서 Enter를 누르면 그 템플릿을 사용합니다. 기본은 표준 문구입니다.
문제: ① "그 종류의 대상"은 무엇의 종류인지 앞 문장으로 돌아가도 모른다(실제는 항목의 개체 종류). ② object를 "대상"으로 옮겨 게임 용어 "대상"(target)과 부딪힌다. ③ "템플릿에서 … 그 템플릿을" 같은 명사가 메아리친다.
고친 문장: 템플릿에서 Enter를 누르면 항목의 개체 종류(예: 생명력)에 맞는 템플릿 목록이 열립니다. 목록에서 원하는 템플릿을 골라 Enter를 누르면 적용됩니다. 기본을 고르면 표준 문구로 읽습니다.

## 찾을 것

1. 지시어(그, 이, 그것, 이것, 그곳, 해당)가 가리키는 명사를 한 번 들어서 알 수 없거나, 바로 앞 문장으로 돌아가야 알 수 있는 것. 영어 that/the/this/it를 기계적으로 옮긴 것이 대부분이다. 가리키는 명사로 되돌리거나 문장을 재구성한다.
2. 같은 문장이나 이웃 문장에서 같은 명사가 "X에서 … 그 X를"처럼 메아리치는 것. 줄이거나 문장을 합친다.
3. 영어 일반 명사(object, target, entry, item, thing, one)를 한국어로 기계적으로 옮겨 게임 용어나 화면 문구와 부딪히거나 뜻이 흐려진 것. 특히 "대상"이 target이 아닌 뜻으로 쓰인 곳.
4. "one", "it"을 "하나", "그것"으로 옮겨 무엇인지 안 들리는 것.

## 두는 것

- 접속 관용구: 그 밖의, 그 뒤에, 그 사이, 그 아래에, 그 다음, 그 때문에 등 한국어에서 자연스러운 것.
- 바로 앞 구절의 명사를 가리켜 한 번 들어도 분명한 것(예: "퀘스트를 고르면 그 퀘스트의 목표를 읽습니다"는 분명하면 둔다. 다만 "퀘스트를 고르면 목표를 읽습니다"처럼 지시어 없이도 분명하면 줄이는 쪽을 제안해도 된다. 확신이 없으면 내지 않는다).
- 취향 차이. 뜻이 분명하고 자연스러우면 지적하지 않는다.
- 화면 문구 인용("…" 안), 키 이름, 링크 대상, 표 구조는 그대로 둔다. 사실·조건·강도를 바꾸지 않는다.
- 용어집 `C:\project\games\wowwork\docs\glossary.tsv`와 결정 `C:\project\games\wowwork\docs\decisions.tsv`를 따른다.

## 확인

뜻이 애매하면 영어 원문 해당 문단을, 그래도 애매하면 코드를 본다. 고친 문장이 원문과 사실이 같은지 확인한다.

## 출력

결과 파일(경로는 프롬프트에 있다)에 UTF-8 TSV로 쓴다. 헤더: `file	line	quote	fix	type	reason`
- file: `ko\` 아래 상대 경로(예: `basics/menu-and-settings.md`)
- quote: 현재 문장에서 바꿀 부분을 글자 그대로(파일 안에서 한 곳만 가리킬 만큼 길게). 탭·줄바꿈 금지.
- fix: quote를 대신할 문장
- type: 1~4 중 번호
- reason: 한 줄. 원문 구절이나 코드 근거 포함.
최종 응답은 건수와 파일 경로만 짧게.
