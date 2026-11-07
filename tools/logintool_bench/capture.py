"""측정 애드온 페이지를 캡처한다(capture.ahk 대체).

capture.ahk 는 쪽마다 보조 프로그램을 새로 실행했고, 그때마다 콘솔이 게임 창의 초점을 가져가서
70쪽 근처에서 멈췄다(2026-11-07, 초점 복구 94회). 여기서는 보조 프로그램을 창 없는 repl 프로세스
하나로 띄워 두고 "save <파일>"만 보낸다.

- 수동 넘김: 다음 쪽 키(CTRL-SHIFT-F12)는 게임 창이 앞에 있을 때만 보낸다. 30초 넘게 앞에 없거나
  보조 프로그램이 오류를 응답하면 멈춘다(잘못된 쪽을 찍지 않는다).
- 자동 넘김(--auto, /otb auto 와 함께): 키 없이 0.6초마다 저장한다. 오류 응답은 기록만 하고 계속한다.
  그 쪽은 평가기가 "PAGE 표지를 읽지 못한 쪽"으로 따로 보고한다.
보조 프로그램이 10초 안에 응답하지 않으면 두 경우 모두 멈춘다.

사용: uv run python -m tools.logintool_bench.capture <캡처 폴더> <쪽 수>
      uv run python -m tools.logintool_bench.capture <캡처 폴더> <초> --auto
애드온은 미리 1쪽을 보여 주고 있어야 한다(/otb start 또는 /otb auto 2).
"""

from __future__ import annotations

import ctypes
import queue
import subprocess
import sys
import threading
import time
from ctypes import wintypes
from pathlib import Path
from typing import IO

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "WoW Login Tool Korean" / "helper" / "SkuLoginSense.exe"
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

VK_CONTROL, VK_SHIFT, VK_F12 = 0x11, 0x10, 0x7B
KEYUP = 0x0002
ANSWER_TIMEOUT = 10.0


def foreground_exe() -> str:
    hwnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    h = kernel32.OpenProcess(0x1000, False, pid.value)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wintypes.DWORD(1024)
        kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size))
        return Path(buf.value).name.lower()
    finally:
        kernel32.CloseHandle(h)


def wait_for_game(limit: float = 30.0) -> bool:
    end = time.monotonic() + limit
    while time.monotonic() < end:
        if foreground_exe() == "wow.exe":
            return True
        time.sleep(0.2)
    return False


def next_page() -> None:
    for vk in (VK_CONTROL, VK_SHIFT, VK_F12):
        user32.keybd_event(vk, 0, 0, 0)
        time.sleep(0.02)
    for vk in (VK_F12, VK_SHIFT, VK_CONTROL):
        user32.keybd_event(vk, 0, KEYUP, 0)
        time.sleep(0.02)


def _pump(stream: IO[str], q: queue.Queue[str]) -> None:
    for line in stream:
        q.put(line.strip())


def main() -> int:
    out = Path(sys.argv[1])
    pages = int(sys.argv[2])
    auto = len(sys.argv) > 3 and sys.argv[3] == "--auto"
    out.mkdir(parents=True, exist_ok=True)
    log = open(out / "capture-log.txt", "w", encoding="utf-8")  # noqa: SIM115 - closed in finally
    proc = subprocess.Popen([str(HELPER), "repl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW,
                            text=True, encoding="utf-8")
    assert proc.stdin and proc.stdout
    answers: queue.Queue[str] = queue.Queue()
    threading.Thread(target=_pump, args=(proc.stdout, answers), daemon=True).start()

    def save(shot: Path) -> str | None:
        """None: no answer in time. Otherwise the helper's JSON line."""
        assert proc.stdin
        proc.stdin.write(f'save "{shot}"\n')
        proc.stdin.flush()
        try:
            return answers.get(timeout=ANSWER_TIMEOUT)
        except queue.Empty:
            return None

    try:
        if auto:
            end = time.monotonic() + pages
            n = 0
            while time.monotonic() < end:
                n += 1
                answer = save(out / f"c_{n:05d}.png")
                print(f"{n} {answer}", file=log, flush=True)
                if answer is None:
                    print("helper did not answer - stopped", file=log, flush=True)
                    return 3
                time.sleep(0.6)
            print("done", file=log, flush=True)
            return 0
        for i in range(1, pages + 1):
            if not wait_for_game():
                print(f"game window not in front before page {i} - stopped", file=log, flush=True)
                return 2
            answer = save(out / f"p_{i:04d}.png")
            print(f"{i} {answer}", file=log, flush=True)
            if answer is None or '"error"' in answer:
                print("helper failed - stopped", file=log, flush=True)
                return 3
            if not wait_for_game():
                print(f"game window not in front after page {i} - stopped", file=log, flush=True)
                return 2
            next_page()
            time.sleep(0.45)
        print("done", file=log, flush=True)
        return 0
    finally:
        try:
            proc.stdin.write("exit\n")
            proc.stdin.flush()
            proc.wait(timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            proc.kill()
        log.close()


if __name__ == "__main__":
    sys.exit(main())
