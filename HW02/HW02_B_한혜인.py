#five-digit number에 대해
for i in range(10000, 100000):
    #int를 str로 변환, 각 자릿수를 리스트로 변환
    number=list(str(i))
    #reverse method
    number.reverse()
    #join method
    number_str=''.join(number)

    #number_str 다시 int로 변환 후 비교
    if i*4==int(number_str):
        #format method 사용하여 출력
        print("Since 4 * {} is {},\nThe special number is {}.".format(i, number_str, i))
