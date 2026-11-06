## claude-tester-0 [major/context]
- quote: Windows 표시 언어가 한국어가 아니면 화면이 영어로 나옵니다. 이때는 구성 요소 페이지의 "이 설치 프로그램의 언어"에서 한국어를 고릅니다.
- suggestion: Windows 표시 언어가 한국어가 아니면 설치 프로그램이 영어로 나옵니다. 언어는 "직접 고르기"의 마지막 구성 요소 페이지에서만 바꿀 수 있으므로, 그 전까지는 영어 이름으로 고릅니다. 2단계의 "현재 버전으로 계속"은 "Continue with the current version", 3단계의 "지금 설치"는 "Install now", "지금 업데이트"는 "Update now", "WowVision 새로 설치, 또는 다른 게임 버전에 설치"는 "Install WowVision fresh, or for further game versions"입니다.
- problem: 1단계에서 언어를 구성 요소 페이지에서 바꾸라고 하지만, 그 페이지는 2단계(자체 업데이트 질문)와 3단계(첫 화면)를 지나 "직접 고르기" 경로로 들어가야만 나온다. 영어 Windows 테스터는 2·3단계에서 영어 버튼을 듣는데 안내는 한국어 이름만 인용하므로 "현재 버전으로 계속"을 찾지 못하고, "지금 설치"로 가면 언어를 바꿀 기회가 아예 없다. 1단계 지시를 지금 순서대로 따를 수 없다.
- evidence: Program.cs:16 Loc.Init()이 OS UI 언어로 정함, Loc.cs:29-34 ko가 아니면 En. Program.cs:52-66 자체 업데이트 질문, 91-110 첫 화면, 195-198 구성 요소 페이지는 RunWizard 마지막 단계. ComponentsForm.cs:169-172 Loc.Set만 하고 저장하지 않음. 영어 문구 Loc.cs:82-85, 107.

## claude-tester-1 [major/accuracy]
- quote: 찾아낸 게임 버전에 권장 구성으로 바로 설치합니다.
- suggestion: "지금 설치"는 찾아낸 게임 버전에 권장 구성으로 바로 설치하고, "지금 업데이트"는 지난번에 고른 구성 그대로 업데이트합니다.
- problem: "지금 업데이트"는 권장 구성이 아니라 지난번 선택(안정판/베타, 추가 애드온)을 유지한다. 이전에 베타나 다른 애드온을 고른 테스터는 업데이트하면 권장 구성으로 되돌아간다고 오해한다. 화면 설명도 "현재 설정을 유지합니다"라서 들은 안내와 화면이 어긋난다.
- evidence: Loc.cs:830 update.explainUpdate "현재 설정을 유지합니다", 838 update.installAcc만 "권장 구성 사용". installer.md:29-30 "Update now: ... keeps the choices you made last time". ComponentsForm.cs:244, 260 선택을 저장하고 one-click이 재사용.

## claude-tester-2 [major/context]
- quote: 바꿀 것이 없으면 그대로 "설치"를 누릅니다.
- suggestion: 바꿀 것이 없으면 그대로 "설치"를 누릅니다. WowVision이 NVDA로 말하게 하려면 "WoW에서 NVDA를 음성으로 사용"을 체크한 뒤 "설치"를 누릅니다.
- problem: 3단계에서 NVDA로 듣고 싶으면 "직접 고르기"를 따르라고 보냈는데, 이 절에는 그 목적에 필요한 행동(NVDA 항목 체크)이 지시로 나오지 않고 항목 목록 안 설명으로만 있다. 바로 앞 문장은 "그대로 설치"를 권하므로 목록을 다 듣기 전에 설치를 눌러 브리지 없이 끝나는 테스터가 생긴다.
- evidence: InstallRunner.cs:21 InstallSapi2Sr = false 기본값. 안내 3단계 "WowVision이 NVDA로 말하게 하려면 이쪽을 고르고 아래 "직접 고르기" 절을 따릅니다". installer.md:46.

