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
