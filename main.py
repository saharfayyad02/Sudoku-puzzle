import csv
from abc import ABC, abstractmethod
import pygame, sys
from pygame.locals import *
import numpy as np
import random

# the time in tpm & hint

N = 9  # the number of rows and column in the 2D array
Count = 0 # number of zeros in the 2D array

user1 = np.zeros((9, 9), dtype="int64") # the array we want to solve
user2 = np.zeros((9, 9), dtype="int64") # the array solved


def isSafe(grid, row, col, num): # function check if the value is uniq in the same row and the same column
    for x in range(9):
        if grid[row][x] == num: # return false if the value in the same column
            return False

    for x in range(9):
        if grid[x][col] == num: # return false if the value in the same row
            return False

    startRow = row - row % 3 # in the same squre
    startCol = col - col % 3

    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True


def solveSuduko(grid, row, col): # the function to solve the suduko
    if (row == N - 1 and col == N):
        return True

    if col == N:
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solveSuduko(grid, row, col + 1)
    for num in range(1, N + 1, 1):

        if isSafe(grid, row, col, num):

            grid[row][col] = num

            if solveSuduko(grid, row, col + 1):
                return True

        grid[row][col] = 0
    return False


# the mode is the ask the user if he want the suduku from file or randomly
mode = input("Press 1 to load a puzzle from a text file or Press 2 to start a random puzzle: ")

while(mode != '1' and mode != '2'):
    print("invaild input")
    mode = input("Press 1 to load a puzzle from a text file or Press 2 to start a random puzzle: ")


# from the file
if (mode == '1'):
    j = 0
    co = 0
    file = open("inp.txt", "r")

    for x in file:
        token = x.split("\n")[0]
        token = token.split(",")


        for i in range(len(token)):
            if(str(token[i]).isalpha()): # check the format
                print("Format of the file is Wrong!")
                exit(0)
            elif (str(token[i]).isdigit() or token[i].lstrip('-').isdigit()): # enter the numbers to the 2 d array
                user1[j][i] = token[i]
            else: # zero atherwise
                continue
        j += 1

    for i in range(9):
        for j in range(9):
            user2[i][j] = user1[i][j]
            if (user1[i][j] == 0): # get the numbers of zeros
                co += 1
            if(int(user1[i][j]) < 0 or user1[i][j] > 9 or str(user1[i][j])== '-'):
                print("Format of the file is Wrong!")
                exit(0)
            else:
                continue

    solveSuduko(user2, 0, 0)
    print(user1) # print the array
   # print(user2)
    Count = co

# the random choose
elif (mode == '2'):

    solveSuduko(user1, 0, 0)
    for i in range(N):
        for j in range(N):
            user2[i][j] = user1[i][j]

    level = input("Enter the level u want plz : ") # the level of the random array
    while (level != "E" and level != "e" and level != "D" and level != "d" and level != "M" and level != "m"):
        print("invaild input")
        level = input("Enter the level u want plz : ")  # the level of the random array

    count = 0
    easy = int(0.40* 81)  # the percentage of the easy level
    easy_num = int(81 - easy)

    med = int(0.25 * 81) # the percentage of the medium level
    med_num = int(81 - med)

    diff = int(0.1 * 81) # the percentage of the difficult level
    diff_num = int(81 - diff)

    if (level == "E" or level == "e"): # the easy level
        Count=easy_num

        while (count < easy_num):

            # choose a random value
            number_of_rows = user1.shape[0]
            number_of_columns = user1.shape[1]

            indices_x = np.random.choice(number_of_rows, size=1, replace=False)
            indices_y = np.random.choice(number_of_columns, size=1, replace=False)

            if (user1[indices_x, indices_y] != 0): # Unloading the values to zero
                user1[indices_x, indices_y] = 0
                count += 1

        print(user1)

    elif (level == "m" or level == "M"): # the med level
        Count = med_num
        while (count < med_num):

            number_of_rows = user1.shape[0]
            number_of_columns = user1.shape[1]

            indices_x = np.random.choice(number_of_rows, size=1, replace=False)
            indices_y = np.random.choice(number_of_columns, size=1, replace=False)
            if (user1[indices_x, indices_y] != 0):
                user1[indices_x, indices_y] = 0
                count += 1

        print(user1)

    elif (level == "D" or level == "d"): # the diff level
        Count = diff_num

        while (count < diff_num):

            number_of_rows = user1.shape[0]
            number_of_columns = user1.shape[1]

            indices_x = np.random.choice(number_of_rows, size=1, replace=False)
            indices_y = np.random.choice(number_of_columns, size=1, replace=False)

            if (user1[indices_x, indices_y] != 0):
                user1[indices_x, indices_y] = 0
                count += 1
        print(user1)




