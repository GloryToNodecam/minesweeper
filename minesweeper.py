import random, time, copy
#introduces the player
print()
print("Welcome to Minesweeper!")
print("===========================")
print()
def selectDiff():
    sizeList = [5,7,9,11]
    gridSize = int(input("Input the size of grid you wish to play on: 5x5[5] 7x7[7] 9x9[9] 11x11[11]"))
    if gridSize not in sizeList:
        selectDiff()
    else:
        return gridSize


#allows the game to be re-run without restarting the program
def reset(gridSize):
    
    
    #places the bombs in the grid and then updates the spaces surrounding to reflect the number of bombs nearby
    for x in range(0,10):
        placeBomb(gameGrid)
    for yCor in range(0,gridSize):
        for xCor in range(0,gridSize):
            if location(yCor,xCor,gameGrid) == "*":
                updateValues(yCor,xCor,gameGrid)
    printBoard(knownGrid)
    play(gameGrid,knownGrid)
    
    

def setup():
    for x in range(0,20):
        print()
    print("""
Welcome to Minesweeper
======================
""")
    time.sleep(2.5)
    reset()
    
                    

def placeBomb(grid):
    yCor = random.randint(0,8)
    xCor = random.randint(0,8)
    currentRow = grid[yCor]
    if not currentRow[xCor] == "*":
        currentRow[xCor] = "*"
    else:
        placeBomb(grid)


def location(yCor,xCor,grid):
    row = grid[yCor]
    spotValue = row[xCor]
    return spotValue

def updateValues(yCor,xCor,grid):
    #updates values for the row above a given bomb
    #any greater than or less than checks are to ensure that the theoretical value exists within the grid
    if yCor - 1 > -1:
        row = grid[yCor-1]
       
        if xCor-1 > -1:
            if not row[xCor-1] == "*":
                row[xCor-1] += 1
                
        
        if not row[xCor] == "*":
            row[xCor] += 1
    
   
        if xCor+1 < 9:
            if not row[xCor+1] == "*":
                row[xCor+1] += 1
    
    #updates values for the row that the bomb is on
    row = grid[yCor]
       
    if xCor-1 > -1:
        if not row[xCor-1] == "*":
            row[xCor-1] += 1
    
   
    if xCor+1 < 9:
        if not row[xCor+1] == "*":
            row[xCor+1] += 1
    
    
    #updates values for the row below the bomb
    
    if yCor + 1 < 9:
        row = grid[yCor+1]
       
        if xCor-1 > -1:
            if not row[xCor-1] == "*":
                row[xCor-1] += 1
                
        
        if not row[xCor] == "*":
            row[xCor] += 1
    
   
        if xCor+1 < 9:
            if not row[xCor+1] == "*":
                row[xCor+1] += 1

#prints the game grid 
def printBoard(grid):
    #effectivly clears the terminal to create the effect of a constant grid
    for x in range(0,40):
        print() 
    print('    A   B   C   D   E   F   G   H   I   J   K')
    print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
    for yCor in range (0, 9):
        print(yCor,'║',location(yCor,0,grid),'║',location(yCor,1,grid),'║',location(yCor,2,grid),'║',
        location(yCor,3,grid),'║',location(yCor,4,grid),'║',location(yCor,5,grid),'║',location(yCor,6,grid),'║',location(yCor,7,grid),'║',location(yCor,8,grid),'║'
        ,location(yCor,9,grid),'║',location(yCor,10,grid),'║')
    if not yCor == 8:
        print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
    
    print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝')

#the play loop for the game updating the game board and accepting inputs
def play(solutionGrid,knownGrid):
    yCor, xCor  = choose(solutionGrid,knownGrid)
    spotVal = location(yCor,xCor,solutionGrid)
   #if the chosen space is a bomb it ends the game
    if spotVal == "*":
        printBoard(solutionGrid)
        print("You Lose!")
        playAgain = input("Play again? (Y/N): ").lower()
        if playAgain == "y":
            reset()
        else:
            quit()
    
    knownGrid[yCor][xCor] = spotVal
    
    if spotVal == 0:
        checkZeros(knownGrid,solutionGrid,yCor,xCor)
    printBoard(knownGrid)
    squaresLeft = 0
    #checks every spot to count bomb markers and unmarked squares and adds them to a count of squares, when the count reaches 10 without a loss occuring the player has won
    for x in range(0,9):
        row = knownGrid[x]
        squaresLeft += row.count(" ")
        squaresLeft += row.count("⚐")
    #checks to see if all of the bombs have been found
    if squaresLeft == 10:
        printBoard(solutionGrid)
        print("You Win!")
        playAgain = input("Play again? (Y/N): ").lower()
        if playAgain == "y":
            reset()
        else:
            quit()
    #loops through play until the game ends
    play(solutionGrid,knownGrid)

