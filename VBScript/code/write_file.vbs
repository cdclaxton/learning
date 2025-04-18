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
