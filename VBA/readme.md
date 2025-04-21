# Visual Basic for Applications (VBA)

## Introduction

- Notes from "Excel VBA Programming for Dummies" - Alexander, M.; Walkenbach, J.
- Object orientated Microsoft programming language
- Not case sensitive
- Line continuation with `_`
- Call another subroutine with `Call <name>` (`Call` is optional)
- Object hierarchy:
  - Excel (called Application)
  - Workbook and Add-In objects, e.g. `Application.Workbooks("Book1.xlsx")`
  - Worksheet objects, e.g. `Application.Workbooks("Book1.xlsx").Worksheets("Sheet1")`
  - Range objects, e.g. `Worksheets("Sheet1").Range("A1")`
- If specific references are omitted, e.g. `Application.Workbooks()`, then the **active** object is used
- Objects of the same type form a **Collection**
  - `Workbooks` -- all currently open Workbooks
  - `Worksheets` -- all worksheets in a given Workbook
  - `Charts` -- all Chart objects in a given Workbook
  - `Sheets` -- all sheets in a given Workbook (worksheets, chart sheets)
- Objects have properties, e.g. `Worksheets("Sheet1").Range("A1").Value`
- Objects have methods, `Worksheets("Sheet1").Range("A1").ClearContents`
- Named arguments can be used, `<name> := <value>`,
  - e.g. - `Range("A1").Copy Destination:=Range("B1")`
- Objects respond to **events**

## Modify Excel

- To turn off screen updating (for speed): `Application.ScreenUpdating = False`
- To turn off automatic recalculation: `Application.Calculation = xlCalculationManual` (or use `xlCalculationAutomatic`)
- To turn off alerts: `Application.DisplayAlerts = False` (Excel executes the default operation)
- Use `With <object> ... End With` for speed and code compactness

### Visual Basic Editor (VBE)

- To enable Developer Tools:
  - right-click on the Ribbon
  - click 'Customize the Ribbon...'
  - on the right-hand side click 'Developer'
- VBE is an application for writing VBA macros
- Press F5 when the cursor is inside a subroutine to run it
- Ctrl+space to see potential variables, methods and properties
- Ctrl+Break to interrupt execution
- `Debug.Print` to print values to the Immediate Window, e.g.
  - `Debug.Print cell, number, i` -- comma-separated
- `Stop` -- forces Break mode
- `Print <expression>` -- displays values in the Immediate Window
  - `? <expression>` -- quicker to type

## Macros

- Macro = set of instructions to imitate keystrokes and mouse actions
- Macro can be assigned to buttons and shapes
- Macros can be added to the ribbon

### Record a macro

- Ensure the 'Developer' tab is visible
- Click 'Record Macro' on the Developer tab
- Perform actions on the worksheet
- Click 'Stop Recording' on the Developer tab
- View the macro by clicking 'Macros' and editing 'Macro1'
- Click on a property and press F1 to see online help

### Add a macro to a form control or shape

- Add to a form control:
  - Insert --> Form controls
  - Select control, e.g. a button
  - Right-click -> Edit Text
  - Right-click -> Assign Macro...
- Add to a shape:
  - Insert -> Button
  - Draw the shape of the button
  - Set the macro to run

## Language

### Comments

- Start with a `'`
- `REM <comment>`

### Data types

- VBA isn't strictly typed
- `Option Explicit` -- all variables must be declared
- `Dim <name> As <type>` to declare a variable
- Types:
  - `Byte` -- 0 to 255
  - `Boolean` -- True or False
  - `Integer`
  - `Long`
  - `Single`
  - `Double`
  - `Currency`
  - `Date`, e.g. `Dim MyDate As Date: MyDate = #2/26/1980##` must be in US format
  - Time as a `Date`, e.g. `Dim Noon As Date: Noon = #12:00:00 PM#`
  - `String`, e.g. `Dim MyString As String * 50` -- fixed length string of 50 chars
  - Variable length string, e.g. `Dim MyString As String`
  - `Variant` -- varies, default type, automatic conversion, reduced speed
- Variable scope:
  - module-only -- declare before the first Sub or Function
  - `Static` -- variable keeps its value between procedure calls
  - `Public` -- available to all VBA modules in a Workbook
  - `Private`
  - `Const` to define a constant, e.g. `Const Rate = 0.725`

### Operators

