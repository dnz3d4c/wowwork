"""캐릭터 선택 화면 OCR 측정용 이름 묶음을 만든다.

한 사람의 캐릭터 몇 개로는 "다른 캐릭터도 읽히는가"를 알 수 없다. 그래서 이름을 여섯 종류로 만든다.

- coverage: KS X 1001 상용 한글 2,350자를 빠짐없이 한 번 이상 쓰는 이름
- rare: 상용 밖 음절(뷁, 똠 같은 글자)이 섞인 이름
- word: 게임 문자열에서 뽑은 실제 낱말과 낱말 두 개를 붙인 이름("까다로운힐링" 같은 꼴)
- complex: 된소리, 이중모음, 겹받침이 많은 이름
- repeat: 같은 음절을 되풀이한 이름
- latin: 영문 이름

사용:
  uv run python -m tools.logintool_bench.corpus <애드온 폴더>   # data.lua 를 쓴다
"""

from __future__ import annotations

import csv
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GS_KO = ROOT / "cache" / "gs_koKR.csv"

ALL_HANGUL = [chr(c) for c in range(0xAC00, 0xD7A4)]


def _is_common(ch: str) -> bool:
    # Python 의 euc_kr 은 상용 밖 음절을 8바이트 자모 조합으로 인코딩하므로 길이로 가른다
    return len(ch.encode("euc_kr")) == 2


COMMON = frozenset(ch for ch in ALL_HANGUL if _is_common(ch))

# 초성 된소리(ㄲㄸㅃㅆㅉ), 중성 이중모음(ㅘㅙㅚㅝㅞㅟㅢ), 종성 겹받침
_DOUBLE_INITIAL = {1, 4, 8, 10, 13}
_COMPLEX_VOWEL = {9, 10, 11, 14, 15, 16, 19}
_DOUBLE_FINAL = {3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 18}


def _jamo(ch: str) -> tuple[int, int, int]:
    code = ord(ch) - 0xAC00
    return code // 588, (code % 588) // 28, code % 28


def _is_complex(ch: str) -> bool:
    i, v, f = _jamo(ch)
    return i in _DOUBLE_INITIAL or v in _COMPLEX_VOWEL or f in _DOUBLE_FINAL


def _length(rng: random.Random) -> int:
    return rng.choices([2, 3, 4, 5, 6], weights=[2, 4, 4, 2, 1])[0]


def _game_words() -> list[str]:
    words: set[str] = set()
    if not GS_KO.exists():
        return []
    with open(GS_KO, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for tok in re.findall(r"[가-힣]+", row["TagText_lang"]):
                if 2 <= len(tok) <= 6:
                    words.add(tok)
    return sorted(words)


def build_names(seed: int = 1) -> list[dict[str, str]]:
    rng = random.Random(seed)
    names: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(name: str, kind: str) -> bool:
        if name in seen:
            return False
        seen.add(name)
        names.append({"name": name, "kind": kind})
        return True

    common = sorted(COMMON)
    pool = common[:]
    rng.shuffle(pool)
    while pool:
        n = min(_length(rng), len(pool))
        chunk, pool = pool[:n], pool[n:]
        if len(chunk) < 2:
            chunk.append(rng.choice(common))
        add("".join(chunk), "coverage")

    rare = [ch for ch in ALL_HANGUL if ch not in COMMON]
    for ch in rng.sample(rare, 200):
        n = _length(rng)
        body = [rng.choice(common) for _ in range(n - 1)]
        body.insert(rng.randrange(n), ch)
        add("".join(body), "rare")

    words = _game_words()
    for w in rng.sample(words, min(150, len(words))):
        add(w, "word")
    short = [w for w in words if len(w) <= 3]
    made = 0
    while short and made < 100:
        w = rng.choice(short) + rng.choice(short)
        if len(w) <= 6 and add(w, "word"):
            made += 1

    hard = [ch for ch in ALL_HANGUL if _is_complex(ch)]
    hard_common = [ch for ch in hard if ch in COMMON]
    made = 0
    while made < 120:
        n = rng.choice([3, 4, 5])
        name = "".join(rng.choice(hard_common if rng.random() < 0.7 else hard) for _ in range(n))
        if add(name, "complex"):
            made += 1

    made = 0
    while made < 30:
        syl = rng.choice(common)
        if add(syl * rng.choice([2, 3]), "repeat"):
            made += 1

    cons, vows = "bcdfghjklmnprstvwz", "aeiouy"
    made = 0
    while made < 60:
        n = rng.randint(3, 12)
        s = "".join(rng.choice(cons) if i % 2 == 0 else rng.choice(vows) for i in range(n))
        if add(s.capitalize(), "latin"):
            made += 1
    return names


def _lua_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def lua_data(names: list[dict[str, str]]) -> str:
    rows = ",\n".join("{" + _lua_str(n["name"]) + "," + _lua_str(n["kind"]) + "}" for n in names)
    return "local _, ns = ...\nns.NAMES = {\n" + rows + "\n}\n"


def main() -> None:
    out = Path(sys.argv[1]) / "data.lua"
    names = build_names()
    out.write_text(lua_data(names), encoding="utf-8")
    kinds: dict[str, int] = {}
    for n in names:
        kinds[n["kind"]] = kinds.get(n["kind"], 0) + 1
    print(f"{out}: {len(names)} names {kinds}")


if __name__ == "__main__":
    main()
