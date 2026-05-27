' ====================================================================
' Batch-import all .sldcrv files in a folder as "Curve Through XYZ Points"
' features in the active SolidWorks part.
'
' Usage:
'   1. Open / create a Part document in SolidWorks.
'   2. Tools > Macro > New (Ctrl+Shift+M), save as .swp.
'   3. Paste this code into the VBA editor (replace the empty Sub main).
'   4. (Optional) edit DEFAULT_FOLDER below to your section folder.
'   5. Press F5 (or Run).
'
' Each curve feature is renamed to its file name (without .sldcrv extension)
' so they appear in the FeatureManager as sec01_z0.200 ... sec20_z3.500
' (matching the order needed by the loft).
' ====================================================================
Option Explicit

' ---- EDIT THIS to point to your output folder (or leave and pick at runtime) ----
Const DEFAULT_FOLDER As String = _
    "E:\CCBlade\test\S1223_30KW_AFFiles\origin\Futher_Op_com4_sections"

Sub main()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim folderPath As String
    Dim fileName As String
    Dim ok As Boolean
    Dim nOk As Long, nFail As Long
    Dim t0 As Single

    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc
    If swModel Is Nothing Then
        MsgBox "Open a Part document first, then run the macro.", vbExclamation
        Exit Sub
    End If
    If swModel.GetType <> swDocPART Then
        MsgBox "The active document is not a Part.", vbExclamation
        Exit Sub
    End If

    folderPath = PickFolder(DEFAULT_FOLDER)
    If folderPath = "" Then Exit Sub
    If Right(folderPath, 1) <> "\" Then folderPath = folderPath & "\"

    fileName = Dir(folderPath & "*.sldcrv")
    If fileName = "" Then
        MsgBox "No .sldcrv files found in:" & vbCrLf & folderPath, vbExclamation
        Exit Sub
    End If

    t0 = Timer

    Do While fileName <> ""
        ok = swModel.InsertCurveFile(folderPath & fileName)
        If ok Then
            nOk = nOk + 1
            RenameLastFeature swModel, StripExt(fileName)
            Debug.Print "OK   " & fileName
        Else
            nFail = nFail + 1
            Debug.Print "FAIL " & fileName
        End If
        fileName = Dir
    Loop

    swModel.ClearSelection2 True
    swModel.ViewZoomtofit2

    MsgBox "Imported " & nOk & " curve(s)" & _
           IIf(nFail > 0, " (" & nFail & " failed — see Immediate window)", "") & _
           "  in " & Format(Timer - t0, "0.0") & " s.", vbInformation
End Sub

' ---- helpers ------------------------------------------------------

Private Function PickFolder(initial As String) As String
    Dim sh As Object, f As Object
    Set sh = CreateObject("Shell.Application")
    Set f = sh.BrowseForFolder(0, "Select folder containing .sldcrv files", 0, initial)
    If f Is Nothing Then
        PickFolder = ""
    Else
        PickFolder = f.Self.Path
    End If
End Function

Private Function StripExt(s As String) As String
    Dim p As Long
    p = InStrRev(s, ".")
    If p > 0 Then StripExt = Left(s, p - 1) Else StripExt = s
End Function

Private Sub RenameLastFeature(model As SldWorks.ModelDoc2, newName As String)
    Dim feat As SldWorks.feature
    Set feat = model.FeatureByPositionReverse(0)
    If Not feat Is Nothing Then feat.Name = newName
End Sub
