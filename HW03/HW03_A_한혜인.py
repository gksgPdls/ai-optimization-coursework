import os.path

#read set from Names.txt. If the file does not exist, exit.
def readSetFromFile():
    #os.path.isfile method를 사용하여 파일이 존재하는지 확인
    if not os.path.isfile('Names.txt'):
        #파일이 없다면 메세지 출력
        print("Name.txt does not exist.\nTerminate program.")
        #exit function 사용
        exit()
    
    #읽기 모드로 파일 열기
    with open('Names.txt', 'r') as file:
        #set operations을 사용하여 줄 단위로 읽어와 set으로 변환
        name=set(file.read().splitlines())

    return name #set을 반환

#input the name from the terminal.
def inputName():

    return input("Enter a first name to be included: ") #사용자의 입력을 반환

#insert the name into set.
def insertSet(mySet, name):
    #set에 이름이 있다면 메세지 출력
    if name in mySet:
        print("{} is already in Names.txt".format(name))
    #set에 이름이 없다면 추가하고 메세지 출력
    else:
        print("{} is added in Names.txt".format(name))
        #set operations 사용
        mySet.add(name)

    return mySet #수정된 set을 반환

#write set to Names.txt.
def writeToFile(modifiedSet):
    #쓰기 모드로 파일 열기
    with open('Names.txt', 'w') as file:
        #정렬된 set에 이름 쓰기
        for name in sorted(modifiedSet):
            file.write(name + '\n')

def main():
    mySet = readSetFromFile()
    name = inputName()
    modifiedSet = insertSet(mySet, name)
    writeToFile(modifiedSet)

main()