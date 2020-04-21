"""A command line version of Minesweeper"""
import random
import re
import time
import os
from string import ascii_lowercase


def setupgrid(gridsize, start, numberofmines):
    emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]

    mines = getmines(emptygrid, start, numberofmines)

    for i, j in mines:
        emptygrid[i][j] = 'X'

    grid = getnumbers(emptygrid)

    return (grid, mines)


def showgrid(grid):
    gridsize = len(grid)

    horizontal = '   ' + (4 * gridsize * '-') + '-'

    # Print top column letters
    toplabel = '     '

    for i in ascii_lowercase[:gridsize]:
        toplabel = toplabel + i + '   '

    print(toplabel + '\n' + horizontal)

    # Print left row numbers
    for idx, i in enumerate(grid):
        row = '{0:2} |'.format(idx + 1)

        for j in i:
            row = row + ' ' + j + ' |'

        print(row + '\n' + horizontal)

    print('')


def getrandomcell(grid):
    gridsize = len(grid)

    a = random.randint(0, gridsize - 1)
    b = random.randint(0, gridsize - 1)

    return (a, b)


def getneighbors(grid, rowno, colno):
    gridsize = len(grid)
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                neighbors.append((rowno + i, colno + j))

    return neighbors


def getmines(grid, start, numberofmines):
    mines = []
    neighbors = getneighbors(grid, *start)

    for i in range(numberofmines):
        cell = getrandomcell(grid)
        while cell == start or cell in mines or cell in neighbors:
            cell = getrandomcell(grid)
        mines.append(cell)

    return mines


def getnumbers(grid):
    for rowno, row in enumerate(grid):
        for colno, cell in enumerate(row):
            if cell != 'X':
                # Gets the values of the neighbors
                values = [grid[r][c] for r, c in getneighbors(grid,
                                                              rowno, colno)]

                # Counts how many are mines
                grid[rowno][colno] = str(values.count('X'))

    return grid


def showcells(grid, currgrid, rowno, colno):
    # Exit function if the cell was already shown
    if currgrid[rowno][colno] != ' ':
        return

    # Show current cell
    currgrid[rowno][colno] = grid[rowno][colno]

    # Get the neighbors if the cell is empty
    if grid[rowno][colno] == '0':
        for r, c in getneighbors(grid, rowno, colno):
            # Repeat function for each neighbor that doesn't have a flag
            if currgrid[r][c] != 'F':
                showcells(grid, currgrid, r, c)


def playagain():
    choice = input('Play again? (y/n): ')

    return choice.lower() == 'y'


def parseinput(inputstring, gridsize, helpmessage):
    cell = ()
    flag = False
    message = "Invalid cell. " + helpmessage

    pattern = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[gridsize - 1])
    validinput = re.match(pattern, inputstring)

    if inputstring == 'help':
        message = helpmessage

    elif validinput:
        rowno = int(validinput.group(2)) - 1
        colno = ascii_lowercase.index(validinput.group(1))
        flag = bool(validinput.group(3))

        if -1 < rowno < gridsize:
            cell = (rowno, colno)
            message = ''

    return {'cell': cell, 'flag': flag, 'message': message}

def Eval(cnode, tl, tm, tr, ml, mr, bl, bm, br):
    #array of prob
    nNull = 0
    uSpace = 0
    nFlag = 0
    pVal = [tl, tm, tr, ml, mr, bl, bm, br]
    # print(pVal)
    #Counts empty, unchecked and flagged spaces
    for i in range(len(pVal)):
        # print(i)
        if pVal[i] == -1:
            nNull = nNull + 1
        if isinstance(pVal[i], int):
            uSpace = uSpace + 1
        if pVal[i] == 'F':
            nFlag = nFlag + 1
    nRemain = 8 - (nNull + uSpace)
    if(nRemain > 0):
        prob = (int(cnode) - nFlag) / nRemain
    else:
        print("Something is wrong")
    for i in range(len(pVal)):
        if(pVal[i] == ' '):
            pVal[i] = prob
        else:
            pVal[i] = 0

    return pVal

