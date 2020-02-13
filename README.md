**Brainwave Visualization**
===========================
Program that allows the user to visualise brainwaves.

**Installation**
----------------
Install this .zip folder:   *"zip folder here"*
1.  Open the "Executable.exe" file
2.  Open your desired data
3.  Start working!
    
**How to Use**
--------------
Home Page
*  Open button - when clicked opens the file directory and allows the user to pick a project to open
*  Quit button - when clicked closes the application

Main Application Layout
*  Reference graph - the full waveform for the patient displayed above the interactive graph for reference - coloured cyan
*  Toolbar - a set of buttons allowing for navigating the graph and adding annotations
*  Interactive graph - the graph affected by the toolbar - coloured blue

Toolbar (Buttons from left to right)
*  Home button - when clicked resets the interactive graph to its original view before any actions were made
*  Back button - when clicked sets the view to before the users last action (i.e before the user zoomed/panned)
*  Forward button - does not function unless the Back button has been used, if clicked sets the view to before the back buttonw was used
*  Pan button - if clicked allows user to move the waveform while holding the left mouse button and dragging
*  Zoom button - if clicked allows the user to click and drag to form a rectangle which when the mouse button is released adjusts the view to the size of that rectangle (i.e zooming in)
*  Configure button - if clicked creates a pop-up allowing the user to format the size of the interactive graph to their choosing
*  Annotation button - when clicked allows the user to click and drag to form a red rectangle specifying the area of the graph the user would like to annotate
*  Confirm Annotation button - does not function if Annotation button has not been used, when clicked confirms annotation and allows user to input a title and description
*  Open button - if clicked allows the user to open a new project replacing the current window
*  Export button - if clicked allows the user to export the graph they are working on as a PDF
*  Save button - if clicked allows the user to export the graph they are working on as a PNG
*  Open Concurrent button - if clicked allows user to open a new project in a new window if needed for comparison
*  Quit button - if clicked closes the current project and any existing concurrent projects