- `=`, `<>`
- `+`, `-`, `/`, `*`, `^`
- `&` for String concatenation
- `Mod` for modulo arithmetic
- `Not`, `And`, `Or`, `Xor`
- `Eqv` -- equivalence
- `Imp` -- implication

### Goto

- `GoTo` statement
- labels are defined as `<label name>:`
- be sure to use `Exit Sub` before the label
- use for trapping errors

### Conditionals

- `If` ... `Then` ... `Elseif` ... `Else` ... `End If`
- One liner: `If Time < 0.5 Then MsgBox "Good Morning" Else MsgBox "Afternoon!"`
- Equality is `=`, not double

```vb
Sub GreetMe()
    If Time < 0.5 Then
        MsgBox "Good morning!"
    Elseif Time < 0.75 Then
        MsgBox "Good afternoon!"
    Else:
        MsgBox "Evening!"
    End If
End Sub
```

- `Select Case`
  - useful for decisions involving 3 or more options
  - structure is exited when VBA finds a true case
  - use `To`: `Case 0 To 24: Discount = 0.1`

```vb
Sub ShowDiscount()
    Dim Quantity As Long
    Dim Discount As Double

    Quantity = InputBox("Enter quantity:")

    Select Case Quantity
        Case 0 To 24
            Discount = 0.1
        Case 25 To 49
            Discount = 0.2
        Case Is >= 50
            Discount = 0.3
    End Select
    MsgBox "Discount: " & Discount
End Sub
```

### Loops

- `For <initialisation> To <condition> Step <value>` ... `Next <variable>`
- `Exit For` to terminate loop (like break)

```vb
Function RandomColourValue()
    RandomColourValue = Int(256 * Rnd)
End Function

Sub ColourCells()
    Dim i As Long
    Dim j As Long

    For i = 1 To 10
        For j = 1 To 10
            Cells(i, j).Interior.Color = RGB(RandomColourValue(), _
                RandomColourValue(), RandomColourValue())
        Next j
    Next i
End Sub
```

- `Do While <condition>` ... `Loop`
  - Executes while the condition is True
- `Do Until` ... `Loop`
  - executes until the condition is True
- `For Each <variable> In <collection>` ... `Next <variable>`
  - loop through each object in a collection, e.g. worksheets

### Subroutine procedures

- Do not return a value
- Can pass parameters
- `Sub <name>` ... `End Sub`
- Call the sub routine just using its name

```vb
Sub AddEmUp()
    Dim Sum As Integer
    Sum = 1 + 1
    Debug.Print Sum
End Sub

Sub Macro()
    AddEmUp
End Sub
```

```vb
' Get the value in a cell
Sub GetValueInA1()
    Debug.Print Worksheets(1).Range("A1").Value
End Sub
```

### Functions

- Three types:
  - built-in functions to VBA
  - provided by Excel
  - custom function
- `Function <name>` ... `End Function`
- Don't need parentheses
- Returns a single value
- Assign return value to a variable with the same name of the function
- Specify the return type with `As <type>`
- A function can be used in a Worksheet formula (appears in the context window)

```vb
Function AddTwo(arg1, arg2) As Double
	AddTwo = arg1 + arg2
End Function
```

#### Built-in type functions

- `IsArray`
- `IsDate`
- `IsEmpty`
- `IsNull` -- no valid data
- `IsNumeric`
- `TypeName()` -- return the type of the selection with `TypeName(Selection)`

#### Built-in Date functions

- `Date`
- `DateAdd`
- `DateDiff` -- difference between two dates, e.g. `DateDiff("yyyy", d1, d2)`
- `DatePart` -- date part, e.g. `DatePart("yyyy", Date)`
- `DateSerial` -- date to a serial number from year, month, day
- `DateValue` -- convert a String to a date, e.g. `DateValue("26/02/1980")`
- `Day` -- get the day of the month from a Date
- `Hour`
- `Minute`
- `Month` -- get the month number from a Date (2 for February)
- `Now` -- get the system date and time
- `Second`
- `Time` - get the system time
- `Timer` -- number of seconds since midnight
- `TimeSerial` -- get a time from hour, minute, second
- `TimeValue` -- convert a String representation of a time to a time
- `WeekDay` -- number representing the day of the week
- `Year` -- get the year from a Date

```vb
Sub ShowTime()
    Dim now, nowTime As Date
    now = Date
    nowTime = Time

    Debug.Print Day(now) & " / " & Month(now) & " / " & Year(now)
    Debug.Print Hour(nowTime) & " : "; Minute(nowTime) & " : " & Second(nowTime)
End Sub
```