## claude-tester-3 [major/context]
- quote: WowVision 업데이트도 이 설치 프로그램으로 합니다.
- suggestion: WowVision 업데이트도 받은 WowVisionInstaller.exe를 다시 실행해서 합니다. 설치 때 만들어진 바탕 화면의 "WowVision Updater" 바로 가기는 쓰지 않습니다.
- problem: 구성 요소 목록에서 "WowVision Updater의 바탕 화면 바로 가기 만들기"가 기본 체크라고 안내했고, 원본 설명서는 그 바로 가기로 업데이트하라고 한다. 테스터는 "이 설치 프로그램"이 그 바로 가기를 포함하는지 알 수 없다. 바로 가기가 가리키는 사본은 이미 더 새 버전(예: 전에 쓴 원본 설치 프로그램)이 있으면 한국어판으로 바뀌지 않으므로, 바로 가기로 업데이트하면 한국어가 빠질 수 있다.
- evidence: Shortcut.cs:37-58 InstallPersistentCopy는 더 새 사본이 있으면 덮어쓰지 않음, 109 바로 가기는 그 사본을 가리킴. installer.md:45, 69 "Start the WowVision Updater from its shortcut". 안내 "## 업데이트" 절.

## claude-tester-4 [minor/context]
- quote: 게임이 켜져 있었다면 다시 시작합니다.
- suggestion: (이 문장을 뺍니다)
- problem: "시작하기 전에"에서 World of Warcraft를 완전히 종료하라고 했으므로 안내대로 한 테스터에게는 게임이 켜져 있을 수 없다. 들으면 앞 지시를 놓쳤나 되묻게 된다. 바로 뒤 문장(/reload로는 부족)만으로 충분하다.
- evidence: 안내 "## 시작하기 전에" "World of Warcraft를 완전히 종료합니다." installation.md:26.

## gpt-tester-0 [critical/accuracy]
- quote: 3. 구성 요소: 기본값이 권장 구성입니다. 바꿀 것이 없으면 그대로 "설치"를 누릅니다.
- suggestion: 3. 구성 요소: WowVision이 NVDA로 말하게 하려면 "WoW에서 NVDA를 음성으로 사용"을 체크합니다. 그 밖에 바꿀 것이 없으면 "설치"를 누릅니다.
- problem: 앞에서는 NVDA 음성 사용을 위해 직접 설치를 고르라고 했지만, 실제 선택 단계에서는 기본값 그대로 설치하라고 합니다. 이 옵션은 기본으로 꺼져 있으므로 안내대로 진행하면 NVDA 음성 브리지가 설치되지 않습니다.
- evidence: wowvision-ko/wowvision-installer/WowVisionInstaller/InstallRunner.cs:21에서 InstallSapi2Sr의 기본값은 false입니다. 원본 설명서 installer.md:46도 NVDA 음성 옵션이 기본 체크 해제라고 밝힙니다.

## gpt-tester-1 [critical/context]
- quote: 4. 설치가 끝나면 "완료" 또는 "문제가 있었지만 완료"가 나옵니다. "설치 프로그램 닫기"를 누릅니다.
- suggestion: 4. "완료"가 나오면 "설치 프로그램 닫기"를 누릅니다. "문제가 있었지만 완료"가 나오면 결과 요약과 "진행 기록 보기"에서 실패한 내용을 확인한 뒤, 아래 "문제가 생기면" 절에 따라 로그를 보냅니다.
- problem: 실패가 있는 완료 화면에서도 무조건 설치 프로그램을 닫도록 지시합니다. 설치하지 못한 게임 버전이 있어도 다음 단계에서 게임을 실행하게 되어 WowVision이 동작하지 않을 수 있습니다.
- evidence: Loc.cs:874는 실패한 실행의 제목을 "문제가 있었지만 완료"로 표시하고, Loc.cs:880-882는 세부 단계를 확인하는 "진행 기록 보기"를 제공합니다. 원본 설명서 installer.md:63도 이 화면에 게임 버전별 실패 이유가 나온다고 설명합니다.

