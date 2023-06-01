#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.

SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


; ---------- PRESENTATION MODE  -----------
;           (Added 2023-06-01)
; ----------------------------------------
#Persistent  ; Ensures the script keeps running permanently

presentation_mode := false  ; Initializes the presentation_mode variable to false

!p::  ; TOGGLE PRESENTATION MODE ("alt + p")
    presentation_mode := !presentation_mode
    if presentation_mode {
        MsgBox,, Presentation Mode, Presentation Mode ON, .5  ; .5 for half a second, adjust as needed
        SetTimer, CloseMsgBox, -500  ; -500 for half a second, adjust as needed
    }
    else {
        MsgBox,, Presentation Mode, Presentation Mode OFF, .5
        SetTimer, CloseMsgBox, -500
    }
return

CloseMsgBox:
    WinClose, Presentation Mode
return

#If presentation_mode  ; The hotkeys following will only be active if presentation_mode is true

    1::             ; HIGHLIGHTER ("ctrl + shift + Q" hotkey remapped to "1")
        send ^+{q}
    return 

    2::             ; UNDO
        send ^+{6}
    return 

    3::             ; CLEAR SCREEN
        send ^+{x}
    return 

    4::             ; CURSOR
        send ^+{z}
    return 

    5::             ; SHOW/HIDE EPIC PEN
        send ^+{1}
    return 

#If  ; Ends the conditional block


; -------- EN DASH  ------------
;(alt dash -> send en dash) 

!-::
	send {ASC 0150}
return



; -------- ALT ARROWS KEYS "IJKL" ------------

!I::
    send {up}
return 

!K::
    send {down}
return

!J::
    send {left}
return

!L::
    send {right}
return


; ------------ LINE JUMPS ----------------

; Alt+U = CTRL+Left

!U:: 
    send ^{left}
return

!O::
    send ^{right}
return

!H::
    send {home}
return

!`;::
    send {end}
return



; ------------ MEDIA CONTROL ----------------

; for previous 
; PgDn::Media_Prev

; for next 
; PgUp::Media_Next

;Pause::Media_Play_Pause

;+PgUp::SoundSet +2
;+PgDn::SoundSet -2
;+Home::SoundSet, +1, , mute




