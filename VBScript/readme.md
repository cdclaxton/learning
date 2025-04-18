# VBScript

## Introduction

- Microsoft scripting language (Active Scripting language, formerly known as ActiveX Scripting, in Windows to implement component-based scripting support).

- Light-weight version of Visual Basic

- Uses the Component Object Model (COM) to access elements of the environment in which it is running, e.g. FileSystemObject (FSO) to create, read, update and delete files.

- Uses:
  - Widely used amongst system administrators in Microsoft environments
  - Scripting language for Quick Test Professional (a test automation tool)
  - Internal scripting language for some embedded applications, such as industrial operator and human machine interfaces
  - Automating day-to-day office tasks
  - Monitoring Windows-based environments
  - Client-side web development in Internet Explorer (similar to JavaScript), but not supported in Firefox or Opera (or IE Edge now)
  - Server-side processing of web pages with Microsoft Active Server Pages (ASP)
  - Create applications that run on Windows, e.g. a `.vbs` script that uses the Windows Script Host (WSH) environment. Script can be invoked with `Wscript.exe` (GUI) or `Cscript.exe` (command-line environment).
  - Windows Script File (WSF) can include multiple VBS files (help with code reuse)
  - HTML Application (HTA) -- HTML within the file is used to generate the UI and VBscript can be used for the program logic (executed with mshta.exe)

## In Web Browsers

- Code is inserted between:

```html
<script type="text/vbscript">
  ...
</script>
```

- To hide VBScript from browsers that don't support scripting, enclose the statements between HTML comments,

```html
<!-- ... -->
```

- Only single-line comments are allowed, e.g. `' This is a comment`

- A new line denotes the end of a statement, hence no semicolons

- To split a long statement onto multiple lines, use an `_` at the end of each line except the last

- String concatenation with the `&` symbol

- VBScript is not case-sensitive, i.e. `myVar` and `myvar` refer to the same variable

- To write Hello World in a web browser that supports VBScript:

```html
<html>
  <head>
    <title>Hello World!</title>
    <script type="text/vbscript">
      Sub sayHello()
          document.write("Hello world!\n")
      End Sub
    </script>
  </head>
  <body onload="sayHello()"></body>
</html>
```

## Stand-alone Windows application

To write Hello World, create a file called `hello_world.vbs` and insert:

```vbs
MsgBox Hello World
```

## Variables

- Variables must begin with a letter and cannot contain a dot (`.`)

- All variables are of type `variant`, which can store different types of data

- To prevent the script from automatically creating new variables if they are misspelled versions of variables, use the `Option Explicit` statement, which forces variables to be declared with the `dim`, `public` or `private` statement.

- To declare a variable `x` with the value 3:

```vbs
Dim x = 3
```

- Example:

```vbs
Dim name
name = "Chris"
MsgBox("Hello " & name)
```

- Arrays: Declare an array with 3 elements:

```vbs
Dim names(2), namesToShow
names(0) = "Chris"
names(1) = "David"
names(2) = "George"
For i = 0 To 2
    namesToShow = namesToShow & names(i) & " "
Next
MsgBox namesToShow
```

- Multi-dimensional array (2D):

```vbs
Dim table(4,3), multiplicationTable
For row = 0 To 4
    For col = 0 To 3
        multiplicationTable = multiplicationTable & ((row+1) * (col+1)) & vbNewLine
    Next
    multiplicationTable = multiplicationTable & "\n"
Next
MsgBox multiplicationTable
```

## Conditional Statements

- Comparison operators: `=`, `>`, `<`, `>=`, `<=`, `<>`

- Logic operators: `Not`, `Or`, `And`

- `If` ... `ElseIf` ... `Else` ... `End If`

- To execute only one statement when a condition is true:

```vbs
If i=10 Then c=20
```

- To execute multiple statements when a condition is true:

```vbs
If i=10 Then
    c = 20
    d = 4
End If
```

- The `Select` statement can be used to check for equality:

```vbs
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
```

## Looping

- There are four looping statements in VBScript:

  - `For` ... `Next`
  - `For Each` ... `Next` (repeats a block of code for each item in a collection or array)
  - `Do` ... `Loop`
    - `Do While <test>` ... `Loop`
    - `Do` ... `Loop While <test>`
    - `Do Until <test>` ... `Loop`
    - `Do` ... `Loop Until <test>`
  - `While` ... `Wend`

- Example that prints the square numbers using each type of loop:

```vbs
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
```

- Using the `Step` keyword, the counter variable can be incremented or decremented as required

- To exit a `For` ... `Next` statement, use the `Exit` keyword

- To exit a `Do` ... `Loop` statement, use the `Exit Do` keyword

```vbs
Option Explicit
Dim i, output
For i=1 To 10 Step 3
    output = output & i & " "
Next
MsgBox output
```

## Functions and Procedures

- Sub procedures:
  - statements enclosed in `Sub` and `End Sub`
  - does not return a value
  - can take arguments
  - to call a procedure: `MyProc(args)`

```vbs
Sub SayHello(name)
    MsgBox("Hello " & name)
End Sub

SayHello("George")
```

- Function procedures
  - statements enclosed in `Function` and `End Function`
  - can return a value (assign a value to its name)
  - can take arguments

