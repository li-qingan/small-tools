from ipysheet import sheet, cell, row, column, cell_range
import random
import ipywidgets as widgets
import ipysheet
import numpy as np
import xlrd

# %%
# 选择位置
def chooseIJ(baseI, baseJ):
    if baseI == nRows:
        return nRows, nCols
    for j in range(baseJ,nCols):
            if checkboard[baseI][j] == 0:
                return baseI, j

    for i in range(baseI+1,nRows):
        for j in range(0,nCols):
            if checkboard[i][j] == 0:
                return i, j
    return nRows, nCols


# %%
# 检查对应行、列、九宫格是否有重复元素
def tryValue(i, j):
    available = set()
    for k in range(nRows):
        available.add(record[i][k])  #所在行
        available.add(record[k][j])     #所在列
    baseI = int(i)//3 * 3
    baseJ = int(j)//3 * 3
    for p in range(3):
        for q in range(3):
            available.add(record[baseI+p][baseJ+q]) #所在九宫格
    
    iniValue = record[i][j] + 1
    for value in range(iniValue, 9+1):
        if value in available:  # 如果无重复
            continue
        else:
            record[i][j] = value
            return True
    return False


# %%
def printResult(stack):
    for index in stack:
        i = index//nCols
        j = index%nCols
        checkboard[i][j] = record[i][j]
    
    for i in range(nRows):
        for j in range(nCols):
            print (checkboard[i][j], end='\t')
        print('\n')

def printSpace(num):
    for i in range(num):
        print(' ', end='')


data = xlrd.open_workbook("data.xlsx")
table = data.sheets()[0]
nRows = table.nrows
nCols = table.ncols
checkboard = np.zeros((nRows, nCols), dtype=int)

for i in range(nRows):
    #print(table.row_values(i))
    for j in range(nCols):
        value = table.row_values(i)[j]
        if value != '':
            checkboard[i][j] = value

record = np.zeros((nRows,nCols), dtype=int)


for i in range(nRows):
    for j in range(nCols):
        value = checkboard[i][j]
        print(value, end='\t')
        record[i][j] = value
    print('\n')

# %%
baseI, baseJ = 0, 0
stack = []
finish = False
while True:
    i,j = chooseIJ(baseI, baseJ)

    if i > nRows - 1 or j > nCols - 1:
        finish = True
        print('Succeed!')
        printResult(stack)
        break;

    success = tryValue(i,j)
    if success:
        
        #for debug: print the tries
        #printSpace(len(stack) * 2)
        #print(i, j, ':', record[i][j])
        stack.append(i*nCols+j)
        if i == 1 and j == 7:
            print("hit")
        baseI = i
        baseJ = j + 1
        if baseJ == nCols:
            baseJ = 0
            baseI = baseI + 1
    else:
        # fail, backtrace it
        
        if len(stack) == 0:
            print('Fail!!!')
            break
        index = stack.pop()
        baseI, baseJ = index//nCols, index%nCols
        #printSpace(len(stack)*2)
        #print("fail@(%d, %d)", i,j)
        record[i][j] = 0
        