## gpt-tester-2 [major/accuracy]
- quote: 1. `WowVisionInstaller.exe`를 실행합니다. Windows 표시 언어가 한국어가 아니면 화면이 영어로 나옵니다. 이때는 구성 요소 페이지의 "이 설치 프로그램의 언어"에서 한국어를 고릅니다.
- suggestion: 1. WowVisionInstaller.exe를 실행합니다. Windows 표시 언어가 한국어가 아니면 영어, 독일어 또는 프랑스어로 나올 수 있습니다. 구성 요소 페이지의 "이 설치 프로그램의 언어"에서 한국어를 고릅니다.
- problem: 한국어가 아닌 Windows에서 항상 영어가 나온다는 설명은 틀렸습니다. 독일어 또는 프랑스어 화면을 마주친 테스터는 예상과 달라 설치 프로그램이나 안내가 잘못됐다고 오해할 수 있습니다.
- evidence: Loc.cs:25-37은 Windows UI 언어가 de이면 독일어, fr이면 프랑스어, ko이면 한국어, 나머지는 영어를 선택합니다.

## gpt-tester-3 [minor/style]
- quote: 테스터용 안내입니다. `WowVisionInstaller.exe`를 실행해서 설치하고, 업데이트도 같은 파일로 합니다.
- suggestion: 테스터용 안내입니다. WowVisionInstaller.exe를 실행해서 설치하고, 업데이트도 같은 파일로 합니다.
- problem: 텍스트 파일에서는 백틱이 서식으로 처리되지 않습니다. NVDA의 기호 읽기 설정에 따라 파일명 앞뒤의 기호까지 들려 첫 실행 파일 이름을 알아듣는 데 방해가 됩니다.
- evidence: 제시된 문서 규칙은 마크다운 기호가 텍스트 파일에서 그대로 읽히므로 본문 지시에 넣지 말라고 명시합니다.

## claude-facts-0 [major/accuracy]
- quote: Windows 표시 언어가 한국어가 아니면 화면이 영어로 나옵니다. 이때는 구성 요소 페이지의 "이 설치 프로그램의 언어"에서 한국어를 고릅니다.
- suggestion: Windows 표시 언어가 한국어이면 처음부터 한국어로 나옵니다. 아니면 Windows 언어(영어, 독일어, 프랑스어 중 하나)로 나오고, 한국어로 바꾸는 곳은 "WowVision 새로 설치, 또는 다른 게임 버전에 설치"를 고른 뒤 나오는 구성 요소 페이지의 "이 설치 프로그램의 언어"뿐입니다. 그 전 화면은 Windows 언어로 나오므로, 영어 화면이라면 2단계의 "현재 버전으로 계속"은 "Continue with the current version", 3단계의 버튼은 "Install now", "Update now", "Install WowVision fresh, or for further game versions"입니다.
- problem: 1단계 지시로 언어를 바꾸라고 했지만 언어 선택은 구성 요소 페이지에만 있고, 그 페이지는 2단계(자체 업데이트 확인)와 3단계(첫 화면)를 지나 직접 고르기 경로를 택해야만 나온다. "지금 설치/지금 업데이트" 경로로는 끝내 나오지 않는다. 한국어가 아닌 Windows의 테스터는 1단계를 그 자리에서 할 수 없고, 2·3단계에서 안내가 인용한 한국어 버튼 이름을 영어 화면에서 찾지 못한다. 특히 2단계에서 고를 버튼을 못 찾으면 권장 버튼인 설치 프로그램 업데이트를 눌러 한국어를 잃을 수 있다. 또 독일어·프랑스어 Windows에서는 영어가 아니라 그 언어로 나온다.
- evidence: Program.cs:16 Loc.Init(), 52-66 자체 업데이트 확인이 첫 화면보다 먼저, 93-106 첫 화면 뒤 RunWizard, 195-204 ComponentsForm은 마법사 3단계에서만; Loc.cs:29-35 de/fr/ko 자동 감지; ComponentsForm.cs:169-172 언어 변경은 이 폼에서만; Loc.cs En 표 82,83,85,107 영어 버튼 이름; installer.md:21 "The installer speaks the language of Windows (English, German 

