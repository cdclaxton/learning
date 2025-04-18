Dim d, message
d = weekday(date)
Select Case d
    Case 6
        message = "Nearly the weekend"
    Case 1
        message = "Last day of the weekend"
    Case 7
        message = "It's the weekend"
    Case else
        message = "Not the weekend yet. Keep working!"
End Select

MsgBox("Day = " & d & vbNewLine & message)
