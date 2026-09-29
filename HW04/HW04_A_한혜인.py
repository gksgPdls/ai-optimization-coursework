class Quizzes:
    def __init__(self, listOfGrades):
        #생성자 함수
        self.listOfGrades=listOfGrades

    def average(self): #calculates the average of grades.
        #self.listOfGrades의 값 중 최소값을 제외한 평균을 계산하여 반환
        return (sum(self.listOfGrades)-min(self.listOfGrades))/5
    
    def __str__(self): #returns as shown in the example I/O
        #객체 출력
        return f"Quiz average: {self.average():.1f}"

def main():
    #declares an empty list listOfGrades
    listOfGrades=[]

    for i in range(1, 7):
        #request 6 quiz grades as inputs
        grade=float(input("Enter grade on quiz {}: ".format(i)))
        #appends each of them to listOfGrades
        listOfGrades.append(grade)

    #prints Quizzes(listOfGrades)
    q = Quizzes(listOfGrades)
    print(q)

main()