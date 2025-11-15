import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi

def menu():
    num_linha, num_coluna = map(int, input("Escolha o tamanho da matriz (ex: 20x20): ").split("x"))
    matriz = gerar_matriz_de_pixels(num_linha, num_coluna)

    print("\nDefina o centro e o raio da circunferência (use coordenadas cartesianas):")
    print(f"Intervalo X: [{-num_coluna//2}, {num_coluna//2}]")
    print(f"Intervalo Y: [{-num_linha//2}, {num_linha//2}]")
    xc, yc = map(int, input("Digite o centro (ex: 0,0): ").split(","))
    r = int(input("Digite o raio: "))

    gerar_circunferencia(xc, yc, r, matriz, num_linha, num_coluna)
    print("\nResultado:")
    mostrar_matriz_terminal(matriz, num_linha, num_coluna)
    
    print("\nGerando visualização gráfica...")
    mostrar_matriz_grafica(matriz, xc, yc, r, num_linha, num_coluna)

def gerar_matriz_de_pixels(num_linha, num_coluna):
    matriz = []
    for i in range(num_linha):
        linha = []
        for j in range(num_coluna):
            linha.append(0)  # 0 = pixel desligado
        matriz.append(linha)
    return matriz

def cartesiano_para_matriz(x_cart, y_cart, num_linhas, num_colunas):
    """Converte coordenadas cartesianas para índices da matriz"""
    x_matriz = x_cart + num_colunas // 2
    y_matriz = y_cart + num_linhas // 2
    return x_matriz, y_matriz

def liga_pixel(x_cart, y_cart, matriz, num_linhas, num_colunas):
    x_matriz, y_matriz = cartesiano_para_matriz(x_cart, y_cart, num_linhas, num_colunas)
    if 0 <= y_matriz < num_linhas and 0 <= x_matriz < num_colunas:
        matriz[y_matriz][x_matriz] = 1  # 1 = pixel ligado

def mostrar_matriz_terminal(matriz, num_linhas, num_colunas):
    print("\nMapa de pixels no terminal:")
    for linha in reversed(matriz):
        print(" ".join(["⬛" if pixel else "⬜" for pixel in linha]))

def mostrar_matriz_grafica(matriz, xc, yc, r, num_linhas, num_colunas):
    fig, ax = plt.subplots(figsize=(12, 10))
    matriz_visual = np.array(matriz)
    
    # Calcula os limites do plano cartesiano
    x_min = -num_colunas // 2
    x_max = num_colunas // 2
    y_min = -num_linhas // 2
    y_max = num_linhas // 2
    
    # Mostra a matriz com coordenadas cartesianas
    ax.imshow(matriz_visual, cmap='gray_r', origin='lower', 
              extent=[x_min, x_max, y_min, y_max], aspect='equal')
    
    # Grid nas coordenadas cartesianas
    x_ticks = range(x_min, x_max + 1)
    y_ticks = range(y_min, y_max + 1)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.grid(True, color='lightgray', linewidth=0.5, alpha=0.7)
    
    # Destaca os eixos X e Y (origem)
    ax.axhline(y=0, color='blue', linewidth=2, alpha=0.7, label='Eixo X')
    ax.axvline(x=0, color='red', linewidth=2, alpha=0.7, label='Eixo Y')
    
    # Marca o centro da circunferência
    ax.plot(xc + 0.5, yc + 0.5, 'ro', markersize=15, label=f'Centro ({xc}, {yc})', zorder=5)
    
    # Desenha uma linha do centro até a borda (raio)
    x_raio = xc + r * cos(pi/4)
    y_raio = yc + r * sin(pi/4)
    ax.plot([xc + 0.5, x_raio + 0.5], [yc + 0.5, y_raio + 0.5], 
            'g--', linewidth=2, label=f'Raio = {r}', zorder=4)
    
    # Adiciona rótulos dos quadrantes
    offset_x = (x_max - x_min) * 0.4
    offset_y = (y_max - y_min) * 0.4
    ax.text(offset_x, offset_y, 'Q1', fontsize=20, fontweight='bold', 
            color='navy', alpha=0.3, ha='center', va='center')
    ax.text(-offset_x, offset_y, 'Q2', fontsize=20, fontweight='bold', 
            color='navy', alpha=0.3, ha='center', va='center')
    ax.text(-offset_x, -offset_y, 'Q3', fontsize=20, fontweight='bold', 
            color='navy', alpha=0.3, ha='center', va='center')
    ax.text(offset_x, -offset_y, 'Q4', fontsize=20, fontweight='bold', 
            color='navy', alpha=0.3, ha='center', va='center')
    
    # Marca a origem se não for o centro
    if xc != 0 or yc != 0:
        ax.plot(0, 0, 'ko', markersize=10, zorder=5)
        ax.text(0.5, 0.5, 'O(0,0)', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Eixo X', fontsize=14, fontweight='bold')
    ax.set_ylabel('Eixo Y', fontsize=14, fontweight='bold')
    ax.set_title(f'Rasterização de Circunferência: Centro({xc},{yc}), Raio={r}', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_min - 0.5, y_max + 0.5)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    info_text = f'Matriz: {num_linhas}×{num_colunas}\nCoordenadas Cartesianas\nX: [{x_min}, {x_max}]\nY: [{y_min}, {y_max}]'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.tight_layout()
    plt.show()

def gerar_circunferencia(xc, yc, r, matriz, num_linhas, num_colunas):
    x = 0
    y = r
    p = 1 - r #parâmetro de decisão

    while x <= y:
        liga_pixel(x + xc, y + yc, matriz, num_linhas, num_colunas)#usa os octantes para ativar
        liga_pixel(y + xc, x + yc, matriz, num_linhas, num_colunas)
        liga_pixel(-y + xc, x + yc, matriz, num_linhas, num_colunas)
        liga_pixel(-x + xc, y + yc, matriz, num_linhas, num_colunas)
        liga_pixel(-x + xc, -y + yc, matriz, num_linhas, num_colunas)
        liga_pixel(-y + xc, -x + yc, matriz, num_linhas, num_colunas)
        liga_pixel(y + xc, -x + yc, matriz, num_linhas, num_colunas)
        liga_pixel(x + xc, -y + yc, matriz, num_linhas, num_colunas)
        if p >= 0:
            y -= 1
            p += 2*x - 2*y + 5 
            x += 1

        else:
            p += 2*x + 3
            x += 1

if __name__ == "__main__":
    menu()