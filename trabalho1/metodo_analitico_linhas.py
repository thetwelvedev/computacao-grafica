#import matplotlib.pyplot as plt
#import numpy as np

def menu():
    num_linha, num_coluna = map(int, input("Escolha o tamanho da matriz(ex: 3x3): ").split("x"))
    matriz = gerar_matriz_de_pixels(num_linha, num_coluna)

    print("\nDefina os pontos da linha:")
    x1, y1 = map(int, input("Digite o p1 (ex: 1,1): ").split(","))
    x2, y2 = map(int, input("Digite o p2 (ex: 3,3): ").split(","))

    gerar_reta(x1, y1, x2, y2, matriz)
    print("\nResultado:")
    mostrar_matriz(matriz)

def gerar_matriz_de_pixels(num_linha, num_coluna):
    matriz = []
    for i in range(num_linha):
        linha = []
        for j in range(num_coluna):
            linha.append("⬜")
        matriz.append(linha)
    return matriz

def mostrar_matriz(matriz):
    for linha in reversed(matriz): # inverte fazendo o pixel 0,0 ser o do canto inferior esquerdo
        print(" ".join(linha))  # Deixa mais bonito (sem colchetes)

def liga_pixel(x, y, matriz):
    if 0 <= y < len(matriz) and 0 <= x < len(matriz[0]): #Verifica se tá dentro da matriz
        matriz[y][x] = "⬛" 

def gerar_reta(x1, y1, x2, y2, matriz):
    if x1 == x2:
        for y in range(y1, y2 + 1): #Vai pecorrer a distância da diferença dos pontos em relação ao y
            liga_pixel(x1, y, matriz)
    else: #caso não seja vertical
        m = (y2 - y1) / (x2 - x1) #coeficiente angular
        b = y1 - m*x1 #coeficiente linear
        for x in range(x1, x2 + 1): #Vai pecorrer a distância da diferença dos pontos em relação ao x
            y = int(round(m * x + b)) #Vai pegar o valor de y para cada ponto entre x1 e x2 e arredondar
            liga_pixel(x, y, matriz) #liga_pixel(x, y, cor)

menu()