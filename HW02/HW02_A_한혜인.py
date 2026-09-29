#measurements 입력받음
measurements=eval(input("Enter measurements as a list: "))
#리스트 정렬
measurements.sort()
#리스트 길이 계산
n=len(measurements)

#n이 홀수인지 짝수인지에 따라 median 계산
if n%2==1:
    median=measurements[(n-1)//2]
else:
    median=(measurements[n//2-1]+measurements[n//2])/2

#format method 사용하여 출력
print("Median: {:.1f}".format(median))