## claude-facts-1 [major/accuracy]
- quote: 게임이 켜져 있었다면 다시 시작합니다. 새로 설치한 애드온은 게임을 시작할 때만 인식되므로 /reload로는 부족합니다.
- suggestion: 게임이 켜져 있었다면 설치 프로그램 마지막 화면의 안내를 따릅니다. "Battle.net에서 World of Warcraft를 시작(또는 다시 시작)하십시오"가 나오면 게임을 다시 시작하고, "게임에서 /reload를 입력하십시오"가 나오면 /reload로 됩니다.
- problem: 안내는 게임이 켜져 있으면 언제나 다시 시작하라고 하지만, 이미 설치된 WowVision의 업데이트는 게임이 켜진 채로 복사되고 설치 프로그램 마지막 화면은 /reload를 입력하라고 말한다. 테스터는 마지막 화면에서 "/reload"를 듣고, 안내에서는 "/reload로는 부족"을 들어 어느 쪽을 따를지 헷갈린다. 다시 시작이 필요한 경우(새 애드온, 게임을 닫아야 하는 단계, 인터페이스 버전 맞춤)는 설치 프로그램이 직접 Battle.net 문구로 알려 준다.
- evidence: InstallRunner.cs:556-561 restart 여부에 따라 summary.battlenet 또는 summary.reload; Loc.cs:985-986 Ko summary.reload, summary.battlenet 문구; installer.md:59 "An update of a WowVision that is already installed is copied even while the game runs; type /reload in the game afterward.", installer.md:65 "or type 

## claude-facts-2 [minor/accuracy]
- quote: "설치 프로그램을 지금 업데이트"를 고르면
- suggestion: "설치 프로그램을 지금 업데이트 (권장)"을 고르면
- problem: 실제 버튼 이름 끝에 "(권장)"이 붙어 있고 NVDA도 그렇게 읽는다. 안내가 피하라는 버튼이 화면에서는 권장으로 들리므로, 같은 이름으로 인용해야 테스터가 맞는 버튼이라는 것을 알아듣는다.
- evidence: Loc.cs:856 Ko selfupdate.updateBtn = "설치 프로그램을 지금 업데이트(&U) (권장)", 857 selfupdate.updateAcc "설치 프로그램을 지금 업데이트, 권장 — ..."

## claude-facts-3 [minor/accuracy]
- quote: 설치 프로그램이 실행할 때마다 한국어 문구를 다시 넣습니다.
- suggestion: 이 설치 프로그램으로 설치나 업데이트를 마칠 때마다 한국어 문구를 다시 넣습니다.
- problem: 한국어 덮어쓰기는 설치 단계를 실행할 때 일어나며, 설치 프로그램을 열었다가 첫 화면에서 아무것도 하지 않고 닫으면 일어나지 않는다. 한국어가 빠졌을 때 설치 프로그램을 열기만 하면 된다고 오해할 수 있다. before에도 같은 표현이 있었다.
- evidence: InstallRunner.cs:298-308 KoreanLocale.Apply는 게임 버전별 설치 단계 안에서 호출; Program.cs:108-109 첫 화면을 그냥 닫으면 아무것도 하지 않고 종료; KoreanLocale.cs:14 "written after every run's install steps"

