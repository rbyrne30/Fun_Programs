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

def convertMatrix(matrix):
    return [ int(row, 2) for row in matrix ]

def checkCons(row, size):
    for i in range(size):
        if row>>i & 1 != 1:
            return False
    return True

def findLargestSquare(matrix):
    return pow( findLargestSquareHelper(convertMatrix(matrix), len(matrix[0]), 1), 2 )

def ANDRows(matrix):
    newMatrix = []
    for i in range(len(matrix)-1):
        newMatrix.append(matrix[i] & matrix[i+1])
    return newMatrix

def findLargestSquareHelper(matrix, numCols, size):
    for row in matrix:
        # Find consecutive
        cons = 0
        for i in range(numCols):
            if 1 & row>>i == 1:
                cons += 1
            else:
                cons = 0
            if cons >= size:
                return findLargestSquareHelper(ANDRows(matrix), numCols, size+1)
    return size - 1



if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    matrix = Matrix.readMatrixFile(sys.argv[1])
    print(findLargestSquare(matrix))
