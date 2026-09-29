from problem import Numeric


def main():
    # Create a Problme object for numerical optimization
    p = Numeric()    # Create a problem object 
    p.setVariables() # Set its class variables (expression, domain)
    # Call the search algorithm
    gradientDescent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def gradientDescent(p):
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

def displaySetting(p):
    print()
    print("Search algorithm: Gradient Descent")
    print()
    print("Udate rate:", p.getAlpha())
    print("Increment for calculating derivative:", p.getDx())

main()