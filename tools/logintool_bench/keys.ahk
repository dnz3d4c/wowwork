#Requires AutoHotkey v2.0
; Sends keys to the WoW window, one AHK key name per argument, 1.5 s apart
; (the login tool needs time to hover and the client to narrate).
;   AutoHotkeyV2.exe keys.ahk Escape Down Down Up
win := "ahk_exe Wow.exe"
if !WinExist(win)
    ExitApp(1)
WinActivate(win)
if !WinWaitActive(win, , 5)
    ExitApp(2)
Sleep(400)
SendLevel(1)   ; the login tool's hotkeys ignore level-0 input from other AHK scripts
for key in A_Args {
    if !RegExMatch(key, "^[A-Za-z0-9]+$")
        ExitApp(3)
    Send("{" key "}")
    Sleep(1500)
}
ExitApp(0)
