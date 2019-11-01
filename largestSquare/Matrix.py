import random
import sys


def genMatrix(r, c, threshold=50):
    matrix = []
    for i in range(r):
        row = ""
        for j in range(c):
            row += '1' if random.randint(0,100) <= threshold else '0'
        matrix.append(row)
    return matrix

def createAndSaveMatrix(file, rows, cols, percent):
    matrix = genMatrix(rows, cols, percent)
    print("Matrix created")
    with open(file, "w") as f:
        for row in matrix:
            f.write(row)
            f.write('\n')
    f.close()
    print("%dX%d Matrix saved" %(rows, cols))

def readMatrixFile(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
    return [ line.strip() for line in lines ]

def binStringToInt(string):
    result = 0
    for i in range(1, len(string)+1):
        if string[-1 * i] == '1':
            result += pow(2, i-1)
    return result

def convertMatrix(matrix):
    return [ binStringToInt(row) for row in matrix ]


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 5:
        print("Usage: python3 Matrix.py <outputFile> <numRows> <numCols> <percentage of 1's>")
        exit()

    ofile = args[1]
    m = int(args[2], 10)
    n = int(args[3], 10)
    percent = int(args[4], 10)
    createAndSaveMatrix(ofile, m, n, percent)