#### Built-in Mathematical functions

- `Abs` -- absolute value
- `Exp`
- `Fix` -- integer portion
- `Rnd` -- random number between 0 and 1
- `Sqr` -- square root

#### Built-in String functions

- `Left` -- specified number of characters from the left of a String
- `Len` -- returns the length of a String
- `LCase` -- lower-case version
- `Mid` -- specified number of characters given a start and end position
- `Replace` -- replace a String in a String
- `Right` -- specified number of characters from the right of a String
- `Space` -- string with required number of spaces
- `Split` -- split a string using a delimiter
- `String` -- return a repeated character
- `Trim` -- remove leading and trailing spaces
- `UCase` -- upper-case version
- `Val` -- get the numbers in a String

#### Built-in File functions

- `CurDir` -- current directory
- `FileLen()` -- filesize
- `Shell` -- executes another program (returns the task ID)

#### Built-in Colour functions

- `RGB`

### Message box

- `MsgBox(<prompt>, <buttons>, <title>)`
- `<prompt>` -- String to display
- `<buttons>` -- type of button (use a `+` to combine)
  - Buttons to be displayed:
    - `vbOKOnly`
    - `vbOKCancel`
    - `vbAbortRetryIgnore`
    - `vbYesNoCancel`
    - `vbYesNo`
    - `vbRetryCancel`
  - Style:
    - `vbCritical`
    - `vbQuestion`
    - `vbExclamation`
    - `vbInformation`
  - Default button:
    - `vbDefaultButton1`
    - `vbDefaultButton2`
    - `vbDefaultButton3`
    - `vbDefaultButton4`
  - Modality:
    - `vbApplicationModal`
    - `vbSystemModal`
- `<title>` -- title bar String
- Returns the button the user clicked
  - `vbOK`
  - `vbCancel`
  - `vbAbort`
  - `vbRetry`
  - `vbIgnore`
  - `vbYes`
  - `vbNo`

### Dialog Boxes

- `InputBox("<message>")` -- asks for a value with parameters:
  - prompt -- text displayed
  - title -- title bar text
  - default -- default value

```vb
Dim result
result = InputBox("Enter a number", "Input", 0)
Debug.Print result
```

- `Application.InputBox`
  - can prompt for a range
  - type 8 is a range

```vb
' Get a range from the user
Sub GetRange()
    Dim Rng As Range
    On Error Resume Next
    Set Rng = Application.InputBox(prompt:="Specify range", Type:=8)
    If Rng Is Nothing Then Exit Sub
    Debug.Print Rng.Address
End Sub
```

### Arrays

- lower index is assumed to be zero, unless otherwise specified - `Dim MyArray(1 To 100) As Integer`
- multidimensional array: `Dim MyArray(1 to 9, 1 to 9) As Integer`
- `MyArray (3,5) = 125` assigns a value to a single element
- dynamic array: - `Dim MyArray() As Integer`
- can't use a dynamic array without `ReDim` - e.g. `ReDim Preserve MyArray (1 to NumElements)`
- `LBound` -- lowest array index
- `UBound` -- largest array index

```vb
Sub ArrayExample()
    Dim MyArray(0 To 4) As Integer
    MyArray(0) = 100
    MyArray(4) = 400
    Debug.Print "Lowest array index: " & LBound(MyArray) ' 0
    Debug.Print "Highest array index: " & UBound(MyArray) ' 4
    Debug.Print IsArray(MyArray) ' True
End Sub
```

### Class modules

- Class module is the VBA equivalent of a class
- Right-click in the VBE -> Insert -> Class Module
- Change the name of the class using its properties
- Parts of a class module:
  - Methods
  - Member variables
  - Properties -- types of functions/subs that behave like variables
  - Events -- subs that are triggered by an event
- Destructor: `Private Sub Class_Terminate()`

```vb
' Example of a class module
Option Explicit

' Member variable
Private dblTotal As Double

' Properties
Property Get Total() As Double  ' Getter
    Total = dblTotal
End Property

Property Let Total(value As Double)  ' Setter
    dblTotal = value
End Property

' Event
Private Sub Class_Initialize()
    dblTotal = 100
End Sub

' Methods
Public Sub Add(value As Double)
    dblTotal = dblTotal + value
End Sub

Public Sub ShowDebug()
    Debug.Print "Total: " & Me.dblTotal
End Sub
```

to use the class module:

```vb
Dim dataItem As New clsDataItem
dataItem.ShowDebug    ' Total: 100

dataItem.Add 100      ' Calling Add() method
dataItem.ShowDebug    ' Total: 200

dataItem.Total = 500  ' Use the setter
dataItem.ShowDebug    ' Total: 500
```

### Collection

- Methods:
  - `Add()`
  - `Count()`
  - `Item()`
  - `Remove()`

```vb
Sub CollectionExample()
  Dim col1 As New Collection

  col1.Add "Item 1"
  Debug.Print col1.Count()  ' 1
  Debug.Print col1.Item(1)  ' Item 1

  col1.Add "Item 2"
  Debug.Print col1.Count()  ' 2
  Debug.Print col1.Item(1)  ' Item 1
  Debug.Print col1.Item(2)  ' Item 2

  col1.Remove (1)
  Debug.Print col1.Count()  ' 1
  Debug.Print col1.Item(1)  ' Item 2
End Sub
```

## Excel

### Worksheet functions

- Most of Excel's worksheet functions can be used in VBA
- Can't use those that have an equivalent VBA function, e.g. `Rnd`
- Worksheet functions available through the `WorksheetFunction` object
  - `Application.WorksheetFunction.Sum(Range("A1:A3"))`
- Functions:
  - `Large` -- get the k(th)-largest value
  - `Max` -- get the maximum value in a Range
  - `Min` -- get the minimum value in a Range
  - `Small` -- get the k(th)-smallest value
  - `Sum` -- sum the values in a Range
  - `VLookup` -- get a value from a lookup table

```vb
Sub GetPrice()
    ' Perform a VLookup -- use Application.VLookup to handle missing values
    Dim PartNum As Variant
    Dim Price As Variant
    PartNum = InputBox("Enter part number")
    Price = Application.VLookup(PartNum, Range("A1:B4"), 2, False)
    If IsError(Price) Then
        MsgBox "Unknown part number " & PartNum
    Else
        MsgBox "Price of " & PartNum & " is " & Price
    End If
End Sub
```

### Range

- name a Range using Formulas --> Defined Names --> Define Name
- single cell, e.g. `Range("A1")`
- range of cells, e.g. `Range("A1:C3")`
- entire row, e.g. `Range("3:3")`
- entire column, e.g. `Range("A:A")`
- non-contiguous range, e.g. `Range("B2:C6,A10:B12")`
- properties: -
  - `Address` -- cell address as an absolute reference
  - `Clear` -- deletes the contents, plus all cell formatting
  - `ClearContents` -- clear contents, but leave formatting intact
  - `ClearFormats` -- deletes the formatting, but not the cell contents
  - `Column` -- column index
  - `Count` -- number of cells in range
  - `CurrentRegion` -- cells around a particular cell
  - `Delete` -- delete
  - `Font` -- returns a Font object
  - `Formula` -- read-write property
  - `Interior` -- set background colour
  - `HasFormula` -- returns True if a single cell contains a formula
  - `NumberFormat` -- read/set the number format
  - `Row` -- row index
  - `Select` -- select a range
  - `Text` -- string representation of the text in a cell
  - `Value` -- value contained in a single cell (default, read-write)
- methods:
  - `ClearContents` -- erase the contents of the cells
  - `Copy` -- copy the contents to another `Range`
  - `Cells` property takes a row and column index, e.g. `Cells(2,3)` refers to C2
- `TypeName(Selection)` -- get the selection type
- `Selection.Areas.Count` -- total number of areas (for multiple selection)

```vb
' Draw a compass relative to the current cell
Sub DrawCompass()
    ActiveCell.Offset(-1, 0) = "North"
    ActiveCell.Offset(0, 1) = "East"
    ActiveCell.Offset(1, 0) = "South"
    ActiveCell.Offset(0, -1) = "West"
End Sub
```

```vb
' Highlight a cell by changing its background colour to yellow
Sub HighlightCell()
    Range("A1").Interior.Color = vbYellow
End Sub
```

```vb
' Insert a formula into cell A12
Sub SumPreviousColumns()
    Range("A12").Formula = "=SUM(A1:A11)"
End Sub
```

```vb
' Copy the contents of cells A1:A4 into C1:C4
Sub CopyContents()
    Range("A1:A4").Select
    Selection.Copy
    Range("C1").Select
    ActiveSheet.Paste
End Sub
```

