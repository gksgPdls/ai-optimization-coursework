from problem import Numeric


def main():
    # Create an instance of numerical optimization problem
    p = Numeric()   # 'p': (expr, domain)
    p.setVariables()
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()

def steepestAscent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)

def bestOf(neighbors, p): ###
    # 변형된 투어 경로들 중, 첫번째 것을 최단 경로로 설정
    best = neighbors[0]
    bestValue = p.evaluate(best)

    # 첫 투어 경로를 제외하고 iterate
    for i in range(1, len(neighbors)):
        newValue = p.evaluate(neighbors[i])
        # 더 좋은 투어 경로가 있으면 최단 경로를 더 좋은 투어 경로로 업데이트
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue

    return best, bestValue

def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())

main()