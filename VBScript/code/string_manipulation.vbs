' String manipulation examples
Option Explicit

Dim txt, txt2, msg
txt = "Hello Chris! This is VBScript"
txt2 = "    (12,23)  "

Function addMsg(msg1)
    addMsg = msg & msg1 & vbNewLine
End Function

' Display the text
msg = addMsg("Text: " & txt)
msg = addMsg("Second text: " & txt2)

' Len(string) - get the number of characters in the string
msg = addMsg("String length: " & Len(txt))

' InStr returns the position of the first occurrence of one string in another
' InStr(string1, string2) - search for string2 in string1 starting at the beginning of the string
' InStrRev - start at the end of the string
msg = addMsg("First occurrence of 'is' is: " & InStr(txt, "is"))
msg = addMsg("Last occurrence of 'is' is: " & InStrRev(txt, "is"))

' LCase -- convert to lowercase
msg = addMsg("Lowercase version: " & LCase(txt))

' UCase -- convert to uppercase
msg = addMsg("Uppercase version: " & UCase(txt))

' Left(string, length) -- get characters from the start of the string
msg = addMsg("First 15 characters: " & Left(txt, 15))

' Mid(string, start [,length]) -- get characters from the string
msg = addMsg("Character 9 to 19: " & Mid(txt, 9, 19))

' Right(string, length) -- get length characters from the end of the string
msg = addMsg("Last 5 characters: " & Right(txt, 5))

' Replace(string, find, replaceWith) -- replaces a specified part of the string
msg = addMsg("Replacing space with *: " & Replace(txt, " ", "*"))

' StrReverse(string) -- reverse a string
msg = addMsg("Reversed string: " & StrReverse(txt))

' LTrim(string) -- remove spaces on the left-side of the string
msg = addMsg("Remove left spaces: " & LTrim(txt2))

' RTrim(string) -- remove spaces on the right-side of the string
msg = addMsg("Remove right spaces: " & RTrim(txt2))

' Trim(string) -- remove spaces on both sides
msg = addMsg("Remove left and right spaces: " & Trim(txt2))

' Space(number) -- creates a string with a given number of spaces
msg = addMsg("Creating 7 spaces: " & "*" & Space(7) & "*")

' Compare two strings
msg = addMsg("Comparing abs and acb: " & StrComp("abc", "acb"))

MsgBox msg
