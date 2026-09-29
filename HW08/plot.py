import matplotlib.pyplot as plt  

def read_data(filename):
    iterations = []  # 반복 횟수를 저장할 리스트
    values = []  # 각 반복에서의 값을 저장할 리스트
    with open(filename, 'r') as f:  # 파일을 읽기 모드로 열어
        for line in f:  # 파일의 각 줄을 돌면서
            iteration, value = line.strip().split(',')  # 쉼표로 분리해서 반복 횟수와 값을 가져옴
            iterations.append(int(iteration))  # 반복 횟수를 정수로 변환해서 리스트에 추가
            values.append(float(value))  # 값을 실수로 변환해서 리스트에 추가
    return iterations, values  # 반복 횟수와 값의 리스트를 반환

def plot_data():
    first_iterations, first_values = read_data('first.txt')  # First Choice 데이터 읽어옴
    anneal_iterations, anneal_values = read_data('anneal.txt')  # Simulated Annealing 데이터 읽어옴

    plt.figure(figsize=(10, 5))  # 그래프 크기 설정
    plt.plot(first_iterations, first_values, label='First Choice Hill Climbing')  # First Choice 그래프 그림
    plt.plot(anneal_iterations, anneal_values, label='Simulated Annealing')  # Simulated Annealing 그래프 그림
    plt.xlabel('Iteration')  # x축 레이블 설정
    plt.ylabel('Objective Value')  # y축 레이블 설정
    plt.title('Objective Value by Iteration for First Choice and Simulated Annealing')  # 그래프 제목 설정
    plt.legend()  # 범례 표시
    plt.grid(True)  # 그리드 표시
    plt.savefig('comparison_plot.png')  # 그래프를 파일로 저장
    plt.show()  # 그래프 표시

if __name__ == '__main__':
    plot_data()  # 데이터를 읽고 그래프 그리는 함수 실행