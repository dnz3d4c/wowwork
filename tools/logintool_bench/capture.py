"""측정 애드온 페이지를 캡처한다(capture.ahk 대체).

capture.ahk 는 쪽마다 보조 프로그램을 새로 실행했고, 그때마다 콘솔이 게임 창의 초점을 가져가서
70쪽 근처에서 멈췄다(2026-11-07, 초점 복구 94회). 여기서는 보조 프로그램을 창 없는 repl 프로세스
하나로 띄워 두고 "save <파일>"만 보낸다. 다음 쪽 키(CTRL-SHIFT-F12)는 게임 창이 앞에 있을 때만 보낸다.
게임 창이 앞에 없으면 기다리고, 30초 넘게 돌아오지 않으면 멈춘다(잘못된 쪽을 찍지 않는다).

사용: uv run python -m tools.logintool_bench.capture <캡처 폴더> <쪽 수>
      uv run python -m tools.logintool_bench.capture <캡처 폴더> <초> --auto   # /otb auto 와 함께
애드온은 미리 1쪽을 보여 주고 있어야 한다(/otb start).
"""

from __future__ import annotations

import ctypes
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "WoW Login Tool Korean" / "helper" / "SkuLoginSense.exe"
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

VK_CONTROL, VK_SHIFT, VK_F12 = 0x11, 0x10, 0x7B
KEYUP = 0x0002


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


def main() -> int:
    out = Path(sys.argv[1])
    pages = int(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    log = open(out / "capture-log.txt", "w", encoding="utf-8")  # noqa: SIM115 - closed in finally
    proc = subprocess.Popen([str(HELPER), "repl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW,
                            text=True, encoding="utf-8")
    assert proc.stdin and proc.stdout
    try:
        if len(sys.argv) > 3 and sys.argv[3] == "--auto":
            # /otb auto: the addon turns the pages; just keep saving the window
            # (WGC also captures a window that is not in front) for <pages> seconds
            end = time.monotonic() + pages
            n = 0
            while time.monotonic() < end:
                n += 1
                shot = out / f"c_{n:05d}.png"
                proc.stdin.write(f'save "{shot}"\n')
                proc.stdin.flush()
                print(f"{n} {proc.stdout.readline().strip()}", file=log, flush=True)
                time.sleep(0.6)
            print("done", file=log, flush=True)
            return 0
        for i in range(1, pages + 1):
            if not wait_for_game():
                print(f"game window not in front before page {i} - stopped", file=log, flush=True)
                return 2
            shot = out / f"p_{i:04d}.png"
            proc.stdin.write(f'save "{shot}"\n')
            proc.stdin.flush()
            answer = proc.stdout.readline().strip()
            print(f"{i} {answer}", file=log, flush=True)
            if not wait_for_game():
                print(f"game window not in front after page {i} - stopped", file=log, flush=True)
                return 2
            next_page()
            time.sleep(0.45)
        print("done", file=log, flush=True)
        return 0
    finally:
        proc.stdin.write("exit\n")
        proc.stdin.flush()
        proc.wait(timeout=10)
        log.close()


if __name__ == "__main__":
    sys.exit(main())
