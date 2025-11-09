from math import floor, ceil

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
    for linha in reversed(matriz): #inverte fazendo o pixel 0,0 ser o do canto inferior esquerdo
        print(" ".join(linha))  #deixa mais bonito (sem colchetes)

def liga_pixel(x, y, matriz):
    if 0 <= y < len(matriz) and 0 <= x < len(matriz[0]): #verifica se tá dentro da matriz
        matriz[y][x] = "⬛" 

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
        return floor(y + 0.5) #aqui é para números inteiros, quando for mas que 0.5 vai para próxima casa decimal e arredonda para baixo se for menor ou igual que 0.4 vai ficar no máximo 0.9 então vai para casa decimal anterior
    else:
        return ceil(y - 0.5)

menu()