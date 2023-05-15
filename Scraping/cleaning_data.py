import re
import math

def stringCut(arr):
    for j in range(1, 4):
        arr[j] = list(filter(lambda x: x != '', arr[j]))
        for k in range(len(arr[j])):
            arr[j][k] = re.findall(r'\d+\.\d+', arr[j][k])
            if len(arr[j][k]) >1:
                arr[j][k] = float(arr[j][k][1])
            else:
                arr[j][k] =-1

def probability(arr):
    probab = 0
    for j in range(1,4):
        if len(arr[j]) != 0:
            probab += 1/(max(arr[j]))
    arr[4] = str(math.floor(probab*100)) + str(" %")

'''
def stringCut(arr):
    for i in range(len(arr)):
        for j in range(1, 4):
            arr[i][j] = list(filter(lambda x: x != '', arr[i][j]))
            for k in range(len(arr[i][j])):
                arr[i][j][k] = re.findall(r'\d+\.\d+', arr[i][j][k])
                if len(arr[i][j][k]) >1:
                    arr[i][j][k] = float(arr[i][j][k][1])
                else:
                    arr[i][j][k] =-1

def probability(arr):
    for i in range(len(arr)):
        probab = 0
        for j in range(1,4):
            if len(arr[i][j]) != 0:
                probab += 1/(max(arr[i][j]))
        arr[i][4] = str(math.floor(probab*100)) + str(" %")
'''