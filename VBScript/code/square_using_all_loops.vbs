Option Explicit
Dim minVal, maxVal, values(4)

Function square(x)
    square = x * x
End Function

minVal = 0
maxVal = 3

' For ... Next
Dim forNext, i
forNext = "For ... Next: "
For i = minVal To maxVal
    values(i) = i
    forNext = forNext & square(i) & " "
Next

' For Each ... Next
Dim forEachResult
forEachResult = "For Each ... Next: "
For Each i In values
    forEachResult = forEachResult & square(i) & " "
Next

' Do While <test> ... Loop
Dim doLoopResult
doLoopResult = "Do ... Loop: "
i = 0
Do While i <= maxVal
    doLoopResult = doLoopResult & square(i) & " "
    i = i + 1
Loop

' Do ... Loop While <test>
Dim doLoopWhileResult
doLoopWhileResult = "Do ... Loop While: "
i = 0
Do
    doLoopWhileResult = doLoopWhileResult & square(i) & " "
    i = i + 1
Loop While i <= maxVal

' Do Until <test> ... Loop
Dim doUntilResult
doUntilResult = "Do Until ... Loop: "
i = 0
Do Until i > maxVal
    doUntilResult = doUntilResult & square(i) & " "
    i = i + 1
Loop

' Do ... Loop Until <test>
Dim doLoopUntilResult
doLoopUntilResult = "Do ... Loop Until: "
i = 0
Do
    doLoopUntilResult = doLoopUntilResult & square(i) & " "
    i = i + 1
Loop Until i > maxVal

' While ... Wend
Dim whileWendResult
whileWendResult = "While ... Wend: "
i = 0
While i <= maxVal
    whileWendResult = whileWendResult & square(i) & " "
    i = i + 1
Wend

MsgBox(forNext & vbNewLine & _
forEachResult & vbNewLine & _
doLoopResult & vbNewLine & _
doLoopWhileResult & vbNewLine & _
doUntilResult & vbNewLine & _
doLoopUntilResult & vbNewLine & _
whileWendResult)
