import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem(): ###
    file_name=input("Enter the file name of a function: ")
    with open(file_name, 'r') as infile:
        expression = infile.readline().strip()  # 첫 번째 줄의 수식 읽기
        domain = [[], [], []]  # 변수 이름, 하한, 상한 저장할 리스트
        for line in infile:
            var, low, up = line.strip().split(',')  # 변수 이름과 하한, 상한 읽기
            domain[0].append(var)  # 변수 이름 추가
            domain[1].append(float(low))  # 하한 추가
            domain[2].append(float(up))  # 상한 추가

    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    return expression, domain


def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def randomInit(p): ###
    domain = p[1]  # domain: [VarNames, low, up]
    low, up=domain[1], domain[2]
    init=[]
    for i in range(len(low)): # for each variable
        r=random.uniform(low[i], up[i]) # take a random value
        init.append(r)

    return init    # Return a random initial point
                   # as a list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)


def mutants(current, p): ###
    neighbors = []
    for i in range(len(current)): # for each variable
        mutant = mutate(current, i, DELTA, p)  
        neighbors.append(mutant)  
        mutant = mutate(current, i, -DELTA, p)  
        neighbors.append(mutant)  

    return neighbors     # Return a set of successors


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def bestOf(neighbors, p): ###
    # 변형된 투어 경로들 중, 첫번째 것을 최단 경로로 설정
    best = neighbors[0]
    bestValue = evaluate(best, p)

    # 첫 투어 경로를 제외하고 iterate
    for i in range(1, len(neighbors)):
        newValue = evaluate(neighbors[i], p)
        # 더 좋은 투어 경로가 있으면 최단 경로를 더 좋은 투어 경로로 업데이트
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue

    return best, bestValue

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple


main()