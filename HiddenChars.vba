' Put this code into your MS Word profile and run either the FillChars
' or the FillWords sub to cover some of your text for practicing in
' speed reading.

' Format text by hiding some chars in the beginning and the end of string
Sub FillChars()
    Preformat 15
    FillFirstChars 5, 15
    FillLastChars 5, 15
End Sub

' Hide the first and last words of all strings
Sub FillWords()
    Preformat 13
    FillFirstWord
    FillLastWord
End Sub

' Fill characters at the beginning of a string
Sub FillFirstChars(CharLim As Long, EndLim As Long)
    Dim oPage As Page
    Dim oRect As Rectangle
    Dim i As Long
    Dim j As Long
    Dim m As Integer
    Dim ChrVal As Byte
    
    For Each oPage In ActiveDocument.ActiveWindow.ActivePane.Pages
        For Each oRect In oPage.Rectangles
            For i = 1 To oRect.Lines.Count
                m = 0
                For j = 1 To oRect.Lines(i).Range.Characters.Count
                    ChrVal = Asc(oRect.Lines(i).Range.Characters(j))
                    If TestCharacter(ChrVal) Then m = m + 1
                    If m = CharLim Then Exit For
                Next j
                If m = CharLim And (oRect.Lines(i).Range.Characters.Count > EndLim) Then
                    ActiveDocument.Range(oRect.Lines(i).Range.Characters(1).Start, _
                        oRect.Lines(i).Range.Characters(j).End).HighlightColorIndex = 1
                End If
            Next i
        Next oRect
    Next oPage
End Sub

' Fill chars at the end of a string
Sub FillLastChars(CharLim As Long, EndLim As Long)
    Dim oPage As Page
    Dim oRect As Rectangle
    Dim i As Long
    Dim j As Long
    Dim m As Integer
    Dim ChrVal As Byte
    
    For Each oPage In ActiveDocument.ActiveWindow.ActivePane.Pages
        For Each oRect In oPage.Rectangles
            For i = 1 To oRect.Lines.Count
                m = 0
                For j = oRect.Lines(i).Range.Characters.Count To 1 Step -1
                    ChrVal = Asc(oRect.Lines(i).Range.Characters(j))
                    If TestCharacter(ChrVal) Then m = m + 1
                    If m = CharLim Then Exit For
                Next j
                If m = CharLim And (oRect.Lines(i).Range.Characters.Count > EndLim) Then
                    ActiveDocument.Range(oRect.Lines(i).Range.Characters(j).Start, _
                        oRect.Lines(i).Range.Characters(oRect.Lines(i).Range.Characters.Count).End) _
                        .HighlightColorIndex = 1
                End If
            Next i
        Next oRect
    Next oPage
End Sub

' Fill the first full word of the string (and those preceding, which length < 2)
Private Sub FillFirstWord()
    Dim oPage As Page
    Dim oRect As Rectangle
    Dim oWord As Range
    Dim i As Long
    Dim j As Long
    
    For Each oPage In ActiveDocument.ActiveWindow.ActivePane.Pages
        For Each oRect In oPage.Rectangles
            For i = 1 To oRect.Lines.Count
                If oRect.Lines(i).Range.Words.Count > 6 Then
                    If oRect.Lines(i).Range.Words(1).Characters.Count > 2 Then
                        Set oWord = oRect.Lines(i).Range.Words.First
                    Else
                        For j = 1 To oRect.Lines(i).Range.Words.Count - 4
                            Set oWord = oRect.Lines(i).Range.Words(2)
                            If oWord.Characters.Count > 2 Then Exit For
                        Next
                    End If
                    ActiveDocument.Range(oRect.Lines(i).Range.Characters(1).Start, _
                       oWord.End).HighlightColorIndex = 1
                End If
            Next i
        Next oRect
    Next oPage
End Sub

' Fill the last full word of the string (and those preceding, which length < 2)
Private Sub FillLastWord()
    Dim oPage As Page
    Dim oRect As Rectangle
    Dim oWord As Range
    Dim i As Long
    Dim j As Long
    
    For Each oPage In ActiveDocument.ActiveWindow.ActivePane.Pages
        For Each oRect In oPage.Rectangles
                For i = 1 To oRect.Lines.Count
                    If oRect.Lines(i).Range.Words.Count > 6 Then
                        If oRect.Lines(i).Range.Words.Last.Characters.Count > 2 Then
                            Set oWord = oRect.Lines(i).Range.Words.Last
                        Else
                            For j = oRect.Lines(i).Range.Words.Count To 4 Step -1
                                Set oWord = oRect.Lines(i).Range.Words(j)
                                If oWord.Characters.Count > 2 Then Exit For
                            Next
                        End If
                        ActiveDocument.Range(oWord.Start, _
                            oRect.Lines(i).Range.Characters(oRect.Lines(i).Range.Characters.Count) _
                            .End).HighlightColorIndex = 1
                    End If
                Next i
        Next oRect
    Next oPage
End Sub

' Format a document's text style
Private Function Preformat(Size As Long)
    ActiveDocument.Select
    Selection.WholeStory
    Selection.Font.Size = Size
    Selection.Font.Name = "Calibri"
    Selection.Font.ColorIndex = 1
    Selection.Range.HighlightColorIndex = 0
End Function


' Check the symbol's code for being a Russian or English letter
Private Function TestCharacter(Char As Byte)
    If (Char >= 192 And Char <= 255) Or (Char >= 65 And Char <= 122) Then
        TestCharacter = True
    Else
        TestCharacter = False
    End If
End Function
