#Requires AutoHotkey v2.0
; Captures the LoginToolOcrBench pages. The addon must already show page 1
; (/otb start). Each round: save the window with the login tool's own helper
; (same WGC path the tool uses), then CTRL-SHIFT-F12 for the next page.
;   AutoHotkeyV2.exe capture.ahk <SkuLoginSense.exe> <output folder> <pages>
helper := A_Args[1]
outDir := A_Args[2]
pages := Integer(A_Args[3])
DirCreate(outDir)
logf := FileOpen(outDir "\capture-log.txt", "w", "UTF-8")
win := "ahk_exe Wow.exe"
if !WinExist(win) {
    logf.WriteLine("no Wow.exe window")
    ExitApp(1)
}
WinActivate(win)
WinWaitActive(win, , 5)
Sleep(800)
loop pages {
    if !WinActive(win) {
        logf.WriteLine("lost focus before page " A_Index " - stopped")
        ExitApp(2)
    }
    file := outDir "\p_" Format("{:04}", A_Index) ".png"
    code := RunWait('"' helper '" save "' file '"', , "Hide")
    logf.WriteLine(A_Index " exit=" code)
    Send("^+{F12}")
    Sleep(450)
}
logf.WriteLine("done")
logf.Close()
ExitApp(0)
