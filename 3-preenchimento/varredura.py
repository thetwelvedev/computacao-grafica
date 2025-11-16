import numpy as np
import matplotlib.pyplot as plt

def main():
    largura, altura = 50, 50
    matriz = np.zeros((altura, largura), dtype=int)

    print("Escolha a figura a desenhar:")
    print("1 - Retângulo")
    print("2 - Circunferência")
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
    for y in range(yc - R, yc + R + 1): #vai pecorrer toda circunferencia verticalmente
        delta = R**2 - (y - yc)**2
        if delta >= 0:
            raiz = delta**0.5
            x1 = round(xc - raiz)
            x2 = round(xc + raiz)
            for x in range(x1 + 1, x2):
                liga_pixel(x, y, matriz, valor)



if __name__ == "__main__":
    main()
