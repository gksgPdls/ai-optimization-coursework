class Fraction():
    #Initializer of the class Fraction
    def __init__(self, numerator=0, denominator=1):
        #생성자 함수
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise ValueError("Numerator and Denominator must be integers.")
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator=numerator
        self.denominator=denominator

    #accessor of each local variable.
    def getNumerator(self):
        #self.numerator 반환
        return self.numerator

    #mutator of each local variable.    
    def setNumerator(self, value):
        #self.numerator를 value로 설정
        self.numerator=value

    #accessor of each local variable.   
    def getDenominator(self):
        #self.denominator 반환
        return self.denominator

    #mutator of each local variable.    
    def setDenominator(self, value):
        if value == 0:
            raise ValueError("Denominator cannot be zero.")
        #self.denominator를 value로 설정
        self.denominator=value

    #print the Fraction class like example I/O below.    
    def print(self):
        #fraction의 현재 상태 출력
        print("The fraction is {}/{}".format(self.numerator, self.denominator))

class IrreducibleFraction(Fraction):
    #Initializer of the class IrreducibleFraction.
    def __init__(self, numerator=0, denominator=1):
        #Fraction의 생성자를 호출하여 초기화
        super().__init__(numerator, denominator) #use super() function
        #gcd를 self.numerator와 self.denominator에 각각 나누어 계산
        gcd=self._GCD(self.numerator, self.denominator)
        self.numerator=self.numerator//gcd
        self.denominator=self.denominator//gcd

    #returns the greatest common divisor (GCD) of two nonzero integers.
    def _GCD(self, m, n):
        #m과 n 중 작은 수에서 1씩 감소
        for i in range(min(m, n), 1, -1):
            #두 수의 gcd를 찾아서 반환
            if m%i==0 and n%i==0:
                return i
        return 1 #없으면 1을 반환
    
    #print the IrreducibleFraction like example I/O below.
    def print(self):
        #fraction의 약분된 상태 출력
        print("The reduced fraction is {}/{}".format(self.numerator, self.denominator))

def main():
    numerator = eval(input('Enter the Numerator: '))
    denominator = eval(input('Enter the Denominator: '))
    fraction = Fraction(numerator, denominator)
    fraction.print()
    reduced_fraction = IrreducibleFraction(numerator, denominator)
    reduced_fraction.print()

main()