# allows the player to indicate a chosen spot on the game grid
def choose(solutionGrid, knownGrid):
    # the lists define allowed choices given to the player
    letters = ["a","b","c","d","e","f","g","h","i"]
    numbers = ["0","1","2","3","4","5","6","7","8"]
    # causes the function to loop if given an invalid entry
    choice = input("choose a square (eg. B2) or place a marker (eg. mF7): ").lower()
    #checks if the player is placing a marker or just revealing a tile
    if len(choice) == 3 and choice[0] == "m" and choice[1] in letters and choice[2] in numbers:
       # ord() returns the ASCII value of a given charecter, subtracting 97 from the ASCII value of the allowed letters gives a value 0-8 pointing at a spot on the game grid 
       xCor, yCor = (ord(choice[1])-97, int(choice[2]))
       marker(yCor,xCor,knownGrid)
       play(solutionGrid, knownGrid)
    #revealing tile
    elif len(choice) == 2 and choice[0] in letters and choice[1] in numbers:
        return int(choice[1]),ord(choice[0])-97
    else:
        choose(solutionGrid, knownGrid)
                
                
def marker(yCor,xCor,knownGrid):
    knownGrid[yCor][xCor] = "⚐"
    printBoard(knownGrid)

#Checks known grid for 0s.
def checkZeros(knownGrid, solutionGrid, yCor, xCor):
    # copy.deepcopy is used to prevent the copied list being updated with the original list
    # copies and cycles throgh the whole grid and makes sure that every square surrounding a known 0 is opened up
    oldGrid = copy.deepcopy(knownGrid)
    zeroProcedure(yCor, xCor, knownGrid, solutionGrid)
    if oldGrid == knownGrid:
        return
    while True:
        oldGrid = copy.deepcopy(knownGrid)
        for x in range (9):
            for y in range (9):
                if location(x, y, knownGrid) == 0:
                    zeroProcedure(x, y, knownGrid, solutionGrid)
        if oldGrid == knownGrid:
            return
#essentially the same as the update value funciton but instead of adding 1 to the squares value, it opens it 
def zeroProcedure(yCor,xCor,knownGrid,solutionGrid):
   # the zero procedure is taking the 8 adjacent squares to a given 0 in the known grid and setting their values to their respective values within the solution grid or "opening them"
   # runs the zero procedure on the row above the given zero
    if yCor-1 > -1:
        row = knownGrid[yCor-1]
        if xCor-1 > -1:
            row[xCor-1] = location(yCor-1,xCor-1,solutionGrid)
        row[xCor] = location(yCor-1,xCor,solutionGrid)
        if xCor+1 < 9:
            row[xCor+1] = location(yCor-1,xCor+1,solutionGrid)
    
    #runs the zero procedure on the row of the given zero
    row = knownGrid[yCor]
    if xCor-1 > -1:
        row[xCor-1] = location(yCor,xCor-1,solutionGrid)
    if xCor+1 < 9:
        row[xCor+1] = location(yCor,xCor+1,solutionGrid)
    
    #runs the zero procedure on the row below the given zero
    
    if yCor+1 < 9:
        row = knownGrid[yCor+1]
        if xCor-1 > -1:
            row[xCor-1] = location(yCor+1,xCor-1,solutionGrid)
        row[xCor] = location(yCor+1,xCor,solutionGrid)
        if xCor+1 < 9:
            row[xCor+1] = location(yCor+1,xCor+1,solutionGrid)
setup()
reset()




















""" print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
    for yCor in range (0, 9):
        print(yCor,'║',location(yCor,0,grid),'║',location(yCor,1,grid),'║',location(yCor,2,grid),'║',
        location(yCor,3,grid),'║',location(yCor,4,grid),'║',location(yCor,5,grid),'║',location(yCor,6,grid),'║',location(yCor,7,grid),'║',location(yCor,8,grid),'║'
        ,location(yCor,9,grid),'║',location(yCor,10,grid),'║')
    if not yCor == 8:
        print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
    
    print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝') """
