//Sign in automation script

//Main function to execute sign in process
Function Main()
    Dim x, y
    
    //Click sign in button
    If FindAndClick(0, 0, 200, 200, "sign_in_btn") = False Then 
        MessageBox "Cannot find sign in button"
        Exit Function
    End If
    Delay 1000
    
    //Execute grid sign in
    SignInGrids()
    
    //Close window
    FindAndClick(850, 0, 950, 100, "close_btn")
End Function

//Function to find and click image
Function FindAndClick(x1, y1, x2, y2, pic_name)
    Dim x, y
    FindPic x1, y1, x2, y2, "Attachment:"&pic_name&".png", "101010", 0, 0.9, x, y
    
    If x > -1 And y > -1 Then 
        MoveTo x, y
        Delay 300
        LeftClick
        FindAndClick = True
    Else 
        FindAndClick = False
    End If
End Function

//Function to handle grid sign in
Function SignInGrids()
    Dim row, col, currentX, currentY
    
    //Define grid parameters
    startX = 185
    startY = 150
    gridWidth = 115
    gridHeight = 90
    
    //Loop through all grids
    For row = 0 To 3
        For col = 0 To 6
            //Calculate current position
            currentX = startX + (col * gridWidth)
            currentY = startY + (row * gridHeight)
            
            //Check and click reward if available
            If FindAndClick(currentX-20, currentY-20, currentX+20, currentY+20, "reward_box") Then
                Delay 200
                //Click confirm button if any
                FindAndClick(400, 200, 600, 400, "confirm_btn")
            End If
            
            Delay 300
        Next
    Next
End Function

//Start the script
Main 