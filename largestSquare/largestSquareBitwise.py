# Problem
# Have the function MaximalSquare(strArr) take the strArr parameter
# being passed which will be a 2D matrix of 0 and 1's, and determine
# the area of the largest square submatrix that contains all 1's.
# A square submatrix is one of equal width and height, and your program
# should return the area of the largest submatrix that contains only 1's.
# For example: if strArr is ["10100", "10111", "11111", "10010"] then this
# looks like the following matrix:
#
# 1 0 1 0 0
# 1 0 1 1 1
# 1 1 1 1 1
# 1 0 0 1 0
#
# For the input above, you can see the bolded 1's create the largest square
# submatrix of size 2x2, so your program should return the area which is 4.
# You can assume the input will not be empty.

import Matrix
import sys

def getCols(matrix):
    cols = []
    for i in range(len(matrix[0])):
        col = ""
        for row in matrix:
            col += row[i]
        cols.append(col)
    return cols

def convertMatrix(matrix):
    return [ int(row, 2) for row in matrix ]

def checkCons(row, size):
    for i in range(size):
        if row>>i & 1 != 1:
            return False
    return True

def findLargestSquareHelper(rows, cols, numRows, numCols, size):
    for i in range(len(rows)):
        row = rows[i]
        cons = 0
        for j in range(numCols):
            cons = cons + 1 if row>>j & 1 == 1 else 0
            if cons >= size:
                if checkCons(cols[numCols-j-1]>>numRows-i-size, size):
                    ANDRows = [ rows[k] & rows[k+1] for k in range(len(rows)-1) ]
                    ANDCols = [ cols[k] & cols[k+1] for k in range(len(cols)-1) ]
                    return findLargestSquareHelper(ANDRows, ANDCols, numRows, numCols, size+1)
    return size-1

def findLargestSquare(matrix):
    convertedMatrixRows = convertMatrix(matrix)
    convertedMatrixCols = convertMatrix(getCols(matrix))
    return pow( findLargestSquareHelper(convertedMatrixRows, convertedMatrixCols, len(convertedMatrixRows), len(convertedMatrixCols), 1), 2 )


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    matrix = Matrix.readMatrixFile(sys.argv[1])
    print(findLargestSquare(matrix))
