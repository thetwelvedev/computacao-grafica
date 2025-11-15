import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

def menu():
    num_linha, num_coluna = map(int, input("Escolha o tamanho da matriz(ex: 3x3): ").split("x"))
    matriz = gerar_matriz_de_pixels(num_linha, num_coluna)

    print("\nDefina os pontos da linha:")
    x1, y1 = map(int, input("Digite o p1 (ex: 1,1): ").split(","))
    x2, y2 = map(int, input("Digite o p2 (ex: 3,3): ").split(","))

    gerar_reta(x1, y1, x2, y2, matriz)
    print("\nResultado:")
    mostrar_matriz_terminal(matriz)
    
    print("\nGerando visualização gráfica...")
    mostrar_matriz_grafica(matriz, x1, y1, x2, y2)

def gerar_matriz_de_pixels(num_linha, num_coluna):
    matriz = []
    for i in range(num_linha):
        linha = []
        for j in range(num_coluna):
            linha.append(0)  # 0 = pixel desligado
        matriz.append(linha)
    return matriz

def liga_pixel(x, y, matriz):
    if 0 <= y < len(matriz) and 0 <= x < len(matriz[0]):
        matriz[y][x] = 1  # 1 = pixel ligado

def mostrar_matriz_grafica(matriz, x1, y1, x2, y2):
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    matriz_visual = np.array(matriz)
    
    ax.imshow(matriz_visual, cmap='gray_r', origin='lower', 
              extent=[0, num_colunas, 0, num_linhas])
    
    ax.set_xticks(range(num_colunas + 1))
    ax.set_yticks(range(num_linhas + 1))
    ax.grid(True, color='gray', linewidth=1, alpha=0.7)
    
    ax.plot(x1 + 0.5, y1 + 0.5, 'go', markersize=15, label=f'P1 ({x1}, {y1})', zorder=5)
    ax.plot(x2 + 0.5, y2 + 0.5, 'ro', markersize=15, label=f'P2 ({x2}, {y2})', zorder=5)
    
    ax.annotate('', xy=(num_colunas + 0.3, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.annotate('', xy=(0, num_linhas + 0.3), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    ax.text(num_colunas + 0.5, -0.3, 'X', fontsize=16, fontweight='bold', ha='center')
    ax.text(-0.3, num_linhas + 0.5, 'Y', fontsize=16, fontweight='bold', va='center')
    
    ax.set_xlabel('Eixo X', fontsize=14, fontweight='bold')
    ax.set_ylabel('Eixo Y', fontsize=14, fontweight='bold')
    ax.set_title(f'Rasterização de Linha de P1({x1},{y1}) até P2({x2},{y2})', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.set_xlim(-0.5, num_colunas + 1)
    ax.set_ylim(-0.5, num_linhas + 1)
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    
    info_text = f'Matriz: {num_linhas}x{num_colunas}'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def mostrar_matriz_terminal(matriz):
    print("\nResultado no terminal:")
    for linha in reversed(matriz):
        print(" ".join(["⬛" if pixel else "⬜" for pixel in linha]))

def gerar_reta(x1, y1, x2, y2, matriz):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    #Aqui são responsaveis por mudar quando estão no octantes 1,4,5 e 8
    sx = 1 if x1 < x2 else -1  # direção de incremento em x
    sy = 1 if y1 < y2 else -1  # direção de incremento em y
    trocado = False

    if dy > dx: #aqui ocorre a troca de x por y pois pertencem algum octante sendo o 2,3,6 ou 7
        dx, dy = dy, dx
        trocado = True

    p = 2 * dy - dx
    x, y = x1, y1

    for i in range(dx + 1):
        if trocado:
            liga_pixel(y, x, matriz)
        else:
            liga_pixel(x, y, matriz)

        if p >= 0:
            y += sy
            p -= 2 * dx
        p += 2 * dy
        x += sx

def arredondar(y):
    if y >= 0:
        return floor(y + 0.5) #aqui é paa números inteiros, quando for mas que 0.5 vai para próxima casa decimal e arredonda para baixo se for menor ou igual que 0.4 vai ficar no máximo 0.9 então vai para casa decimal anterior
    else:
        return ceil(y - 0.5)

if __name__ == "__main__":
    menu()