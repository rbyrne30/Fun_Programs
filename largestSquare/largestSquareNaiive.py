import Matrix
import sys
import time

def isConsecutive(row, size):
    if size > len(row):
        return False
    for i in range(size):
        if row[i] != '1':
            return False
    return True

def findLargestSquareHelper(matrix, size):
    for i in range(len(matrix)-size+1):
        for j in range(len(matrix[i])-size+1):
            if matrix[i][j] != '1':
                continue
            isSquare = True
            for k in range(size):
                if not isConsecutive(matrix[i+k][j:], size):
                    isSquare = False
                    break
            if isSquare:
                return findLargestSquareHelper(matrix, size+1)
    return pow(size-1, 2)


def findLargestSquare(matrix):
    start = time.time()
    result = findLargestSquareHelper(matrix, 1)
    # print("Algorithm took %f secs" %(time.time() - start))
    return result


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    matrix = Matrix.readMatrixFile(sys.argv[1])
    print(findLargestSquare(matrix))
