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
        preencher_retangulo(matriz, x1, y1, x2, y2, 2)
        mostrar_matriz(matriz, "Retângulo - Depois do preenchimento")

    elif opcao == 2:
        xc, yc, r = 25, 25, 10
        gerar_circunferencia_bresenham(xc, yc, r, matriz)
        mostrar_matriz(matriz, "Circunferência - Antes do preenchimento")
        preencher_circunferencia(matriz, xc, yc, r, 2)
        mostrar_matriz(matriz, "Circunferência - Depois do preenchimento")

    elif opcao == 3:
        # Polígono A
        gerar_poligono_a(matriz)
        mostrar_matriz(matriz, "Polígono A - Antes do preenchimento")
        pontos_a = [
            (15, 12),
            (30, 13),
            (32, 15),
            (20, 23),
            (10, 20),
            (18, 15)
        ]
        preencher_poligono_varredura(matriz, pontos_a, 2)
        mostrar_matriz(matriz, "Polígono A - Depois do preenchimento")

    elif opcao == 4:
        # Polígono C
        gerar_poligono_c(matriz)
        mostrar_matriz(matriz, "Polígono C - Antes do preenchimento")
        pontos_c = [
            (10, 30),
            (10, 24),
            (20, 17),
            (30, 24),
            (30, 30),
            (24, 30),
            (20, 28),
            (16, 30)
        ]
        preencher_poligono_varredura(matriz, pontos_c, 2)
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
        (15, 12),
        (30, 13),
        (32, 15),
        (20, 23),
        (10, 20),
        (18, 15)
    ]
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        gerar_reta_bresenham(x1, y1, x2, y2, matriz, cor)


def gerar_poligono_c(matriz, cor=1):
    vertices = [
        (10, 30),
        (10, 24),
        (20, 17),
        (30, 24),
        (30, 30),
        (24, 30),
        (20, 28),
        (16, 30)
    ]
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

    if dy > dx:
        dx, dy = dy, dx
        trocado = True
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        sx, sy = sy, sx

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


def preencher_retangulo(matriz, xmin, ymin, xmax, ymax, valor):
    for y in range(ymin + 1, ymax):
        for x in range(xmin + 1, xmax):
            liga_pixel(x, y, matriz, valor)


def preencher_circunferencia(matriz, xc, yc, R, valor):
    for y in range(yc - R, yc + R + 1):
        delta = R**2 - (y - yc)**2
        if delta >= 0:
            raiz = delta**0.5
            x1 = round(xc - raiz)
            x2 = round(xc + raiz)
            for x in range(x1 + 1, x2):
                liga_pixel(x, y, matriz, valor)


def preencher_poligono_varredura(matriz, pontos, cor_preenchimento=2):
    
    tabela_arestas = []
    
    for i in range(len(pontos)): #Aqui assim como no passo 1 ele constroi a tabela
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % len(pontos)]
        if y1 == y2: #Ele ser para ignorar quando fica numa aresta isolada
            continue
        if y1 < y2:
            y_min, y_max, x_y_min = y1, y2, x1
        else:
            y_min, y_max, x_y_min = y2, y1, x2
        dx_dy = (x2 - x1) / (y2 - y1)
        tabela_arestas.append([y_min, y_max, x_y_min, dx_dy]) #Depois de pegar os pontos setados ele armazena na tabela de arestas(vulgo lista)

    if not tabela_arestas:
        return

    #Verifica se tá no range do polígono para fazer varredura
    y_min_global = int(min(aresta[0] for aresta in tabela_arestas))
    y_max_global = int(max(aresta[1] for aresta in tabela_arestas))

    for y_varredura in range(y_min_global, y_max_global + 1): 
        interseccoes = []
        for aresta in tabela_arestas:
            y_min, y_max, x_y_min, inv_m = aresta
            if y_min <= y_varredura < y_max: 
                x_intersecao = inv_m * (y_varredura - y_min) + x_y_min #Aqui ele calcula as intersecções 
                interseccoes.append(x_intersecao) #Aqui ele pega as intersecções 
        interseccoes.sort()

        #faz o preenchimento a partir das intersecções
        for i in range(0, len(interseccoes), 2):
            if i + 1 < len(interseccoes):
                x_inicio = round(interseccoes[i])
                x_fim = round(interseccoes[i + 1])
                for x in range(x_inicio + 1, x_fim):
                    liga_pixel(x, y_varredura, matriz, cor_preenchimento)


if __name__ == "__main__":
    main()
