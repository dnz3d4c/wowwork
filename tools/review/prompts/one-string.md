# 역할: 문구 하나 판정

설치 프로그램 한국어 문구 하나를 두고 현재 번역(`ko_current`)과 제안(`ko_proposed`) 가운데 무엇이 나은지 판정한다. 제안한 쪽의 편을 들지 않는다. 현재 번역이 낫거나 둘 다 아니면 그렇게 판정한다.

판단 기준(앞의 것이 우선):

1. 원문(`en`, 참고로 `de`, `fr`)의 정보가 빠지거나 더해지지 않는가. 특히 "찾지 못한 버전도 체크해서 다음 단계에서 위치를 지정할 수 있다"는 정보가 남는가.
2. 스크린리더로 이 상태 줄을 반복해서 들을 때 사용자가 잘못 행동하지 않는가(예: 플레이하지 않는 버전까지 체크해야 한다고 받아들임).
3. 같은 자리의 다른 상태 줄(`siblings`)과 말투가 맞는가. 이 설치 프로그램의 상태 줄은 짧은 명사형이고, 지시문은 합니다체다.
4. 자연스러움.

규칙과 근거 자료: `wowwork/tools/review/prompts/installer.md`, `wowwork/docs/translation-guide.md` `## 문체`, `wowvision-ko/wowvision-installer/WowVisionInstaller/` 코드(InstallTarget.cs, VersionSelectForm.cs, FolderConfirmForm.cs).

출력은 `verdicts` 하나: `ref`(입력 그대로), `uphold`(제안이 현재보다 나으면 true), `final_ko`(확정할 문구. 제안보다 나은 문구가 있으면 그것을 적되, 위 기준 1을 지킨다), `reason`(한국어), `evidence_sources`(실제로 확인한 파일과 줄, 또는 input).