# abstract class
class abstract(ABC):

    @abstractmethod
    def _fill(self, row, column, value): # fill method
        raise NotImplementedError("sub class must implement the abstract class")

    @abstractmethod
    def _hint(self): # hint method
        raise NotImplementedError("sub class must implement the abstract class")

    @abstractmethod
    def _solve(self): # solve method
        raise NotImplementedError("sub class must implement the abstract class")

# one player mode class
class OM(abstract):

    def _hint(self): # hint function
        tuple = ()
        flag = 0
        for i in range(N):
            for j in range(N):
                tuple = (i, j ,user2[i][j]) # add the row & column & value to a tuple
                if (user1[int(tuple[0])][int(tuple[1])] == 0): # if the ceil is zero add the value
                    user1[int(tuple[0])][int(tuple[1])] = tuple[2]
                    flag = 1
                    break

            if (flag == 1):
                break

        print("Tuple was filled: ", tuple) # print the tuple
        print("Puzzle After Filled:\n", user1)

    def _solve(self): # solve function
        solveSuduko(user1, 0, 0) # solve the array
        print(user1)

    def _fill(self): # the fill function
        _count = 0 # for the for loop
        _points = 0 # to check the points
        _clock = pygame.time.Clock() # for the time
        _time = 0
        _score = 0 # for the score

        while (_count < Count):
            ans = input("Solve?Hint?Fill?")
            # to evaluate the time
            milli = _clock.tick()
            seconds = milli / 1000.
            _time += seconds

           # print("Time: ", _time)

            if (ans == "hint"): # hint
                self._hint()
                _count += 1
                _points -= 2
                print("Points : ", _points)
                continue

            elif (ans == "solve"): # solve
                self._solve()
                break
            elif (ans == "fill"): # fill

                # check the row and column less or equal 8 and greater and equal 0 and the value >=1 & <=9
                row = input("Enter number of row:")

                while (int(row) < 0 or int(row) > 8 ):
                    row = input("Enter a row from 0 to 8 only")

                column = input("Enter number of column:")
                while (int(column) < 0 or int(column) > 8):
                    column = input("Enter a column from 0 to 8 only")

                value = input("Enter value:")
                while (int(value) < 1 or int(value) > 9):
                    value = input("Enter a value from 1 to 9 only")

                # add to the tuple
                tuple=(row,column,value)

                # check if the ceil is zero & the value is safe and does not the wrong value
                if (int(tuple[2])==user2[int(tuple[0])][int(tuple[1])] and
                        user1[int(tuple[0])][int(tuple[1])] == 0 and
                        isSafe(user1, int(tuple[0]), int(tuple[1]),int(tuple[2]))):

                    # add to the array
                    user1[int(tuple[0])][int(tuple[1])] = int(tuple[2])
                    _count += 1
                    _points += 1 # add the points
                    print("Points : ", _points)
                    print(user1)

                else: # if the check is not correct then loss one point
                 print("Invalid input!")
                 _points-=1
                 print("Points : ", _points)
            else:
                print("invaild input")
        # check the score
        if (_points < 0):
            print("Score is :", int(0))
        else:
            if(_time!=0):
                _score = ((_points) / N) * (3600 / _time)
                print("Score is : ", _score)
        print("Time: ", _time)
        print("Points :" , _points)


