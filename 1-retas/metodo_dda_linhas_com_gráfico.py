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
    
    # Criar figura e eixo
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Criar matriz para visualização
    matriz_visual = np.array(matriz)
    
    # Plotar a matriz como imagem (origin='lower' faz (0,0) ficar embaixo à esquerda)
    ax.imshow(matriz_visual, cmap='gray_r', origin='lower', 
              extent=[0, num_colunas, 0, num_linhas])
    
    # Configurar grid para mostrar cada pixel (de 1 em 1)
    ax.set_xticks(range(num_colunas + 1))
    ax.set_yticks(range(num_linhas + 1))
    ax.grid(True, color='gray', linewidth=1, alpha=0.7)
    
    # Marcar os pontos P1 (verde) e P2 (vermelho) - centrados em cada pixel
    ax.plot(x1 + 0.5, y1 + 0.5, 'go', markersize=15, label=f'P1 ({x1}, {y1})', zorder=5)
    ax.plot(x2 + 0.5, y2 + 0.5, 'ro', markersize=15, label=f'P2 ({x2}, {y2})', zorder=5)
    
    # Desenhar setas nos eixos começando de (0,0)
    ax.annotate('', xy=(num_colunas + 0.3, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.annotate('', xy=(0, num_linhas + 0.3), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Labels dos eixos
    ax.text(num_colunas + 0.5, -0.3, 'X', fontsize=16, fontweight='bold', ha='center')
    ax.text(-0.3, num_linhas + 0.5, 'Y', fontsize=16, fontweight='bold', va='center')
    
    ax.set_xlabel('Eixo X', fontsize=14, fontweight='bold')
    ax.set_ylabel('Eixo Y', fontsize=14, fontweight='bold')
    ax.set_title(f'Rasterização de Linha de P1({x1},{y1}) até P2({x2},{y2})', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Ajustar limites começando de (0,0)
    ax.set_xlim(-0.5, num_colunas + 1)
    ax.set_ylim(-0.5, num_linhas + 1)
    
    # Adicionar legenda
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    
    # Adicionar informações da matriz
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
    dx = x2 - x1
    dy = y2 - y1

    if dx > dy: #aqui eu vou verificar se vou ter que preencher os espaços horizontalmente
        inc = dy/dx #O incremento sempre é a razão entre a menor diferença pela maior diferença
        y = y1 #aqui atribuo dessa forma para y começar do inicio 
        for x in range(x1, x2 + 1): #aqui usamos o sinal para definir para qual sentido vai se é da  esquerda para a direita ou da direita para a esquerda
            liga_pixel(x, arredondar(y), matriz)
            y += inc 
    else : #aqui vai preencher verticalmente pois é maior verticalmente
        inc = dx/dy
        x = x1
        for y in range(y1, y2 + 1): 
            liga_pixel(arredondar(x), y, matriz)
            x += inc 

def arredondar(y):
    if y >= 0:
        return floor(y + 0.5) #aqui é paa números inteiros, quando for mas que 0.5 vai para próxima casa decimal e arredonda para baixo se for menor ou igual que 0.4 vai ficar no máximo 0.9 então vai para casa decimal anterior
    else:
        return ceil(y - 0.5)

if __name__ == "__main__":
    menu()