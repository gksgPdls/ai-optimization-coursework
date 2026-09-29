from problem import *
from optimizer import *


def readPlan():
    fileName = input("Enter the file name of experimental setting: ") 
    infile = open(fileName, 'r')
    ############## GA를 위한 parameter 추가하기; start ############### 
    parameters = {
        'pType': 0, 'pFileName': '', 'aType': 0, 'delta': 0,
        'limitStuck': 0, 'alpha': 0, 'dx': 0, 'numRestart': 0,
        'limitEval': 0, 'numExp': 0, 'popSize': 0, 'resolution': 0,
        'uXp': 0, 'mrF': 0, 'XR': 0, 'mR': 0
    }
    ############## GA를 위한 parameter 추가하기; end ###############

     # 설정 파일에서 한 줄씩 읽어서 parameters 업데이트
    for line in infile:
        # 각 줄을 key=value 형태로 나누기
        key, value = line.strip().split('=')
        # 파라미터 키가 유효하면 값 업데이트
        if key in parameters:
            parameters[key] = float(value) if '.' in value else int(value)

    # 파일 닫기
    infile.close()
    # 파라미터 반환하기
    return parameters

def readPlanAndCreate():
    # 설정 파일에서 매개변수 읽기
    parameters = readPlan() 
    # 문제 객체 생성 
    p, pType = selectProblem() 
    # 매개변수에 문제 타입 추가 
    parameters['pType'] = pType  
    # 알고리즘 객체 생성
    alg = createOptimizer(parameters)  
    return p, alg

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
    
def createOptimizer(parameters):
    # 옵티마이저 변수 초기화
    optimizer = None

    # 알고리즘 타입에 따라 맞는 클래스 초기화
    if parameters['aType'] == 1:
        # SteepestAscent 옵티마이저 생성
        optimizer = SteepestAscent(parameters)
    elif parameters['aType'] == 2:
        # FirstChoice 옵티마이저 생성
        optimizer = FirstChoice(parameters)
    elif parameters['aType'] == 3:
        # GradientDescent 옵티마이저 생성
        optimizer = GradientDescent(parameters)
    elif parameters['aType'] == 4:
        # Stochastic 옵티마이저 생성
        optimizer = Stochastic(parameters)
    elif parameters['aType'] == 5:
        # SimulatedAnnealing 옵티마이저 생성
        optimizer = SimulatedAnnealing(parameters)
    elif parameters['aType'] == 6:
        # GeneticAlgorithm 옵티마이저 생성
        optimizer = GA(parameters)
    else:
        # 유효하지 않은 알고리즘 타입이면 에러 출력
        print("Invalid algorithm type!")
    
    # 생성된 옵티마이저 반환하기
    return optimizer
    
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

def main():
    # 문제와 알고리즘 객체 생성
    p, alg = readPlanAndCreate()  # 문제(p)와 알고리즘(alg) 초기화
    if not p or not alg:  # 객체 생성 실패 시 종료
        return

    # 실험 수행
    conductExperiment(p, alg)

    # 문제 설명 및 결과 출력
    p.describe()  # 문제 설명 출력
    alg.displaySetting()  # 알고리즘 설정 출력
    p.report()  # 최종 결과 출력

main()