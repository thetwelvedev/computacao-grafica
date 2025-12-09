import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

def menu():
    num_linha, num_coluna = map(int, input("Escolha o tamanho da matriz (ex: 40x40): ").split("x"))
    matriz = gerar_matriz_de_pixels(num_linha, num_coluna)

    print("\nDefina os pontos de controle da curva de Bézier CÚBICA:")
    print(f"Intervalo X: [{-num_coluna//2}, {num_coluna//2}]")
    print(f"Intervalo Y: [{-num_linha//2}, {num_linha//2}]")

    x0, y0 = map(int, input("P0 (ex: -15,0): ").split(","))
    x1, y1 = map(int, input("P1 (ex: -5,15): ").split(","))
    x2, y2 = map(int, input("P2 (ex: 5,-15): ").split(","))
    x3, y3 = map(int, input("P3 (ex: 15,0): ").split(","))

    P0 = (x0, y0)
    P1 = (x1, y1)
    P2 = (x2, y2)
    P3 = (x3, y3)

    casteljau(P0, P1, P2, P3, matriz, num_linha, num_coluna)

    print("\nResultado:")
    mostrar_matriz_terminal(matriz, num_linha, num_coluna)

    print("\nGerando visualização gráfica...")
    mostrar_matriz_grafica(matriz, P0, P1, P2, P3, num_linha, num_coluna)

def gerar_matriz_de_pixels(num_linha, num_coluna):
    return [[0 for _ in range(num_coluna)] for _ in range(num_linha)]

def cartesiano_para_matriz(x_cart, y_cart, num_linhas, num_colunas):
    x_matriz = x_cart + num_colunas // 2
    y_matriz = y_cart + num_linhas // 2
    return x_matriz, y_matriz

def liga_pixel(x_cart, y_cart, matriz, num_linhas, num_colunas):
    x_matriz, y_matriz = cartesiano_para_matriz(x_cart, y_cart, num_linhas, num_colunas)
    if 0 <= y_matriz < num_linhas and 0 <= x_matriz < num_colunas:
        matriz[y_matriz][x_matriz] = 1

def mostrar_matriz_terminal(matriz, num_linhas, num_colunas):
    print("\nMapa de pixels:")
    for linha in reversed(matriz):
        print(" ".join(["⬛" if pixel else "⬜" for pixel in linha]))

def mostrar_matriz_grafica(matriz, P0, P1, P2, P3, num_linhas, num_colunas):
    fig, ax = plt.subplots(figsize=(10, 10))
    matriz_np = np.array(matriz)

    x_min = -num_colunas // 2
    x_max = num_colunas // 2
    y_min = -num_linhas // 2
    y_max = num_linhas // 2

    ax.imshow(matriz_np, cmap='gray_r', origin='lower',
              extent=[x_min, x_max, y_min, y_max], aspect='equal')

    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    ax.grid(True, color='lightgray', linewidth=0.5)

    # Pontos de controle
    ax.plot(P0[0], P0[1], 'ro', markersize=10, label="P0")
    ax.plot(P1[0], P1[1], 'bo', markersize=10, label="P1")
    ax.plot(P2[0], P2[1], 'go', markersize=10, label="P2")
    ax.plot(P3[0], P3[1], 'mo', markersize=10, label="P3")

    # Linhas de controle
    ax.plot([P0[0], P1[0]], [P0[1], P1[1]], 'r--')
    ax.plot([P1[0], P2[0]], [P1[1], P2[1]], 'b--')
    ax.plot([P2[0], P3[0]], [P2[1], P3[1]], 'g--')

    ax.axhline(0, color='blue')
    ax.axvline(0, color='red')

    ax.legend()
    ax.set_title("Curva de Bézier CÚBICA")

    plt.show()

def distancia(p1, p2):
    """Calcula a distância euclidiana entre dois pontos"""
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def ponto_medio(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def casteljau(P0, P1, P2, P3, matriz, num_linhas, num_colunas, tolerancia=1.0):
    #Critério de parada: se a distância entre o primeiro e último ponto for pequena
    dist = distancia(P0, P3)
    
    if dist < tolerancia:
        #Liga os pixels ao longo da linha reta entre P0 e P3
        liga_pixel(int(round(P0[0])), int(round(P0[1])), matriz, num_linhas, num_colunas)
        liga_pixel(int(round(P3[0])), int(round(P3[1])), matriz, num_linhas, num_colunas)
        return
    
    #Primeira subdivisão: pontos médios do polígono de controle
    P01 = ponto_medio(P0, P1)
    P12 = ponto_medio(P1, P2)
    P23 = ponto_medio(P2, P3)
    
    #Segunda subdivisão: pontos médios dos pontos médios
    P012 = ponto_medio(P01, P12)
    P123 = ponto_medio(P12, P23)
    
    #Terceira subdivisão: ponto final que divide a curva
    P0123 = ponto_medio(P012, P123)
    
    #Liga o pixel do ponto de subdivisão
    liga_pixel(arredondar(P0123[0]), arredondar(P0123[1]), matriz, num_linhas, num_colunas)
    
    #Recursão para o lado esquerdo: P0, P01, P012, P0123
    casteljau(P0, P01, P012, P0123, matriz, num_linhas, num_colunas, tolerancia)
    
    #Recursão para o lado direito: P0123, P123, P23, P3
    casteljau(P0123, P123, P23, P3, matriz, num_linhas, num_colunas, tolerancia)

def arredondar(y):
    if y >= 0:
        return floor(y + 0.5) #aqui é paa números inteiros, quando for mas que 0.5 vai para próxima casa decimal e arredonda para baixo se for menor ou igual que 0.4 vai ficar no máximo 0.9 então vai para casa decimal anterior
    else:
        return ceil(y - 0.5)

if __name__ == "__main__":
    menu()