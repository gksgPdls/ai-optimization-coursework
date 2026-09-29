#sum을 0으로 초기화
sum=0

#1부터 1000000까지의 홀수에 대해
for odd in range(1, 1000000, 2):
        #각 홀수의 자릿수를 str로 변환 -> 다시 int로 변환 후 더함
        for digit in str(odd):
                digit_sum=0
                digit_sum=digit_sum+int(digit)
                sum=sum+digit_sum

#출력
print("The sum of the digits of odd numbers\nFrom 1 to one million is {:,}.".format(sum))