def AI(currgrid, probGrid):
    gridsize = 9
    pGrid = probGrid
    for i in range(gridsize):
        for x in range(gridsize):
            cnode = currgrid[i][x]
            if(cnode.isdigit()):
                if(int(cnode) > 0):
                    # Eval:
                    if(i + 1 < gridsize):
                        tm = currgrid[i + 1][x]
                        if(x - 1 >= 0):
                            tl = currgrid[i + 1][x - 1]
                        else:
                            tl = -1
                        if(x + 1 < gridsize):
                            tr = currgrid[i + 1][x + 1]
                        else:
                            tr = -1
                    else:
                        tm = tl = tr = -1
                    if(x - 1 >= 0):
                        ml = currgrid[i][x - 1]
                    else:
                        ml = -1
                    if(x + 1 < gridsize):
                        mr = currgrid[i][x + 1]
                    else:
                        mr = -1
                    if(i - 1 >= 0):
                        bm = currgrid[i - 1][x]
                        if(x - 1 >= 0):
                            bl = currgrid[i - 1][x - 1]
                        else:
                            bl = -1
                        if(x + 1 < gridsize):
                            br = currgrid[i - 1][x + 1]
                        else:
                            br = -1
                    else:
                        bl = bm = br = -1
                    #Evaluating the spaces
                    # print(i, x)
                    pVal = Eval(cnode, tl, tm, tr, ml, mr, bl, bm, br)
                    if(pVal[0] != 0):
                        pGrid[i + 1][x - 1] += pVal[0]
                    if(pVal[1] != 0):
                        pGrid[i + 1][x] += pVal[1]
                    if(pVal[2] != 0):
                        pGrid[i + 1][x + 1] += pVal[2]
                    if(pVal[3] != 0):
                        pGrid[i][x - 1] += pVal[3]
                    if(pVal[4] != 0):
                        pGrid[i][x + 1] += pVal[4]
                    if(pVal[5] != 0):
                        pGrid[i - 1][x - 1] += pVal[5]
                    if(pVal[6] != 0):
                        pGrid[i - 1][x] += pVal[6]
                    if(pVal[7] != 0):
                        pGrid[i - 1][x + 1] += pVal[7]

    return pGrid


def playgame():
    gridsize = 9
    numberofmines = 10
    probGrid = [[(numberofmines / (gridsize * gridsize)) for i in range(gridsize)] for i in range(gridsize)]

    currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

    grid = []
    flags = []
    starttime = 0

    helpmessage = ("Type the column followed by the row (eg. a5). "
                   "To put or remove a flag, add 'f' to the cell (eg. a5f).")

    showgrid(currgrid)
    print(helpmessage + " Type 'help' to show this message again.\n")

    while True:
        minesleft = numberofmines - len(flags)
        prompt = input('Enter the cell ({} mines left): '.format(minesleft))
        result = parseinput(prompt, gridsize, helpmessage + '\n')

        message = result['message']
        cell = result['cell']

        if cell:
            print('\n\n')
            rowno, colno = cell
            currcell = currgrid[rowno][colno]
            flag = result['flag']

            if not grid:
                grid, mines = setupgrid(gridsize, cell, numberofmines)
            if not starttime:
                starttime = time.time()

            if flag:
                # Add a flag if the cell is empty
                if currcell == ' ':
                    currgrid[rowno][colno] = 'F'
                    flags.append(cell)
                # Remove the flag if there is one
                elif currcell == 'F':
                    currgrid[rowno][colno] = ' '
                    flags.remove(cell)
                else:
                    message = 'Cannot put a flag there'

            # If there is a flag there, show a message
            elif cell in flags:
                message = 'There is a flag there'

            elif grid[rowno][colno] == 'X':
                print('Game Over\n')
                showgrid(grid)
                if playagain():
                    playgame()
                return

            elif currcell == ' ':
                showcells(grid, currgrid, rowno, colno)

            else:
                message = "That cell is already shown"

            if set(flags) == set(mines):
                minutes, seconds = divmod(int(time.time() - starttime), 60)
                print(
                    'You Win. '
                    'It took you {} minutes and {} seconds.\n'.format(minutes,
                                                                      seconds))
                showgrid(grid)
                if playagain():
                    playgame()
                return

        showgrid(currgrid)
        probGrid = AI(currgrid, probGrid)
        if(os.path.exists("grid.txt")):
            os.remove("grid.txt")
        f = open("grid.txt", "a")
        for ele in probGrid:
            for i in ele:
                f.write(str(i))
            f.write('\n')
        f.close()
        print(message)

playgame()