## gpt-facts-0 [critical/accuracy]
- quote: "지금 설치" 또는 "지금 업데이트": 찾아낸 게임 버전에 권장 구성으로 바로 설치합니다. NVDA 음성 브리지와 Windows 음성 복사는 설치하지 않습니다.
- suggestion: "지금 설치": 찾아낸 게임 버전에 권장 구성으로 설치합니다. "지금 업데이트": WowVision이 이미 설치된 게임 버전만 현재 설정에 따라 업데이트합니다. 두 방법 모두 NVDA 음성 브리지와 Windows 음성 복사는 설치하지 않습니다.
- problem: 두 버튼의 대상과 설정 처리 방식이 다른데 하나로 설명했습니다. 이미 WowVision이 설치된 버전이 하나라도 있으면 "지금 업데이트"는 다른 게임 버전을 새로 설치하지 않으며, 권장 구성으로 초기화하지 않고 기존 선택을 유지합니다. 테스터가 다른 게임 버전에도 설치될 것으로 믿고 잘못된 방법을 고를 수 있습니다.
- evidence: wowvision-ko/wowvision-installer/WowVisionInstaller/UpdatePromptForm.cs:63-73에서 "지금 업데이트" 대상은 WowVision이 설치된 버전이며, Loc.cs:830-831도 업데이트는 현재 설정을 유지하고 새 설치만 권장 구성을 사용한다고 구분합니다.

## gpt-facts-1 [major/accuracy]
- quote: Windows 표시 언어가 한국어가 아니면 화면이 영어로 나옵니다.
- suggestion: Windows 표시 언어가 한국어이면 한국어로 나옵니다. 독일어 또는 프랑스어이면 해당 언어로 나오며, 그 밖의 언어에서는 영어로 나옵니다.
- problem: 한국어가 아닌 모든 환경에서 영어가 나온다는 설명은 틀렸습니다. 독일어와 프랑스어 Windows를 사용하는 테스터는 실제 화면과 안내가 일치하지 않습니다.
- evidence: wowvision-ko/wowvision-installer/WowVisionInstaller/Loc.cs:29-35에서 UI 언어를 독일어, 프랑스어, 한국어로 각각 선택하고 나머지만 영어로 설정합니다.

## gpt-facts-2 [major/terminology]
- quote: "설치 프로그램을 지금 업데이트"
- suggestion: "설치 프로그램을 지금 업데이트 (권장)"
- problem: 따옴표로 인용한 버튼 이름에서 화면에 표시되는 "(권장)"이 빠졌습니다. 실제 화면 문구와 다른 인용입니다.
- evidence: wowvision-ko/wowvision-installer/WowVisionInstaller/Loc.cs:856의 한국어 버튼 문구는 단축키 표시를 제외하면 "설치 프로그램을 지금 업데이트 (권장)"입니다.

## gpt-facts-3 [major/terminology]
- quote: "다음"으로 넘어가고 "뒤로"로 돌아갑니다.
- suggestion: "다음 >"으로 넘어가고 "< 뒤로"로 돌아갑니다.
- problem: 두 버튼의 인용에서 화면 문구에 포함된 화살표 기호가 빠졌습니다. 단축키 표시만 제외한다는 대조 규칙에 따르면 실제 버튼 이름과 일치하지 않습니다.
- evidence: wowvision-ko/wowvision-installer/WowVisionInstaller/Loc.cs:817-818의 한국어 버튼 문구는 단축키 표시를 제외하면 각각 "< 뒤로"와 "다음 >"입니다.

## gpt-facts-4 [major/accuracy]
- quote: 설치 프로그램이 실행할 때마다 한국어 문구를 다시 넣습니다.
- suggestion: 이 설치 프로그램으로 WowVision을 설치하거나 업데이트할 때마다 한국어 문구를 다시 넣습니다.
- problem: 실행만 해도 한국어 문구를 복원한다는 설명은 틀렸습니다. 설치 프로그램을 열었다가 설치나 업데이트 없이 닫으면 한국어 문구를 덮어쓰지 않으므로, 테스터가 실행만으로 복구됐다고 오해할 수 있습니다.
- evidence: wowvision-ko/wowvision-installer/WowVisionInstaller/InstallRunner.cs:298-307에서 한국어 문구 덮어쓰기는 각 설치 대상의 설치 처리 중 실행됩니다. KoreanLocale.cs:14-15도 매 실행의 설치 단계 뒤에 기록한다고 설명합니다.

## claude-editor-0 [major/context]
- quote: 이때는 구성 요소 페이지의 "이 설치 프로그램의 언어"에서 한국어를 고릅니다.
- suggestion: 언어를 바꾸는 곳은 "WowVision 새로 설치, 또는 다른 게임 버전에 설치"를 골랐을 때 나오는 구성 요소 페이지의 "이 설치 프로그램의 언어"뿐입니다. 영어 화면 그대로 진행해도 설치에는 문제가 없습니다.
- problem: 1단계에서 '이때는'이라고 해서 지금 바로 할 일처럼 지시한다. 그런데 구성 요소 페이지는 3단계에서 직접 고르기를 택해야만 나온다. 1단계를 듣는 테스터는 첫 화면에서 언어 선택을 찾게 되고, '지금 설치'를 고른 테스터는 그 페이지에 끝내 닿지 않는다. 지시가 실행 순서와 어긋나서 들었을 때 헷갈린다.
- evidence: Loc.cs:921 ui.installerLanguage("이 설치 프로그램의 언어:")는 구성 요소 화면 문구 묶음(Loc.cs:920 components.body 옆)에만 있다. after 3단계에 따르면 구성 요소 페이지는 직접 고르기 경로에서만 나온다.

## claude-editor-1 [minor/style]
- quote: 원본 WowVision 설치 프로그램 1.6에 한국어 화면과 한국어 문구 덮어쓰기를 더한 것입니다.
- suggestion: 이 설치 프로그램은 원본 WowVision 설치 프로그램 1.6과 같고, 두 가지를 더했습니다. 화면 문구를 한국어로 보여 주고, 설치가 끝날 때마다 WowVision에 한국어 문구를 덮어씁니다.
- problem: 주어가 빠져서 무엇을 '더한 것'인지 문장 안에서 드러나지 않는다. '한국어 문구 덮어쓰기'는 명사를 늘어놓은 말이라 무엇을 언제 덮어쓰는지 듣고서 알기 어렵다. before에 있던 '설치가 끝날 때마다'라는 시점 정보도 빠졌다.
- evidence: before 문장: "원본 WowVision 설치 프로그램 1.6과 같고, 두 가지만 더했습니다. 화면 문구에 한국어를 넣었고, 설치가 끝날 때마다 WowVision에 한국어 문자열을 덮어씁니다." 덮어쓰는 시점은 InstallRunner.cs:303의 KoreanLocale.Apply 호출(설치 흐름 안)이다.

## claude-editor-2 [minor/style]
- quote: 설치 프로그램이 실행할 때마다 한국어 문구를 다시 넣습니다.
- suggestion: 설치가 끝날 때마다 설치 프로그램이 한국어 문구를 다시 넣습니다.
- problem: '설치 프로그램이 실행할 때마다'는 주어와 서술어가 맞지 않는다. 실행하는 사람은 테스터이고 설치 프로그램은 실행되는 쪽이다. 게다가 한국어를 넣는 때는 프로그램을 켤 때가 아니라 설치가 끝날 때다. 지금 문장으로는 켰다가 닫기만 해도 한국어가 들어간다고 오해할 수 있다.
- evidence: InstallRunner.cs:303에서 KoreanLocale.Apply를 설치 실행 흐름 안에서 호출한다. guide-review.md 대조 자료에도 '설치가 끝날 때마다 koKR을 덮어씀(KoreanLocale.cs)'이라고 되어 있다.

## claude-editor-3 [minor/style]
- quote: 모든 애드온을 켜고 인터페이스를 다시 불러옵니다.
- suggestion: 이 명령은 모든 애드온을 켜고 인터페이스를 다시 불러옵니다.
- problem: 주어가 없어서 앞 문장과 같은 지시문, 곧 테스터가 할 일로 들린다. 그러면 테스터는 /enableaddons를 입력한 뒤 애드온을 직접 켜거나 /reload를 따로 해야 한다고 오해할 수 있다. 실제로는 이 명령이 하는 일을 설명하는 문장이다.
- evidence: installation.md:30: "type the game's own command /enableaddons ... It switches on all your addons and reloads the interface." 원문은 명령을 가리키는 주어 It을 둔다.

