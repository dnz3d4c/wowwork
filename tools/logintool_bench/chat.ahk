#Requires AutoHotkey v2.0
; Types one chat command into the WoW window (SendText bypasses the Korean IME).
;   AutoHotkeyV2.exe chat.ahk "/otb start"
if (A_Args.Length != 1 || SubStr(A_Args[1], 1, 1) != "/" || InStr(A_Args[1], ":"))
    ExitApp(3)   ; only a slash command; a converted path (C:/...) must never reach the chat
win := "ahk_exe Wow.exe"
if !WinExist(win)
    ExitApp(1)
WinActivate(win)
if !WinWaitActive(win, , 5)
    ExitApp(2)
Sleep(400)
Send("{Escape}")
Sleep(300)
Send("{Enter}")
Sleep(300)
SetKeyDelay(40, 20)
SendEvent("{Raw}" A_Args[1])
Sleep(200)
Send("{Enter}")
ExitApp(0)
