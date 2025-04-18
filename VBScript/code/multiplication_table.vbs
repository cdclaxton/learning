Dim table(4,3), multiplicationTable
For row = 0 To 4
    For col = 0 To 3
        multiplicationTable = multiplicationTable & ((row+1) * (col+1)) & " "
    Next
    multiplicationTable = multiplicationTable & vbNewLine
Next
MsgBox multiplicationTable
