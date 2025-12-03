import matplotlib.pyplot as plt
import matplotlib.patches as PolygonPatch

def recortar(subjectPolygon, clipPolygon):

    def inside(p, edge):
        (x1, y1), (x2, y2) = edge
        return (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0

    def intersec(s, e, edge):
        (x1, y1), (x2, y2) = edge

        A1 = e[1] - s[1]
        B1 = s[0] - e[0]
        C1 = A1 * s[0] + B1 * s[1]

        A2 = y2 - y1
        B2 = x1 - x2
        C2 = A2 * x1 + B2 * y1

        det = A1 * B2 - A2 * B1
        if det == 0:
            return e  # Paralela

        x = (B2 * C1 - B1 * C2) / det
        y = (A1 * C2 - A2 * C1) / det
        return [x, y]

    outputList = subjectPolygon[:]

    for i in range(len(clipPolygon)):
        cp1 = clipPolygon[i]
        cp2 = clipPolygon[(i + 1) % len(clipPolygon)]
        edge = (cp1, cp2)

        inputList = outputList
        outputList = []

        if not inputList:
            break

        s = inputList[-1]

        for e in inputList:
            s_in = inside(s, edge)
            e_in = inside(e, edge)

            if (not s_in) and e_in:
                outputList.append(intersec(s, e, edge))
                outputList.append(e)

            elif s_in and e_in:
                outputList.append(e)

            elif s_in and (not e_in):
                outputList.append(intersec(s, e, edge))

            s = e

    return outputList

escala = 2

janela = [(2,2),(2,12),(12,12),(12,2)]
janela = [(x*escala, y*escala) for x,y in janela]

poligonoA = [
    (3, 9.8), (3, 15), (11, 15), (11, 10),
    (6, 9.8), (8, 10), (6, 12.2), (8, 12.2)
]
poligonoA = [(x*escala, y*escala) for x,y in poligonoA]

poligonoB = [(6,14), (6,6), (14,6)]
poligonoB = [(x*escala, y*escala) for x,y in poligonoB]

poligonoC = [
    (5,2), (7,2), (7,5), (10,5), (10,7),
    (7,7), (7,10), (5,10), (5,7), (2,7),
    (2,5), (5,5)
]
poligonoC = [(x*escala, y*escala) for x,y in poligonoC]

poligonoD = [
    (2,12), (4,15), (7,15), (9,12), (5,10)
]
poligonoD = [(x*escala, y*escala) for x,y in poligonoD]

def desenhar_poligono(ax, vertices, cor="yellow", alpha=0.7):
    if len(vertices) < 3:
        return
    patch = plt.Polygon(vertices, closed=True, facecolor=cor, alpha=alpha, edgecolor="black", linewidth=2)
    ax.add_patch(patch)

def mostrar(poligono_original):

    fig, axs = plt.subplots(1, 2, figsize=(12,6))

    # ----------- ANTES -----------
    axs[0].set_title("Antes do recorte")
    desenhar_poligono(axs[0], poligono_original, "yellow")

    desenhar_poligono(axs[0], janela, "none", alpha=1.0)
    axs[0].plot([p[0] for p in janela] + [janela[0][0]],
                [p[1] for p in janela] + [janela[0][1]], color="green")

    axs[0].set_xlim(0, 40)
    axs[0].set_ylim(0, 40)
    axs[0].grid(True)

    poligono_recortado = recortar(poligono_original, janela)

    axs[1].set_title("Depois do recorte")

    if poligono_recortado:
        desenhar_poligono(axs[1], poligono_recortado, "red")

    desenhar_poligono(axs[1], janela, "none", alpha=1.0)
    axs[1].plot([p[0] for p in janela] + [janela[0][0]],
                [p[1] for p in janela] + [janela[0][1]], color="green")

    axs[1].set_xlim(0, 40)
    axs[1].set_ylim(0, 40)
    axs[1].grid(True)

    plt.show()


print("Escolha o polígono para recortar:")
print("1 - Polígono A")
print("2 - Polígono B")
print("3 - Polígono C (cruz)")
print("4 - Polígono D (pentágono)")
opcao = int(input("Opção: "))

if opcao == 1:
    mostrar(poligonoA)
elif opcao == 2:
    mostrar(poligonoB)
elif opcao == 3:
    mostrar(poligonoC)
elif opcao == 4:
    mostrar(poligonoD)
else:
    print("Opção inválida!")
