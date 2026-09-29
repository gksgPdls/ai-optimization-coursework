def inputData():
    #annualRateOfInterest, monthlyPayment, begBalance 입력받음
    annualRateOfInterest=float(input("annual rate of interest: "))*0.01 #rate로 변환
    monthlyPayment=float(input("Enter monthly payment: "))
    begBalance=float(input("Enter beg. of month balance: "))
    #입력값 반환
    return annualRateOfInterest, monthlyPayment, begBalance

def calculateValues(annualRateOfInterest, monthlyPayment, begBalance):
    #intForMonth, redOfPrincipal, endBalance 계산
    intForMonth = int(begBalance*(annualRateOfInterest/12)*100)/100 #Round down the intForMonth to two decimal places
    redOfPrincipal=monthlyPayment-intForMonth
    endBalance=begBalance-redOfPrincipal
    #계산값 반환
    return intForMonth, redOfPrincipal, endBalance

def displayOutput(intForMonth, redOfPrincipal, endBalance):
    #format method 사용하여 출력
    print("Interest paid for the month: ${:,.2f}".format(intForMonth))
    print("Reduction of principal: ${:,.2f}".format(redOfPrincipal))
    print("End of month balance: ${:,.2f}".format(endBalance))
    
def main():
    #Analyze monthly payment of mortgage.
    annualRateOfInterest, monthlyPayment, begBalance = inputData()
    (intForMonth, redOfPrincipal, endBalance)= calculateValues(annualRateOfInterest, monthlyPayment, begBalance)
    displayOutput(intForMonth, redOfPrincipal, endBalance)

main() #main함수 호출