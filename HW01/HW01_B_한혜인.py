#first_salary 입력받음
first_salary=int(input("Enter beginning salary: "))

#5퍼센트씩 증가하는 salary 계산
second_salary=first_salary+first_salary*0.05
third_salary=second_salary+second_salary*0.05
fourth_salary=third_salary+third_salary*0.05
fifth_salary=fourth_salary+fourth_salary*0.05

#first_salary, fifth_salary 변화량을 백분율로 계산
change=(fifth_salary-first_salary)/first_salary*100

#출력
print("New salary: ${:,.2f}".format(fifth_salary))
print("Change: {:.2f}%".format(change))