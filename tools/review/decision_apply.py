"""2026-11-07 사용자 결정을 한국어 설명서에 일괄 반영한다(docs/decisions.tsv).

- alert: "경보" → "알림". 받침이 생기므로 바로 뒤 조사를 맞춘다(는→은, 를→을, 가→이, 와→과, 나→이나, 로→으로).
- 게임 버전 이름: "리테일" → "Retail", "클래식 시대" → "Classic Era" (뒤 조사는 받침이 같아 그대로).
- "오류 알리기"(koKR Announce Errors = "오류 알림"과 다른 표기) → "오류 알림", 조사 맞춤.
인라인 코드와 코드 블록은 건드리지 않는다.

사용: uv run python -m tools.review.decision_apply [--dry-run]
"""

from __future__ import annotations

import re
import sys

from tools.manual import KO_ROOT

# 받침 없는 말 → 받침 있는 말로 바뀔 때의 조사
_PARTICLE = {"는": "은", "를": "을", "가": "이", "와": "과", "나": "이나", "로": "으로"}
_CODE = re.compile(r"```.*?```|`[^`\n]+`", re.DOTALL)


def _swap_batchim(text: str, old: str, new: str) -> str:
    def repl(m: re.Match[str]) -> str:
        paren, p = m.group(1) or "", m.group(2)
        return new + paren + _PARTICLE.get(p, p)

    # 바로 뒤 한 글자가 조사면 바꾼다. 설명서에서 "경보" 뒤에 오는 형태를 모두 뽑아 보니
    # 조사뿐이었다(2026-11-07: 를·가·는·와·에는·의·입니다·도·에·마다·나·처럼·에만·이며·에서·만·로·들과·까지).
    # 괄호가 끼어 있어도 조사는 괄호 앞 낱말을 따른다("경보(켬)와" → "알림(켬)과").
    return re.sub(re.escape(old) + r"(\([^)]*\))?(는|를|가|와|나|로|)", repl, text)


def _apply_plain(text: str) -> str:
    text = _swap_batchim(text, "경보", "알림")
    text = _swap_batchim(text, "오류 알리기", "오류 알림")
    return text.replace("클래식 시대", "Classic Era").replace("리테일", "Retail")


def apply_text(text: str) -> str:
    out, last = [], 0
    for m in _CODE.finditer(text):
        out.append(_apply_plain(text[last : m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(_apply_plain(text[last:]))
    return "".join(out)


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed = 0
    for p in sorted(KO_ROOT.rglob("*.md")):
        old = p.read_text(encoding="utf-8")
        new = apply_text(old)
        if new != old:
            changed += 1
            if not dry:
                p.write_text(new, encoding="utf-8", newline="\n")
    print(f"바뀐 파일 {changed}개" + (" (dry-run)" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