- Copy a range `Range("A1:A5").Copy Destination:=Range("B1")`
- Cut-and-paste `Range("A1:A5").Cut Range("A10")`
- Select to the end of a row `Range(ActiveCell, ActiveCell.End(xlDown)).Select`
- Select a column `ActiveCell.EntireColumn.Select`
- Select a row `ActiveCell.EntireRow.Select`
- To loop through cells: `For Each cell in Selection ... Next cell`

### Automatic procedures and events

- Macros must be enabled for the event-handler procedures to work
- Always `Sub` procedures -- not functions
- Double-click the event in the VBE to get a procedure stubs
- Workbook events:
  - Activate -- workbook is activated
  - BeforeClose
  - BeforePrint
  - BeforeSave
  - Deactivate
  - NewSheet -- a new sheet is added to the workbook
  - Open -- the workbook is opened, used to:
    - Display a welcome message
    - Open other workbooks
    - Activate a particular worksheet
    - Set up custom shortcut menus
  - SheetActivate -- sheet is activated
  - SheetBeforeDoubleClick -- cell is double-clicked
  - SheetBeforeRightClick -- cell is right-clicked
  - SheetChange -- change is made to a cell in the workbook
  - SheetDeactivate -- sheet is deactivated
  - SheetSelectionChange -- selection is changed
  - WindowActivate -- workbook window is activated
  - WindowDeactivate -- workbook window is deactivated
- Worksheet events:
  - Activate -- worksheet is activated
  - BeforeDoubleClick -- cell in worksheet is double-clicked
    - set `Cancel = True` so that the default double-click action doesn't occur
  - BeforeRightClick -- cell in worksheet is right-clicked
  - Change -- change is made to any cell
  - Deactivate -- worksheet is deactivated
  - SelectionChange -- selection is changed
- OnTime event -- occurs at a particular time of day

```vb
' Must be in the code module for the worksheet
' Responds to a worksheet change event
Private Sub Worksheet_Change(ByVal Target As Range)
    If Target.Column = 1 Then
        Target.Offset(0, 1) = Now
    End If
End Sub
```

### Error handling techniques

- When an error occurs, Excel stores the details in an `Err` object
  - `Err.Number` -- error number
  - `Err.Description` -- error description
- `On Error GoTo <label>` traps errors and resumes at label
- `On Error GoTo 0`
- `On Error Resume Next` -- ignores all errors and resumes execution
- Ensure that 'Break on all errors' is deselected

```vb
Sub EnterSquareRoot()
    Dim Num As Variant
    Dim Msg As String

    ' Set up the error handling
    On Error GoTo BadEntry
    ' Prompt for a value
    Num = InputBox("Enter a value")
    ' Exit if cancelled
    If Num = "" Then Exit Sub
    ' Insert the square root
    ActiveCell.Value = Sqr(Num)
    ' Need to exit to stop execution continuing to BadEntry
    Exit Sub

BadEntry:
    Msg = "An error occurred." & vbNewLine & "Try again"
    MsgBox Msg, vbCritical
End Sub
```

