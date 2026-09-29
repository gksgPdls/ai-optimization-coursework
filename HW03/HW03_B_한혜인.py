#create dictionary from Units.txt to convert units.
def populateDictionary():
    #dictionary operations 사용
    dict={}
    try:
        #읽기 모드로 파일 열기
        with open('Units.txt', 'r') as file:
            #파일에서 각 줄을 순회
            for line in file:
                #unit과 feet 값을 ','로 분리
                unit, feet=line.strip().split(',')
                #{unit: feet}로 dict에 저장
                dict[unit]=float(feet)
    #파일이 존재하지 않을 때 예외처리
    except FileNotFoundError:
        print("Units.txt 파일이 없습니다.")
        #메세지 출력 후 프로그램 종료
        exit()

    return dict #dict 반환

#Input units and length from the terminal.
def getInput():
    #orig, dest 입력받음
    orig=input("Unit to convert from: ")
    dest=input("Unit to convert to: ")
    #length 입력받아 실수로 변환
    length=float(input("Enter length in {}: ".format(orig)))

    return orig, dest, length #사용자의 입력을 반환

def main():
    feet = populateDictionary()
    orig, dest, length = getInput()
    answer = length * feet[orig] / feet[dest]
    print("Length in {0}: {1:,.4f}".format(dest, answer))

main()