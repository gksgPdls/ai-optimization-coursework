#Use random library to implement Computer.makeChoice method.
import random

class Contestant:
    #initializer of the class Contestant.
    def __init__(self, name="", score=0):
        #생성자 함수
        self.name=name
        self.score=score

    #accessor of each local variable.
    def getName(self):
        #self.name 반환
        return self.name

    #accessor of each local variable.
    def getScore(self):
        #self.score 반환
        return self.score
    
    #mutator of each local variable.
    def setScore(self,value):
        #self.score를 value로 설정
        self.score=value

class Human(Contestant):
    #Human requests a choice and returns it.
    def makeChoice(self):
        #사용자로부터 choice 입력받음
        choice=input("{}, enter your choice: ".format(self.name))
        #사용자가 "rock", "scissors", "paper" 중 하나를 입력할 때까지 반복
        while choice not in ["rock", "scissors", "paper"]:
            print("invalid choice {}".format(choice)) #오류 문자 출력
            choice=input("{}, enter your choice: ".format(self.name))
            
        return choice #Human의 choice 반환

class Computer(Contestant):
    #Computer randomly makes the choice and returns it.
    def makeChoice(self):
        #무작위로 "rock", "scissors", "paper" 중 하나를 선택
        choice=random.choice(["rock", "scissors", "paper"])
        print("{} chooses {}".format(self.name, choice))
        return choice #Computer의 choice 반환

def playGame(h, c):
    choiceH = h.makeChoice()
    choiceC = c.makeChoice()
    if choiceH == choiceC:
        pass
    elif judge(choiceH, choiceC):
        h.setScore(h.getScore() + 1)
    else:
        c.setScore(c.getScore() + 1)

def judge(choiceH, choiceC):
    if ((choiceH == 'rock' and choiceC == 'scissors') or (choiceH == 'paper' and choiceC == 'rock') or (choiceH == 'scissors' and choiceC == 'paper')):
        return True
    else:
        return False
    
def main():
    #사용자로부터 human과 computer의 이름을 입력받음
    human=input("Enter name of human: ")
    computer=input("Enter name of computer: ")
    #Human과 Computer 객체 생성
    h=Human(human)
    c=Computer(computer)

    #playGame 3회 진행
    for i in range(3):
        playGame(h, c)
        print("{}: {}, {}: {}".format(h.getName(), h.getScore(), c.getName(), c.getScore()))
    
    #최종 승자 출력
    if h.getScore()>c.getScore():
        print("{} WIN".format(h.getName()))
    elif h.getScore()<c.getScore():
        print("{} WIN".format(c.getName()))
    else:
        #동점일 경우 무승부 출력
        print("TIE")
    
main()