# Editor Interface Functionality

## User Input 

When the program starts running, three inputs are asked to be given by the user:
1. 'Name of the target' : Enter the common name of the object you want to hop to (if any) or hit enter 
2. 'RA/DEC of the target': Enter the J2000 RA/DEC coordinates of the object you want to hop to in this format and will appear as a yellow mark in the plot. Example: '200/20'. Default value is 0/0
3. 'Limiting Magnitude' : Enter the maximum 'V' band AB apparent magnitude of the objects visible in the plot. Should be a positive integer. Keeping only the bright stars help in creating a sensible hopping sequence. Default is 25.

## Hopping and Plot

Once all inputs are given, the final plot will launch in a new browser window. Your entered target will appear as a yellow '+' mark. CLusters, Messier objects and stars are represented with different markers. Cursor hovering on the objects will show their RA/DEC/Contellation tags. 
The plot has following features:

1. Controls
* Home View
* Pan zoom
* Zoom-to-rectangle

2. Buttons
* Save Hops
* Undo
* Clear All

3. On-screen updates
* Deleted Hop
* Last Hop
* Hop list 


