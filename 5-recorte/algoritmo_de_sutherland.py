import matplotlib.pyplot as plt
import matplotlib.patches as PolygonPatch

def menu():
    print("Escolha o polígono para recortar (e pressione Enter):")
    print("1 - Polígono A ")
    print("2 - Polígono B (Triângulo)")
    print("3 - Polígono C (Cruz)")
    print("4 - Polígono D (Pentágono)")
    try:
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
    except ValueError:
        print("Entrada inválida. Por favor, digite um número (1 a 4).")

escala = 2 

# Janela (Window) - Vértices no sentido anti-horário (importante para 'inside')
# (min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)
janela = [(2,2),(2,12),(12,12),(12,2)] 
janela = [(x*escala, y*escala) for x,y in janela] # Multiplica por 2 para melhor visualização

# Polígono A (Côncavo)
poligonoA = [
    (3, 9.8), (3, 15), (11, 15), (11, 10),
    (8, 12.2), (6, 12.2), (8, 10), (6, 9.8)
]
poligonoA = [(x*escala, y*escala) for x,y in poligonoA]

# Polígono B (Triângulo)
poligonoB = [(6,14), (6,6), (14,6)]
poligonoB = [(x*escala, y*escala) for x,y in poligonoB]

# Polígono C (Cruz, Recorte complexo)
poligonoC = [
    (5,2), (7,2), (7,5), (10,5), (10,7),
    (7,7), (7,10), (5,10), (5,7), (2,7),
    (2,5), (5,5)
]
poligonoC = [(x*escala, y*escala) for x,y in poligonoC]

# Polígono D (Pentágono)
poligonoD = [
    (2,12), (4,15), (7,15), (9,12), (5,10)
]
poligonoD = [(x*escala, y*escala) for x,y in poligonoD]

def desenhar_poligono(ax, vertices, cor="yellow", alpha=0.7, edge_color="black"):
    if len(vertices) < 3:
        return
    patch = plt.Polygon(vertices, closed=True, facecolor=cor, alpha=alpha, edgecolor=edge_color, linewidth=2)
    ax.add_patch(patch)

def mostrar(poligono_original):

    fig, axs = plt.subplots(1, 2, figsize=(12,6))

    # ----------- ANTES -----------
    axs[0].set_title("Antes do recorte (Polígono Original em Amarelo)")
    desenhar_poligono(axs[0], poligono_original, "yellow")

    # Desenha a Janela (Window)
    janela_coords = [p for p in janela]
    desenhar_poligono(axs[0], janela_coords, "none", alpha=1.0, edge_color="green")
    
    axs[0].set_xlim(0, 40)
    axs[0].set_ylim(0, 40)
    axs[0].set_aspect('equal', adjustable='box')
    axs[0].grid(True)

    poligono_recortado = recortar(poligono_original, janela)

    # ----------- DEPOIS -----------
    axs[1].set_title("Depois do recorte (Polígono Recortado em Vermelho)")

    if poligono_recortado:
        # Verifica se o polígono resultante tem pelo menos 3 vértices para ser desenhado
        desenhar_poligono(axs[1], poligono_recortado, "red")

    # Desenha a Janela (Window)
    janela_coords = [p for p in janela]
    desenhar_poligono(axs[1], janela_coords, "none", alpha=1.0, edge_color="green")

    axs[1].set_xlim(0, 40)
    axs[1].set_ylim(0, 40)
    axs[1].set_aspect('equal', adjustable='box')
    axs[1].grid(True)

    plt.show()

def recortar(subjectPolygon, clipPolygon):
    """
    Recorta o poligono sujeito contra o poligono de recorte (janela)
    usando o algoritmo de Sutherland-Hodgman.
    """

    def inside(p, edge):
        """ Verifica se o ponto 'p' esta 'dentro' (a esquerda ou na linha) 
            da aresta de recorte (x1,y1) -> (x2,y2). """
        (x1, y1), (x2, y2) = edge
        # O vetor (x2-x1, y2-y1) é o vetor da aresta.
        # O vetor normal (y1-y2, x2-x1) aponta para 'dentro' da janela.
        # Calcula o produto escalar do vetor (p-p1) com o vetor normal.
        # (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0 
        # (p[0] - x1) * (y1 - y2) + (p[1] - y1) * (x2 - x1) >= 0
        return (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0

    def intersec(s, e, edge):
        """ Calcula o ponto de interseção entre o segmento s->e e a linha de recorte edge. """
        (x1, y1), (x2, y2) = edge  # Aresta de recorte

        dx_edge, dy_edge = x2 - x1, y2 - y1
        dx_seg, dy_seg = e[0] - s[0], e[1] - s[1]

        # Denominador para t e u (u é o segmento, t é a aresta de recorte)
        # Den = -dx_seg * dy_edge + dx_edge * dy_seg (de forma mais limpa)
        det = dx_seg * dy_edge - dx_edge * dy_seg
        
        # Se o determinante é zero, as linhas são paralelas
        if det == 0:
            # Não é esperado que as arestas sejam paralelas no recorte SH, mas
            # se for, retornamos 'e' para seguir a lógica do SH.
            return e 

        t = (s[0] - x1) * dy_edge - (s[1] - y1) * dx_edge
        u = (s[0] - x1) * dy_seg - (s[1] - y1) * dx_seg

        t_param = u / det  # Usamos t_param para a equação paramétrica do segmento s->e: P = s + t_param * (e-s)
        
        # Calcula as coordenadas do ponto de interseção
        ix = s[0] + t_param * dx_seg
        iy = s[1] + t_param * dy_seg
        
        return [ix, iy]

    outputList = subjectPolygon[:]

    # Percorre as 4 arestas da janela (clipPolygon)
    for i in range(len(clipPolygon)):
        cp1 = clipPolygon[i]
        cp2 = clipPolygon[(i + 1) % len(clipPolygon)]
        edge = (cp1, cp2)  # Aresta de recorte (cp1 -> cp2)

        inputList = outputList
        outputList = []

        if not inputList:
            break

        # S é o ponto anterior, E é o ponto atual na iteração
        s = inputList[-1]

        for e in inputList:
            s_in = inside(s, edge)
            e_in = inside(e, edge)

            # Caso 4: Fora -> Dentro
            if (not s_in) and e_in:
                # 1. Adiciona a interseção (I)
                outputList.append(intersec(s, e, edge))
                # 2. Adiciona o ponto final (E)
                outputList.append(e)

            # Caso 1: Dentro -> Dentro
            elif s_in and e_in:
                # 1. Adiciona o ponto final (E)
                outputList.append(e)

            # Caso 2: Dentro -> Fora
            elif s_in and (not e_in):
                # 1. Adiciona a interseção (I)
                outputList.append(intersec(s, e, edge))

            # Caso 3: Fora -> Fora (Nenhum ponto adicionado)

            s = e # Atualiza S para o próximo segmento

    return outputList

menu()