- Resume statements to recover from an error
- `Resume` -- execution resumes with the statement that caused the error
- `Resume Next` -- execution resumes with the next statement
- `Resume <label>` -- execution resumes at the label (doesn't work with `GoTo`)

```vb
Sub SelectionSqrt()
    Dim cell As Range
    If TypeName(Selection) <> "Range" Then Exit Sub
    ' Just ignore any cells that can't be square rooted
    On Error Resume Next
    For Each cell In Selection
        cell.Value = Sqr(cell.Value)
    Next cell
End Sub
```

### Charts

```vb
Sub CreateChart()
    ' Programmatically create a chart
    Dim NewShape As Shape
    Dim NewChart As Chart

    Set NewShape = ActiveSheet.Shapes.AddChart2(XlChartType:=xlColumnClustered)
    Set NewChart = NewShape.Chart

    With NewChart
        .SetSourceData Source:=Range("A1:A20")
        .SetElement (msoElementLegendRight)
        .SetElement (msoElementChartTitleAboveChart)
        .ChartTitle.Text = "Random data"
    End With

    ' Indices start at 1
    NewChart.SeriesCollection(1).Interior.Color = RGB(255, 0, 0)

End Sub
```

- `GetOpenFilename`
  - displays the Open dialog box
  - returns the filename as a String
  - returns False if Cancel was pressed

```vb
Sub GetImportFileName()
    Dim Finfo As String
    Dim FilterIndex As Long
    Dim FileName As Variant

    ' Set up a list of file filters
    Finfo = "Text files (*.txt),*.txt,Excel macros,*.xlsm,All files (*.*),*.*"

    ' Display all files by default
    FilterIndex = 3

    ' Get the filename from the user
    FileName = Application.GetOpenFilename(Finfo, FilterIndex, "Select a file")

    ' Handle the return info from the dialog box
    If FileName = False Then
        MsgBox "No file was selected (you may have pressed Cancel)"
    Else
        MsgBox "You selected " & FileName
    End If
End Sub
```

- `GetSaveAsFilename`

  - displays the 'Save As' dialog box
  - gets a path and filename from the user

- `FileDialog`
  - just get a folder name

```vb
Sub GetAFolder()
    With Application.FileDialog(msoFileDialogFolderPicker)
        .InitialFileName = Application.DefaultFilePath & "\"
        .Title = "Please select a location for the backup"
        .Show
        If .SelectedItems.Count = 0 Then
            MsgBox "Cancelled"
        Else
            MsgBox .SelectedItems(1)
        End If
    End With
End Sub
```

### UserForm

- GUI to get information from the user
- Used to obtain more information than just a InputBox
- Open VBE --> Select relevant Workbook --> Click Insert --> UserForm
- To see the Toolbox: View --> Toolbox
- Toolbox controls:
  - Label -- display text
  - TextBox -- text entry area
  - ComboBox -- drop-down list
  - CheckBox -- on/off or yes/no
  - OptionButton -- select one of several options
  - ToggleButton -- on/off button
  - Frame -- contains other controls
  - CommandButton -- clickable button
  - TabStrip -- tabs
  - Multipage -- tabbed container
  - ScrollBar -- drag a bar to provide a setting
  - SpinButton -- click a button to change a value
  - Image -- holds an image
  - RefEdit -- allows a user to select a range
- Each UserForm has a Code module that holds the event-handler procedures
- Right-click on the UserForm to select 'View Code' or 'View Object'
- `UserForm1.Show` to show the UserForm (must be in a sheet or workbook macro)
- `Unload UserForm1` closes the UserForm
- If writing code in a UserForm's Code, `UserForm1.CheckBox1.Value = True` can be simplified to `CheckBox1.Value = True`
- Press F5 to see the UserForm
- Double-click control to set event handler
- Properties:
  - Accelerator -- determines underlined letter (Alt+key)
  - AutoSize -- control resizes based on caption
  - BackColor -- background colour
  - BackStyle -- transparent or opaque
  - Caption -- text
  - Cancel -- set to True for Esc
  - Default -- set to True for Enter
  - Height
  - Left -- position
  - Name -- name of the control (to refer to it in code)
  - Picture -- graphics image to display
  - Top -- position
  - Value -- control's value
  - Visible -- visible?
  - Width

## Word

- Open the Visual Basic Editor (VBE) with Alt+F11
- To edit a template (.dotm file) as double-clicking the file will create a new file:
  - Open MS Word
  - Open the template file

### DocVariable

- To create a DocVariable: Insert -> Quick Parts -> Field...
- To toggle fields between results and code: ALT+F9

```vb
' Show the field codes in the document
Sub ShowFieldCodes()
    Dim fieldLoop As Field
    Debug.Print "Field codes:"
    For Each fieldLoop In ActiveDocument.Fields
        Debug.Print fieldLoop.Code
    Next fieldLoop
End Sub
```

```vb
' Show the name and value of each variable
Sub ShowVariables()
    Dim myVar
    For Each myVar In ActiveDocument.Variables
        Debug.Print "Name = '" & myVar.Name & "', Value: " & myVar.Value
    Next myVar
End Sub
```

```vb
' Update a variable
Sub UpdateVariable()
  Dim oVars As Word.Variables
  Set oVars = ActiveDocument.Variables
  oVars("varName").Value = "Hi, Chris"

  Debug.Print ActiveDocument.Fields.Update
End Sub
```

### Bookmarks

- To add a bookmark: Insert -> Bookmark (flag icon)
- To show bookmarks:
  - File -> Options -> Advanced
  - Under 'Show document content' select 'Show bookmarks' and click OK

```vb
' Check if a bookmark exists
If ActiveDocument.Bookmarks.Exists(strSightingsBookmark) = False Then
  Dim result
  result = MsgBox("Sightings bookmark not found. Unable to auto-populate.", _
      vbOKOnly + vbCritical)
  Exit Sub
End If
```
