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
n = 100

' Check the functions
testIsPrime()
testFindNthPrimeNumber()

MsgBox("The " & n & "th prime number is " & findNthPrimeNumber(n))
