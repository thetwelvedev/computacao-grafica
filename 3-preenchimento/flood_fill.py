import numpy as np
import matplotlib.pyplot as plt

def main():
    largura, altura = 50, 50
    matriz = np.zeros((altura, largura), dtype=int)

    print("Escolha a figura a desenhar:")
    print("1 - Retângulo")
    print("2 - Circunferência")
    print("3 - Polígono A")
    print("4 - Polígono C")
    opcao = int(input("Opção: "))

    if opcao == 1:
        x1, y1 = 10, 10
        x2, y2 = 30, 25
        desenhar_retangulo(matriz, x1, y1, x2, y2)
        mostrar_matriz(matriz, "Retângulo - Antes do preenchimento")
        flood_fill(matriz, 20, 15, 0, 2)   #semente(xc,yc)
        mostrar_matriz(matriz, "Retângulo - Depois do preenchimento")

    elif opcao == 2:
        xc, yc, r = 25, 25, 10 #semente(xc,yc)
        gerar_circunferencia_bresenham(xc, yc, r, matriz)
        mostrar_matriz(matriz, "Circunferência - Antes do preenchimento")
        flood_fill(matriz, xc, yc, 0, 2)
        mostrar_matriz(matriz, "Circunferência - Depois do preenchimento")
    elif opcao == 3:
        xc, yc = 20, 17 #Semente
        gerar_poligono_a(matriz)
        mostrar_matriz(matriz, "Polígono A - Antes do preenchimento")
        flood_fill(matriz, xc, yc, 0, 2)
        mostrar_matriz(matriz, "Polígono A - Depois do preenchimento")

    elif opcao == 4:
        xc, yc = 20, 23  #semente
        gerar_poligono_c(matriz)
        mostrar_matriz(matriz, "Polígono C - Antes do preenchimento")
        flood_fill(matriz, xc, yc, 0, 2)
        mostrar_matriz(matriz, "Polígono C - Depois do preenchimento")
       
    else:
        print("Opção inválida!")

def desenhar_retangulo(matriz, x1, y1, x2, y2, cor=1):
    matriz[y1:y2, x1] = cor
    matriz[y1:y2, x2] = cor
    matriz[y1, x1:x2+1] = cor
    matriz[y2, x1:x2+1] = cor

def gerar_circunferencia_bresenham(xc, yc, r, matriz, cor=1):
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        liga_pixel(x + xc, y + yc, matriz, cor)
        liga_pixel(y + xc, x + yc, matriz, cor)
        liga_pixel(-y + xc, x + yc, matriz, cor)
        liga_pixel(-x + xc, y + yc, matriz, cor)
        liga_pixel(-x + xc, -y + yc, matriz, cor)
        liga_pixel(-y + xc, -x + yc, matriz, cor)
        liga_pixel(y + xc, -x + yc, matriz, cor)
        liga_pixel(x + xc, -y + yc, matriz, cor)

        if p >= 0:
            y -= 1
            p += 2 * x - 2 * y + 5
        else:
            p += 2 * x + 3
        x += 1

def gerar_poligono_a(matriz, cor=1):
    vertices = [
        (15, 12),  # inferior esquerdo
        (30, 13),  # inferior direito
        (32, 15),  # meio direito
        (20, 23),  # topo
        (10, 20),  # topo esquerdo
        (18, 15)   # meio esquerdo
    ]

    # Conecta os vértices em sequência e fecha o polígono
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        gerar_reta_bresenham(x1, y1, x2, y2, matriz, cor)

def gerar_poligono_c(matriz, cor=1):
    vertices = [
        (10, 30),  # canto superior esquerdo
        (10, 24),  # descendo esquerda
        (20, 17),  # parte inferior central
        (30, 24),  # subindo direita
        (30, 30),  # canto superior direito
        (24, 30),  # topo interno direito
        (20, 28),  # centro superior
        (16, 30)   # topo interno esquerdo
    ]

    # Conecta os vértices e fecha o polígono
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        gerar_reta_bresenham(x1, y1, x2, y2, matriz, cor)

def gerar_reta_bresenham(x1, y1, x2, y2, matriz, cor=1):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    trocado = False

    # Se a inclinação é maior que 1, troca x e y
    if dy > dx:
        dx, dy = dy, dx
        trocado = True
        x1, y1 = y1, x1  # troca as coordenadas de início
        x2, y2 = y2, x2  # troca as coordenadas de fim
        sx, sy = sy, sx  # troca também as direções

    p = 2 * dy - dx
    x, y = x1, y1

    for _ in range(dx + 1):
        if trocado:
            liga_pixel(y, x, matriz, cor)
        else:
            liga_pixel(x, y, matriz, cor)

        if p >= 0:
            y += sy
            p -= 2 * dx
        p += 2 * dy
        x += sx

def liga_pixel(x, y, matriz, cor=1):
    if 0 <= x < matriz.shape[1] and 0 <= y < matriz.shape[0]:
        matriz[y, x] = cor

def mostrar_matriz(matriz, titulo="Imagem"):
    plt.imshow(matriz, cmap="gray", origin="lower")
    plt.title(titulo)
    plt.show()

def flood_fill(matriz, x, y, cor, novaCor):
    if matriz[y, x] == cor:
        matriz[y, x] = novaCor
        flood_fill(matriz, x + 1, y, cor, novaCor)
        flood_fill(matriz, x - 1, y, cor, novaCor)
        flood_fill(matriz, x, y + 1, cor, novaCor)
        flood_fill(matriz, x, y - 1, cor, novaCor)

if __name__ == "__main__":
    main()