## claude-editor-4 [minor/style]
- quote: WoW Login Tool 설치(권장) (기본 체크됨)
- suggestion: WoW Login Tool 설치(권장): 기본으로 체크되어 있습니다.
- problem: 옵션 이름에 붙은 괄호 바로 뒤에 기본값 괄호가 또 붙는다. 스크린리더가 괄호를 읽는 설정이면 괄호 열고 닫기를 두 번 연달아 읽게 되어, 어디까지가 옵션 이름인지 구분하기 어렵다. 같은 목록의 '추가 권장 애드온' 항목은 쌍점 뒤 문장으로 기본값을 말하고 있어서 형식도 섞였다. '모두 다시 설치(복구) (기본 체크 안 됨)'도 문제가 같으니 '모두 다시 설치(복구): 기본으로 체크되어 있지 않습니다. 설치가 손상되었을 때 사용합니다.'로 함께 맞춘다.
- evidence: 옵션 이름 자체에 괄호가 들어 있다. Loc.cs:1045 "WoW Login Tool 설치(권장)", Loc.cs:933 opt.force.label "모두 다시 설치(복구)". guide-lens-editor.md는 괄호가 겹쳐서 듣기를 방해하는 곳을 보라고 한다.

## claude-editor-5 [minor/style]
- quote: 1. `WowVisionInstaller.exe`를 실행합니다.
- suggestion: 1. WowVisionInstaller.exe를 실행합니다.
- problem: 역따옴표는 마크다운의 코드 표기라서 텍스트 파일에서는 기호로 그대로 남는다. 문장부호를 읽는 설정의 스크린리더는 파일 이름 앞뒤에서 이 기호 이름을 읽는다. 도입부의 '`WowVisionInstaller.exe`를 실행해서'도 같으니 모두 역따옴표를 뺀다. 제목 줄의 #, ## 기호도 같은 이유로 텍스트 파일에서는 그대로 읽힌다.
- evidence: guide-review.md 문서 규칙: '마크다운 기호는 텍스트 파일로 그대로 읽히므로 본문 지시에 넣지 않는다.' 배포 형식은 설치_안내.txt다.

## claude-editor-6 [minor/context]
- quote: WowVision이 NVDA로 말하게 하려면 이쪽을 고르고 아래 "직접 고르기" 절을 따릅니다.
- suggestion: WowVision이 NVDA로 말하게 하려면 이쪽을 고르고 아래 "직접 고르기" 절을 따른 뒤, 4단계로 돌아옵니다.
- problem: 직접 고르기를 택한 테스터를 다른 절로 보내면서 돌아올 곳을 말하지 않는다. '직접 고르기' 절은 음성 옵션 설명으로 끝난다. 그래서 이 경로의 테스터는 설치가 끝난 뒤 '설치 프로그램 닫기'와 게임 재시작(4, 5단계)을 놓칠 수 있다. 화면 없이 순서대로 듣는 테스터에게는 돌아갈 위치를 알려 줘야 한다.
- evidence: after의 '직접 고르기' 절 마지막 문단은 음성 옵션 설명이고, 설치가 끝난 뒤 할 일은 나오지 않는다. 완료 화면 문구(Loc.cs:873-878의 "완료", "문제가 있었지만 완료", "설치 프로그램 닫기")는 4단계에만 나온다.

## gpt-editor-0 [major/style]
- quote: # WowVision 한국어판 테스트 설치 안내
- suggestion: WowVision 한국어판 테스트 설치 안내
- problem: 텍스트 파일에서는 제목 기호가 서식으로 처리되지 않습니다. NVDA가 기호를 읽도록 설정된 테스터에게는 제목마다 ‘샵’이 들려 문서 구조 파악을 방해합니다. 같은 방식으로 붙인 나머지 제목 기호도 제거해야 합니다.
- evidence: 입력에서 제시한 문서 규칙은 ‘마크다운 기호는 텍스트 파일로 그대로 읽히므로 본문 지시에 넣지 않는다’고 명시합니다.

