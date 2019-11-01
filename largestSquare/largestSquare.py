import Matrix
import sys

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

# NOTE: Try to implement using BIT-WISE operations

def AND(str1, str2):
    if len(str1) != len(str2):
        return None
    result = ""
    for i in range(len(str1)):
        if str1[i] == '1' and str2[i] == '1':
            result += '1'
        else:
            result += '0'
    return result

def getColumns(matrix):
    cols = []
    for i in range(len(matrix[0])):
        col = ""
        for row in matrix:
            col += row[i]
        cols.append(col)
    return cols

def getMaxConsecutive(L):
    max = 0;
    count = 0;
    countIndex = 0;
    for i in range(len(L)):
        if L[i] == '1':
            count += 1
            if count > max:
                countIndex = i
                max = count
        else:
            count = 0
        max = max if max > count else count
    return max, countIndex-max+1


def findLargestSquareHelper(rows, cols, size):
    ANDRows = []
    ANDCols = []
    for i in range(len(rows)-1):
        ANDRows.append(AND(rows[i], rows[i+1]))
    for i in range(len(cols)-1):
        ANDCols.append(AND(cols[i], cols[i+1]))

    maxConsRowList = list(map(lambda x: getMaxConsecutive(x), ANDRows))
    maxConsColList = list(map(lambda x: getMaxConsecutive(x), ANDCols))
    # print("maxConsRowList " + str(maxConsRowList))
    # print("maxConsColList " + str(maxConsColList))

    for i in range(len(maxConsRowList)):
        if maxConsRowList[i][0] >= size and maxConsColList[maxConsRowList[i][1]][0] >= size:
            # print("Found square of side length %d at (%d,%d)" %(size, maxConsRowList[i][1], maxConsColList[maxConsRowList[i][1]][1]))
            return findLargestSquareHelper(ANDRows, ANDCols, size+1)
    return size-1


def findLargestSquare(matrix):
    return pow( findLargestSquareHelper(matrix, getColumns(matrix), 2), 2)


if __name__ == "__main__":
    # matrix = genMatrix(1000, 1000, 80)
    # for row in matrix:
    #     print(row)
    # print()

    sys.setrecursionlimit(10000)
    matrix = Matrix.readMatrixFile(sys.argv[1])
    print(findLargestSquare(matrix))
