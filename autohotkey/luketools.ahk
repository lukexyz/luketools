#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.

SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


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




