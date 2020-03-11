**Brainwave Visualization**
===========================
Program that allows the user to visualise brainwaves.

**Installation**
----------------
1.  Install the .zip folder
2.  Extract all the items in the desired location
3.  Run "BrainWave.exe"
4.  Start working!
    
**How to Use**
--------------
Home Page
--------------
*  **Open button** - when clicked opens the file directory and allows the user to pick a project to open
*  **Quit button** - when clicked closes the application

Main Application Layout
--------------
*  **Reference graph** - the full waveform for the patient displayed above the interactive graph for reference - coloured cyan
*  **Toolbar** - a set of buttons allowing for navigating the graph and adding annotations
*  **Interactive graph** - the graph affected by the toolbar - coloured blue
*  **Annotation sidebar** - a sidebar on the right allowing the user to focus in on specific annotations and edit and delete ones made prior

Toolbar (Buttons from left to right)
--------------
*  **Home** - when clicked resets the interactive graph to its original view before any actions were made
*  **Back** - when clicked sets the view to before the users last action (i.e before the user zoomed/panned)
*  **Forward** - does not function unless the Back button has been used, if clicked sets the view to before the back buttonw was used
*  **Pan** - if clicked allows user to move the waveform while holding the left mouse button and dragging
*  **Zoom** - if clicked allows the user to click and drag to form a rectangle which when the mouse button is released adjusts the view to the size of that rectangle (i.e zooming in)
*  **Configure** - if clicked creates a pop-up allowing the user to format the size of the interactive graph to their choosing
*  **Annotation** - when clicked allows the user to click and drag to form a red rectangle specifying the area of the graph the user would like to annotate
*  **Confirm** Annotation - does not function if Annotation button has not been used, when clicked confirms annotation and allows user to input a title and description
*  **Open** - if clicked allows the user to open a new project replacing the current window
*  **Export** - if clicked allows the user to export the graph they are working on as a PDF
*  **Save** - if clicked allows the user to export the graph they are working on as a PNG
*  **Open Concurrent** - if clicked allows user to open a new project in a new window if needed for comparison
*  **Quit** - if clicked closes the current project and any existing concurrent projects

Annotation Sidebar
--------------
*  **Go-To** - when clicked after choosing an annotation sets the view to a close-up of the annotated section of graph
*  **Edit** - when clicked after choosing an annotation allows the user to edit the title and description
*  **Delete** - when clicked after choosing an annotation allows the user to delete an annotation
