from problem import *
from optimizer import *

def main():
    p, pType = selectProblem()
    alg = selectAlgorithm(pType) # 추가

    # Call the search algorithm
    alg.randomRestart(p)
    # Show the problem solved 
    p.describe()
    # Show the algorithm settings 
    alg.displaySetting()
    # Report results
    p.report()

    if issubclass(type(alg), HillClimbing):
        alg.randomRestart(p)
    else: 
        alg.run(p)

def selectProblem():
    print("Select the problem type:")
    print("  1. Numerical Optimization")
    print("  2. TSP")

    # 1 (Numeric) 또는 2 (TSP)를 입력 받아서 대응되는 Problem Class를 초기화해서 반환하기 
    pType = int(input("Enter the number: "))
    if pType == 1:               # Create an empty problem instance
        p = Numeric()            #
    elif pType == 2:             #
        p = Tsp()                #
    p.setVariables()        # Now 'p' is a specific problem instance
    return p, pType

def selectAlgorithm(pType): 
    print()
    print("Select the search algorithm:")
    print("  1. Steepest-Ascent")
    print("  2. First-Choice")
    print("  3. Gradient Descent")
    print("  4. Stocahstic")
    print("  5. SimulatedAnnealing")

    # pType == 2 (TSP)일 경우, Gradient Descent를 입력 받으면 사용자로부터 재입력 받도록 구현 
    # pType과 aType이 올바르게 설정 됐는지 확인하기 위한 invalid(pType, aType) 함수 추가 구현
    while True:
        aType = int(input("Enter the number: "))
        if not invalid(pType, aType):
            break
    optimizers = { 1: 'SteepestAscent()',
                   2: 'FirstChoice()',
                   3: 'GradientDescent()',
                   4: 'Stochastic()',
                   5: 'SimulatedAnnealing()'}
                   
    alg = eval(optimizers[aType])
    alg.setVariables(pType)
    return alg

def invalid(pType, aType):
    if pType == 2 and aType == 3:
        print("You cannot choose Gradient Descent")
        print("   unless you want a function optimization.")
        return True
    else:
        return False
    
def conductExperiment(p, alg):
    aType = alg.getAType()
    if 1 <= aType <= 4:
        alg.randomRestart(p)
    else:
        alg.run(p)
        bestSolution = p.getSolution()       
        bestMinimum = p.getValue()          # First result is current best
        numEval = p.getNumEval()            
        sumOfMinimum = bestMinimum          # Prepare for averaging
        sumOfNumEval = numEval              # Prepare for averaging
        sumOfWhen = 0                       # When the best solution is found
        if 5 <= aType <= 6:
            sumOfWhen = alg.getWhenBestFound()
        numExp = alg.getNumExp()
        for i in range(1, numExp):
            p.setNumExp() 
            alg.run(p)                        
            newSolution = p.getSolution()    
            newMinimum = p.getValue()       
            numEval = p.getNumEval()         
            sumOfMinimum += newMinimum       
            sumOfNumEval += numEval          
            if newMinimum < bestMinimum:     
                bestSolution = newSolution   
                bestMinimum = newMinimum     
            sumOfWhen += alg.getWhenBestFound() 
        if newMinimum < bestMinimum:
            bestSolution = newSolution  # Update the best-solution
            bestMinimum = newMinimum
    avgMinimum = sumOfMinimum / numExp
    avgNumEval = round(sumOfNumEval / numExp)
    avgWhen = round(sumOfWhen / numExp)
    results = (bestSolution, bestMinimum, avgMinimum, avgNumEval, sumOfNumEval, avgWhen)
    p.storeExpResult(results)

main()