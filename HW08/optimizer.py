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