```vbs
' Program to find the n(th) prime number
' The first prime numbers are: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37

Option Explicit

' Define an assert function to help with some tests
Sub Assert(boolExpr, messageOnFail)
    If Not boolExpr Then
        Err.Raise vbObjectError + 99999, , messageOnFail
    End If
End Sub

' Unit tests for the isPrime() function
Sub testIsPrime()
    Assert Not isPrime(1) , "1 is not prime"
    Assert isPrime(2) , "2 is prime"
    Assert isPrime(3) , "3 is prime"
    Assert Not isPrime(4) , "4 is not prime"
    Assert isPrime(5), "5 is prime"
    Assert Not isPrime(6) , "6 is not prime"
    Assert isPrime(7) , "7 is prime"
    Assert isPrime(11) , "11 is prime"
    Assert isPrime(13) , "13 is prime"
    Assert isPrime(17) , "17 is prime"
End Sub

' Determine if a number is prime
Function isPrime(n)
    Dim x
    If n <= 1 Then
        isPrime = False
        Exit Function
    End If

    For x = 2 To n/2
        If (n Mod x) = 0 Then
            isPrime = False
            Exit Function
        End If
    Next
    isPrime = True
End Function

' Unit tests for the findNthPrimeNumber() function
Sub testFindNthPrimeNumber()
    Assert findNthPrimeNumber(1) = 2, "1st prime number is 2"
    Assert findNthPrimeNumber(2) = 3, "2nd prime number is 3"
    Assert findNthPrimeNumber(3) = 5, "3rd prime number is 5"
    Assert findNthPrimeNumber(4) = 7, "4th prime number is 7"
    Assert findNthPrimeNumber(5) = 11, "5th prime number is 11"
    Assert findNthPrimeNumber(6) = 13, "6th prime number is 13"
    Assert findNthPrimeNumber(7) = 17, "7th prime number is 17"
    Assert findNthPrimeNumber(8) = 19, "8th prime number is 19"
    Assert findNthPrimeNumber(9) = 23, "9th prime number is 23"
End Sub

' Find the n(th) prime number
Function findNthPrimeNumber(n)
    Dim numPrimeNumbersFound, testValue
    numPrimeNumbersFound = 0
    testValue = 1
    Do Until numPrimeNumbersFound = n
        testValue = testValue + 1
        If isPrime(testValue) Then
            numPrimeNumbersFound = numPrimeNumbersFound + 1
            If numPrimeNumbersFound = n Then
                findNthPrimeNumber = testValue
            End If
        End If
    Loop

End Function

' Main script
Dim n
n = 1000

' Check the functions
testIsPrime()
testFindNthPrimeNumber()

MsgBox("The " & n & "th prime number is " & findNthPrimeNumber(n))
```

## Classes

- Declare a class using the `Class` ... `End Class` statement

- Class properties are used to wrap private variables of a class

- `Public <property name>` defines a public property

- `Private <property name>` defines a private property

- `Property Get` returns the value of the property

- `Property Let` sets the value of a property

- Declare a method using the usual `Function` .. `End Function` statements

- `Private Sub Class_Initialize` is the method to initialise an object

- `Private Sub Class_Terminate` is the destructor

- To create an instance of a new class, use the construction:

```vbs
Dim obj
Set obj = New <class name>
```

- Example of a class:

```vbs
Option Explicit

Class User

    ' Declare a private class variable
    Private m_username

    ' Declare a property
    Public Property Get Username
        Username = m_username
    End Property

    ' Set the username
    Public Property Let UserName (strUserName)
        m_username = strUserName
    End Property

    Sub DisplayUsername
        MsgBox(m_username)
    End Sub

End Class

Dim user1
Set user1 = New User
user1.Username = "Dave"
user1.displayUsername()
```

## String functions

- Demonstration of different string functions:

```vbs
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
```

## Date and time functions

- Demonstration of date and time functions:

```vbs
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
```

## File System Object

```vbs
' Create a file with some text in
Option Explicit

Dim objFSO, objFolder, objFile, strDirectory, strFile

' Create the File System Object
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the current directory
Dim currentDirectory
currentDirectory = objFSO.GetAbsolutePathName(".")
Wscript.Echo "Current directory: " & currentDirectory

' Create the folder if it doesn't already exist
Dim strFullPath
strDirectory = "\data\simple_test\"
strFullPath = objFSO.BuildPath(currentDirectory, strDirectory)
If objFSO.FolderExists(strFullPath) Then
	Set objFolder = objFSO.GetFolder(strFullPath)
	Wscript.Echo "Folder already exists: " & strFullPath
Else
	Set objFolder = objFSO.CreateFolder(strFullPath)
	Wscript.Echo "Creating folder: " & strFullPath
End If

' Create the file
Dim strFullPathFile
strFile = "test1.txt"
strFullPathFile = objFSO.BuildPath(strFullPath, strFile)
Set objFile = objFSO.CreateTextFile(strFullPathFile, True)

Wscript.Echo "Just created " & strFullPathFile

' Write to file
objFile.Write "Hello, World!" & vbCrLf
objFile.Close

Set objFolder = nothing
Set objFile = nothing

' Show where the file has been created using Windows Explorer
Dim objShell
If err.number = vbEmpty Then
	Set objShell = CreateObject("WScript.Shell")
	objShell.run("Explorer" & " " & strFullPath)
Else
	WScript.Echo "VBScript error: " & err.number
End If
```

## Registry

```vbs
Option Explicit

Dim objShell, strTemp
Set objShell = WScript.CreateObject("WScript.Shell")

strTemp = "HKEY_CURRENT_USER\Volatile Environment\USERNAME"
WScript.Echo "Logged in user: " & objShell.RegRead(strTemp)

strTemp = "HKEY_CURRENT_USER\Volatile Environment\USERPROFILE"
WScript.Echo "User profile: " & objShell.RegRead(strTemp)
```
