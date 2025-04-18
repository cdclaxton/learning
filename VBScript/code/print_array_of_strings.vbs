Dim names(2), namesToShow
names(0) = "Chris"
names(1) = "David"
names(2) = "George"
For i = 0 To 2
    namesToShow = namesToShow & names(i) & " "
Next
MsgBox namesToShow
