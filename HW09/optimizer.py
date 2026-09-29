import random
import math
from setup import Setup

class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0      # Type of problem
        self._numExp = 0     # Total number of experiments

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print("Number of experiments:", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 0:
            print("Mutation step size:", self._delta)

class MetaHeuristic(Optimizer):
    def __init__(self):
        Optimizer.__init__(self) 

class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitStuck = 0  # Max evaluations allowed for no improvement
        self._numRestart = 0  # Number of restarts

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts:", self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2 <= self._aType <= 3:  # First-Choice, Stochastic
            print("Max evaluations with no improvement: {}"
                  .format(self._limitStuck))

    def run(self):
        pass

    def randomRestart(self, p):
        i = 1
        self.run(p) 
        bestSolution = p.getSolution()  
        bestMinimum = p.getValue() 
        numEval = p.getNumEval() 
        while i < self._numRestart: 
            self.run(p) 
            newSolution = p.getSolution()  
            newMinimum = p.getValue() 
            numEval += p.getNumEval() 
            if newMinimum < bestMinimum: 
                bestSolution = newSolution
                bestMinimum = newMinimum
            i += 1  
        p.storeResult(bestSolution, bestMinimum) 

class SimulatedAnnealing(MetaHeuristic): 
    def __init__(self):
        self._numSample = 100
        self._limitEval = 100000
        self._whenBestFound = 0

    def setVariables(self, p):
        pass

    def displaySetting(self):
        print("Search Algorithm: Simulated Annealing")
        print("Number of evaluations until termination: {:,}".format(self._limitEval))
        
    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        best, valueBest = current, valueC
        whenBestFound = i = 1
        t = self.initTemp(p)  # An initial temperature is set
        while True:
            t = self.tSchedule(t)  # Follow annealing schedule
            if t == 0 or i == self._limitEval:
                break
            
            neighbor = p.randomMutant(current)
            valueN = p.evaluate(neighbor)
            i += 1
            dE = valueN - valueC
            
            if dE < 0:
                current = neighbor
                valueC = valueN
            elif random.uniform(0, 1) < math.exp(-dE / t):
                current = neighbor  # Move to a worse neighbor
                valueC = valueN
            if valueC < valueBest:
                best, valueBest = current, valueC
                whenBestFound = i
            self._whenBestFound = whenBestFound
            p.storeResult(best, valueBest)


class GA(MetaHeuristic):
    def __init__(self):
        MetaHeuristic.__init__(self)
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation

    def setVariables(self, parameters):
        MetaHeuristic.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        MetaHeuristic.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)

    def run(self, p):
        # Population 생성
        pop = p.initializePop(self._popSize)
        # Population 중 최적해 찾기
        best = self.evalAndFindBest(pop, p)
        numEval = p.getNumEval()
        whenBestFound = numEval
        # limitEval까지 [다음 세대 생성-평가] 반복
        while numEval < self._limitEval:
            newPop = []
            i = 0
            # 다음 세대 생성; start
            while i < self._popSize:
                par1, par2 = self.selectParents(pop)  
                ch1, ch2 = p.crossover(par1, par2, self._pC)  
                newPop.extend([ch1, ch2])
                i += 2
            newPop = [p.mutation(ind, self._pM) for ind in newPop]  
            pop = newPop
            # 다음 세대 생성; end
            # 다음 세대 값 평가 및 best 업데이트
            newBest = self.evalAndFindBest(pop, p)
            numEval = p.getNumEval()
            if newBest[0] < best[0]:
                best = newBest
                whenBestFound = numEval
        self._whenBestFound = whenBestFound
        bestSolution = p.indToSol(best)
        p.storeResult(bestSolution, best[0])

    def evalAndFindBest(self, pop, p): 
        best = pop[0]
        p.evalInd(best)
        bestValue = best[0]
        for i in range(1, len(pop)):
            p.evalInd(pop[i])
            newValue = pop[i][0]
            if newValue < bestValue:
                best = pop[i]
                bestValue = newValue
        return best

    def selectParents(self, pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.binaryTournament(ind1, ind2) 
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.binaryTournament(ind1, ind2) 
        return par1, par2
    
    def selectTwo(self, pop):
        # pop에서 random하게 2개의 individuals 선택해서 반환
        popCopy = pop[:]
        random.shuffle(popCopy)
        return popCopy[0], popCopy[1]

    def binaryTournament(self, ind1, ind2):
        # 2개의 individuals 중 더 좋은 ind 선택해서 반환
        if ind1[0] < ind2[0]:
            return ind1
        else:
            return ind2
        
    def crossover(self, ind1, ind2, uXp):
        chr1, chr2 = self.uXover(ind1[1], ind2[1], uXp)
        return [0, chr1], [0, chr2]

    def uXover(self, chrInd1, chrInd2, uXp):  # uniform crossover
        # chrInd1, chrInd2의 각 원소를 확률적(uXp)으로 crossover
        chr1 = chrInd1[:]  # Make copies
        chr2 = chrInd2[:]
        for i in range(len(chr1)):
            if random.uniform(0, 1) < uXp:
                chr1[i], chr2[i] = chr2[i], chr1[i]
        return chr1, chr2
    
    def mutation(self, ind, mrF):  # bit-flip mutation
        # mrF * (1/ lnegth of individual) 확률로 ind의 개별 원소 bit-flip
        # pM is interpreted as mrF (factor to adjust mutation rate)
        child = ind[:]  # Make copy
        n = len(ind[1])
        for i in range(n):
            if random.uniform(0, 1) < mrF * (1 / n):
                child[1][i] = 1 - child[1][i]
        return child

    
class Stochastic(HillClimbing):
    def __init__(self):
        pass

    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        # hint; Stochastic 알고리즘은 Steepest Ascent 알고리즘과 흐름이 유사함
        current = p.randomInit()  
        valueC = p.evaluate(current)  
        i = 0
        while i < self._limitStuck:
            neighbors = p.mutants(current)  
            successor, valueS = self.stochasticBest(neighbors, p)  
            if valueS < valueC: 
                current = successor
                valueC = valueS
                i = 0  
            else:
                i += 1
        p.storeResult(current, valueC)

    def stochasticBest(self, neighbors, p):
        # Smaller valuse are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

class FirstChoice(HillClimbing):
    def displaySetting(self):
        # first-choice.py 코드의 displaySetting 부분 활용
        # HillClimb에 정의했던 displaySetting을 Super를 통해 호출해서 구현하기
        print()
        print("Search Algorithm: First-Choice Hill Climbing")
        super().displaySetting()
        print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStuck))

    def run(self, p):
        # first-choice.py에 정의했던 firstchoice 함수를 활용해서 구현
        # global Variable 대신 class variable을 활용하도록 변경
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest Ascent Hill Climbing")
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit()  # A current candidate solution
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        best = neighbors[0]
        bestValue = p.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print("Search Algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
        currentP = p.randomInit()  # Current point
        valueC = p.evaluate(currentP)
        while True:
            nextP = p.takeStep(currentP, valueC)
            valueN = p.evaluate(nextP)
            if valueN >= valueC:
                break
            else:
                currentP = nextP
                valueC = valueN
        p.storeResult(currentP, valueC)