class TM(abstract):

    def _hint(self): # hint function
        tuple = ()
        flag = 0
        for i in range(N):
            for j in range(N):
                tuple = (i, j,user2[i][j])
                if (user1[int(tuple[0])][int(tuple[1])] == 0):
                    user1[int(tuple[0])][int(tuple[1])] = tuple[2]
                    flag = 1
                    break

            if (flag == 1):
                break

        print("Tuple was filled: ", tuple)
        print("Puzzle After Filled:\n", user1)

    def _solve(self): # slove function
        solveSuduko(user1, 0, 0)
        print(user1)

    def _fill(self): # fill function
        _count = 0
        _points1 = 0
        _points2 = 0
        _Hint = 0
        _clock = pygame.time.Clock()
        _time1 = 0
        _time2 = 0
        _flag = 0
        _score1 = 0
        _score2 = 0

        while (_count < Count):

                if (_flag == 0): # the first player
                    ans = input("Solve?Pass?Fill?")
                    milli = _clock.tick()
                    seconds = milli / 1000.
                    _time1 += seconds

                  #  print("Time player1: ", _time1)

                    if (ans == "solve"): # the solve function
                        self ._solve()
                        break
                    elif (ans == "pass"): # pass the game to the anther player
                        _flag = 1
                        _Hint += 1
                        _points1-=1
                        if(_Hint == 4): # if the pass turned 4 times then we give a hint
                            self ._hint()
                            continue
                        else:
                            continue

                    elif (ans == "fill"):
                        _Hint = 0
                        # check the row and column less or equal 8 and greater and equal 0 and the value >=1 & <=9
                        row = input("Enter number of row player1 :")

                        while(int(row) < 0 or int(row) > 8):
                            row = input("Enter a row from 0 to 8 only player1 ")

                        column = input("Enter number of column player1 :")
                        while (int(column) < 0 or int(column) > 8 ):
                            column = input("Enter a column from 0 to 8 only player1")

                        value = input("Enter value player1:")
                        while (int(value) < 1 or int(value) > 9 ):
                            value = input("Enter a value from 1 to 9 only player1")

                        tuple1 = (row, column, value)

                        # check if the ceil is zero & the value is safe and does not the wrong value
                        if (int(tuple1[2])==user2[int(tuple1[0])][int(tuple1[1])]  and
                                user1[int(tuple1[0])][int(tuple1[1])] == 0 and
                                isSafe(user1, int(tuple1[0]), int(tuple1[1]),int(tuple1[2]))):

                            user1[int(tuple1[0])][int(tuple1[1])] = int(tuple1[2])
                            _count += 1
                            _points1 += 1
                            _flag = 1
                            print(user1)
                            print("Points player 1: ", _points1)

                        else:
                            print("Invalid input!")
                            _points1 -= 1
                            print("Points player 1: ", _points1)
                            _flag = 1

                elif (_flag == 1): # the second player
                    ans = input("Fill?Solve?Pass?")

                    milli = _clock.tick()
                    seconds = milli / 1000.
                    _time2 += seconds

                    # print("Time player2: ", _time2)

                    if(ans == "solve"): # the solve function
                        self._solve()
                        break
                    elif (ans == "pass"): # pass the game to the anther player
                        _flag = 0
                        _Hint += 1
                        _points2-=1
                        if (_Hint == 4): # if the pass turned 4 times then we give a hint
                            self._hint()
                            continue
                        else:
                            continue

                    elif (ans == "fill"):
                        _Hint = 0

                        # check the row and column less or equal 8 and greater and equal 0 and the value >=1 & <=9
                        row1 = input("Enter number of row player2 :")
                        while (int(row1) < 0 or int(row1) > 8):
                            row1 = input("Enter a row from 0 to 8 only player2")

                        column1 = input("Enter number of column player2:")
                        while (int(column1) < 0 or int(column1) > 8):
                            column1 = input("Enter a column from 0 to 8 only player2")

                        value1 = input("Enter value player2:")
                        while (int(value1) < 1 or int(value1) > 9):
                            value1 = input("Enter a value from 1 to 9 only player2")

                        tuple2 = (row1, column1, value1)

                        # check if the ceil is zero & the value is safe and does not the wrong value
                        if (int(tuple2[2])==user2[int(tuple2[0])][int(tuple2[1])]  and
                                user1[int(tuple2[0])][int(tuple2[1])] == 0 and
                                isSafe(user1, int(tuple2[0]), int(tuple2[1]),int(tuple2[2]))):

                            user1[int(tuple2[0])][int(tuple2[1])] = int(tuple2[2])
                            _count += 1
                            _points2 += 1
                            _flag = 0
                            print(user1)
                            print("Points player 2: ", _points2)
                        else:
                            print("Invalid input!")
                            _points2 -= 1
                            print("Points player 2: ", _points2)

                            _flag = 0
                    else:
                        print("invalid input")

        # check the score of every player
        if (_points1 < 0):
                print("Score player1 is :", int(0))
        else:
            _score1 = ((_points1) / N) * (3600 / _time1)
            print("Score player 1 is : ", _score1)
        print("Time player1: ", _time1)
        print("Points for player1" , _points1)
        if (_points2 < 0):
                print("Score player2 is :", int(0))
        else:
             _score2 = ((_points2) / N) * (3600 / _time2)
             print("Score player 2 is : ", _score2)
        print("Time player2: ", _time2)
        print("Points for player2" , _points2)



# one player mode or two player mode
status=input("Choose the mode of the game (t/T):Tow player mode  (o/O):One player mode : ")

while(status !="o" and status!="O" and status !="t" and status!= "T"):
    print("invaild input")
    status = input("Choose the mode of the game (t/T):Tow player mode  (o/O):One player mode : ")

# one player mode obj
if(status=="o" or status=="O"):
     obj = OM()
     obj._fill()

# two player mode obj
elif(status=="t" or status=="T"):
    obj = TM()
    obj._fill()


