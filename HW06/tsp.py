import random
import math

NumEval = 0    # Total number of evaluations


def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline())
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != '':
        locations.append(eval(line)) # Make a tuple and append
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)
    return numCities, locations, table

def calcDistanceTable(numCities, locations): ###
    # num cities * num cities 크기의 2D 배열 생성
    table = [[0] * numCities for _ in range(numCities)]

    # 각 city마다 iterate
    for i in range(numCities):
        # i city 보다 앞에 있는 city는 이미 계산되었기 때문에, i+1 부터 끝까지 iterate
        for j in range(i + 1, numCities):
            # 거리 계산
            x1, y1 = locations[i]
            x2, y2 = locations[j]
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            # i-j 사이 거리를 i-j, j-i 위치에 저장
            table[i][j] = distance
            table[j][i] = distance

    return table # A symmetric matrix of pairwise distances

def randomInit(p):   # Return a random initial tour
    n = p[0]
    init = list(range(n))
    random.shuffle(init)
    return init


def evaluate(current, p): ###
    ## Calculate the tour cost of 'current'
    ## 'p' is a Problem instance
    ## 'current' is a list of city ids
    global NumEval
    NumEval += 1

    n = p[0]
    table = p[2]  # 거리 = distance table임
    cost = 0  # 비용 초기화

    # 각 도시마다, 다음 도시까지 특이한거 없이 distance table을 참고하여 비용 계산
    for i in range(n - 1):
        locFrom = current[i]
        locTo = current[i + 1]
        cost += table[locFrom][locTo]

    # 마지막 도시에서 처음 도시로 돌아오는 비용을 고려해서 cost에 더해줌
    cost += table[current[-1]][current[0]]

    return cost

def inversion(current, i, j):  # Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
        i += 1
        j -= 1
    return curCopy

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()

def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()