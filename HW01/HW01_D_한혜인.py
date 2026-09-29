#coefficient_of_restitution, initial_height 입력받음
coefficient_of_restitution=float(input("Enter coefficient of restitution: "))
initial_height=float(input("Enter initial height in meters: "))

#각 변수들 초기화
current_height=initial_height
number_of_bounce=0
meters_traveled=0

#current_height가 10cm 이상일 때까지 반복
while current_height>=0.1:
    #첫 번째 바운스
    if number_of_bounce<1:
        meters_traveled=current_height
    else:
        meters_traveled=meters_traveled+current_height*2
    
    #current_height, number_of_bounce 갱신
    current_height=current_height*coefficient_of_restitution
    number_of_bounce=number_of_bounce+1

#출력
print("Number of bounces: {}".format(number_of_bounce))
print("Meters traveled: {:.2f}".format(meters_traveled))