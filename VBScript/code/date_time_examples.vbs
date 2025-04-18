' Demonstration of different date and time functions
Option Explicit
Dim msg

Function appendToMessage(newMessage) 
    appendToMessage = msg & newMessage & vbNewLine
End Function

' Get the current system time
msg = appendToMessage("System time: " & Time)

' Get the parts of the system time
msg = appendToMessage("Hour: " & Hour(Now))
msg = appendToMessage("Minute: " & Minute(Now))
msg = appendToMessage("Seconds: " & Second(Now))

' Get the current system date
msg = appendToMessage("System date: " & Date)

' Get the current date and time
msg = appendToMessage("Date and time: " & Now)

' Get the day (1 to 31), month (1 to 12) and year
msg = appendToMessage("Day: " & Day(now))
msg = appendToMessage("Month: " & Month(now))
msg = appendToMessage("Year: " & Year(now))

' Show the month name and abbreviated version
msg = appendToMessage("Month name: " & MonthName(Month(Now), False))
msg = appendToMessage("Month name: " & MonthName(Month(Now), True))

' Get the day of the week (first day of week set to Monday)
msg = appendToMessage("Week day: " & WeekDay(Now, 2))

' Get the name of the week day
msg = appendToMessage("Week day: " & WeekdayName(WeekDay(Now, 2), False, 2))

' Date part
msg = appendToMessage("Quarter: " & DatePart("q", Now))

' DateDiff(interval, date1, date2) - get the number of intervals between two dates
Dim born : born = "26-Feb-1980 14:15:00"
msg = appendToMessage("Number of hours alive: " & DateDiff("h",born,Now))

' Convert a string to a date
msg = appendToMessage("Born: " & DateValue("26-Feb-1980"))

' Get the number of seconds since 12:00AM
msg = appendToMessage("Number of seconds since midnight: " & Timer)

MsgBox msg