## gpt-editor-1 [major/style]
- quote: `WowVisionInstaller.exe`를 실행해서 설치하고
- suggestion: WowVisionInstaller.exe를 실행해서 설치하고
- problem: 백틱은 텍스트 파일에서 코드 서식으로 바뀌지 않습니다. 기호 읽기를 켠 NVDA에서는 파일명 앞뒤의 백틱까지 들려 실행할 파일명을 알아듣는 데 방해가 됩니다. 설치하기 1단계에 반복된 백틱도 함께 제거해야 합니다.
- evidence: 입력에서 제시한 문서 규칙은 ‘마크다운 기호는 텍스트 파일로 그대로 읽히므로 본문 지시에 넣지 않는다’고 명시합니다.

## gpt-editor-2 [minor/style]
- quote: 원본 WowVision 설치 프로그램 1.6에 한국어 화면과 한국어 문구 덮어쓰기를 더한 것입니다.
- suggestion: 원본 WowVision 설치 프로그램 1.6의 화면을 한국어로 번역하고, 설치가 끝날 때마다 WowVision에 한국어 문구를 덮어쓰도록 바꾼 것입니다.
- problem: ‘한국어 화면’과 ‘한국어 문구 덮어쓰기’를 명사로 나열해 무엇을 어디에 덮어쓰는지 빠졌습니다. 동작과 대상을 풀어 쓰면 번역투가 줄고 두 변경 사항을 한 번에 이해할 수 있습니다.
- evidence: before에는 ‘화면 문구에 한국어를 넣었고, 설치가 끝날 때마다 WowVision에 한국어 문자열을 덮어씁니다.’라고 동작과 대상을 각각 밝혔습니다.

## gpt-editor-3 [major/context]
- quote: 게임이 켜져 있었다면 다시 시작합니다.
- suggestion: 
- problem: 앞에서 World of Warcraft를 완전히 종료하도록 지시했으므로, 정상적으로 순서를 따른 테스터에게는 성립하지 않는 조건입니다. 게임이 켜진 상태도 허용되는지 혼동하게 하므로 삭제해야 합니다.
- evidence: after의 시작하기 전에는 ‘World of Warcraft를 완전히 종료합니다.’라고 지시하며, before에도 설치 후에는 ‘설치가 끝나면 Battle.net에서 게임을 시작합니다.’만 있었습니다.

## gpt-editor-4 [major/style]
- quote: - WoW Login Tool 설치(권장) (기본 체크됨)
- suggestion: - WoW Login Tool 설치(권장): 기본으로 체크되어 있습니다.
- problem: 화면에 표시되는 옵션 이름의 괄호 바로 뒤에 설명용 괄호가 이어집니다. 소리로 들으면 ‘권장’까지가 실제 옵션 이름이고 ‘기본 체크됨’은 안내의 설명이라는 경계를 구분하기 어렵습니다.
- evidence: 인접한 두 괄호 중 ‘WoW Login Tool 설치(권장)’은 화면 문구이고, before는 뒤의 상태만 ‘(체크됨)’으로 덧붙였습니다. 화면 문구는 유지하면서 상태 설명을 문장으로 분리할 수 있습니다.

## gpt-editor-5 [major/style]
- quote: 모든 애드온을 켜고 인터페이스를 다시 불러옵니다.
- suggestion: /enableaddons 명령은 모든 애드온을 켜고 인터페이스를 다시 불러옵니다.
- problem: 주어가 없어 테스터가 /enableaddons 입력 뒤에 애드온을 직접 켜는 별도 작업까지 해야 하는 것처럼 들립니다. 명령의 효과임을 명시해야 단계가 추가된 것으로 오해하지 않습니다.
- evidence: wowvision-ko/WowVision/docs/src/user/en/getting-started/installation.md:30은 /enableaddons 명령 자체가 모든 애드온을 켜고 인터페이스를 다시 불러온다고 설명합니다.

