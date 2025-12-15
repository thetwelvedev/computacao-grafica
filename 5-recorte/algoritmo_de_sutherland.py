import matplotlib.pyplot as plt

# Dimensões da Tela de Visualização
WIDTH, HEIGHT = 400, 400

# Limites da Janela de Recorte
X_MIN, Y_MIN = -100, -100
X_MAX, Y_MAX = 100, 100

# Vértices da Janela de Recorte (para referência, embora o algoritmo use as arestas)
JANELA_RECORTE = [
    (X_MIN, Y_MIN),
    (X_MAX, Y_MIN),
    (X_MAX, Y_MAX),
    (X_MIN, Y_MAX)
]

# Polígonos de Entrada
FIGURAS = [
    [(-80,50),(-80,150),(80,150),(80,50),(25,50),(25,110),(-25,110),(-25,50)], # Polígono A
    [(-50,-50),(-50,150),(150,-50)],                                         # Polígono B (Triângulo)
    [(-50,0),(50,0),(50,-40),(90,-40),(90,-120),(50,-120),
     (50,-160),(-50,-160),(-50,-120),(-90,-120),(-90,-40),(-50,-40)],        # Polígono C (Cruz)
    [(-30,-50),(20,40),(-70,120),(-160,60),(-130,-50)]                       # Polígono D (Pentágono)
]

# Atribuindo nomes para o menu
poligonoA = FIGURAS[0]
poligonoB = FIGURAS[1]
poligonoC = FIGURAS[2]
poligonoD = FIGURAS[3]

# --- Funções de Ajuda ---

def is_inside(p, edge_index):
    """Verifica se um ponto 'p' está 'dentro' da aresta da janela de recorte."""
    x, y = p
    
    if edge_index == 0: # Recorte contra a aresta ESQUERDA (x >= X_MIN)
        return x >= X_MIN
    elif edge_index == 1: # Recorte contra a aresta DIREITA (x <= X_MAX)
        return x <= X_MAX
    elif edge_index == 2: # Recorte contra a aresta INFERIOR (y >= Y_MIN)
        return y >= Y_MIN
    elif edge_index == 3: # Recorte contra a aresta SUPERIOR (y <= Y_MAX)
        return y <= Y_MAX
    return False

def compute_intersection(s, p, edge_index):
    """Calcula o ponto de interseção da linha (s, p) com a linha de recorte."""
    x_s, y_s = s
    x_p, y_p = p

    # Equação da Linha: y - y_s = m * (x - x_s)
    # Paramétrica: P(t) = s + t * (p - s)
    
    if edge_index == 0: # x = X_MIN (Aresta Esquerda)
        # Interseção de (s, p) com x = X_MIN
        # t = (X_MIN - x_s) / (x_p - x_s)
        t = (X_MIN - x_s) / (x_p - x_s)
        x_i = X_MIN
        y_i = y_s + t * (y_p - y_s)
        return (x_i, y_i)

    elif edge_index == 1: # x = X_MAX (Aresta Direita)
        # Interseção de (s, p) com x = X_MAX
        # t = (X_MAX - x_s) / (x_p - x_s)
        t = (X_MAX - x_s) / (x_p - x_s)
        x_i = X_MAX
        y_i = y_s + t * (y_p - y_s)
        return (x_i, y_i)

    elif edge_index == 2: # y = Y_MIN (Aresta Inferior)
        # Interseção de (s, p) com y = Y_MIN
        # t = (Y_MIN - y_s) / (y_p - y_s)
        t = (Y_MIN - y_s) / (y_p - y_s)
        x_i = x_s + t * (x_p - x_s)
        y_i = Y_MIN
        return (x_i, y_i)

    elif edge_index == 3: # y = Y_MAX (Aresta Superior)
        # Interseção de (s, p) com y = Y_MAX
        # t = (Y_MAX - y_s) / (y_p - y_s)
        t = (Y_MAX - y_s) / (y_p - y_s)
        x_i = x_s + t * (x_p - x_s)
        y_i = Y_MAX
        return (x_i, y_i)
        
    return s # Caso de erro, retorna o ponto inicial

# --- Algoritmo Principal ---

def sutherland_hodgman(polygon, edge_index):
    input_list = polygon
    output_list = []
    
    if not input_list:
        return []

    s = input_list[-1]
    
    for p in input_list: # 'p' de 'Point'
        # Regras de recorte para a aresta (s, p)
        
        s_inside = is_inside(s, edge_index)
        p_inside = is_inside(p, edge_index)
        
        if s_inside and p_inside:# CASO 1: s -> dentro, p -> dentro
            # Apenas 'p' é adicionado à lista de saídas.
            output_list.append(p)
            
        elif s_inside and not p_inside: # CASO 2: s -> dentro, p -> fora
            # O ponto 'i' de interseção entre (s, p) é tratado como vértice de saída.
            intersection = compute_intersection(s, p, edge_index)
            output_list.append(intersection)
            
        elif not s_inside and p_inside: # CASO 4 (do enunciado): s -> fora, p -> dentro
            # O ponto de interseção 'i' e 'p' são adicionados.
            intersection = compute_intersection(s, p, edge_index)
            output_list.append(intersection)
            output_list.append(p)
            
        # elif not s_inside and not p_inside:  # CASO 3: s -> fora, p -> fora
            # Nenhum ponto é adicionado (os dois vértices são descartados).
        # 'p' se torna o próximo ponto de partida 's' para a próxima iteração
        s = p
        
    return output_list


def clip_polygon(polygon):
    """
    Recorta o polígono contra todas as 4 arestas da janela.
    A ordem das arestas é: Esquerda, Direita, Inferior, Superior.
    """
    clipped_polygon = polygon
    
    # 0: Esquerda (x >= X_MIN), 1: Direita (x <= X_MAX), 
    # 2: Inferior (y >= Y_MIN), 3: Superior (y <= Y_MAX)
    for edge_index in range(4):
        clipped_polygon = sutherland_hodgman(clipped_polygon, edge_index)
        # Se o polígono se tornar vazio, não precisamos mais processar
        if not clipped_polygon:
            break
            
    return clipped_polygon

# --- Funções de Plotagem ---

def plot_polygon(ax, polygon, color='blue', linestyle='-', label='Polígono'):
    """Desenha um polígono fechado."""
    if not polygon:
        return
    # Cria uma lista de coordenadas x e y, e fecha o polígono (adiciona o primeiro ponto novamente)
    x = [p[0] for p in polygon] + [polygon[0][0]]
    y = [p[1] for p in polygon] + [polygon[0][1]]
    ax.plot(x, y, color=color, linestyle=linestyle, linewidth=2, marker='o', markersize=4, label=label)

def plot_window(ax):
    """Desenha a janela de recorte."""
    x_min, x_max, y_min, y_max = X_MIN, X_MAX, Y_MIN, Y_MAX
    # Vértices da janela (fechada)
    window_x = [x_min, x_max, x_max, x_min, x_min]
    window_y = [y_min, y_min, y_max, y_max, y_min]
    ax.plot(window_x, window_y, color='red', linestyle='--', linewidth=1, label='Janela de Recorte')

def mostrar(poligono_original):
    """
    Realiza o recorte e plota o resultado.
    """
    
    poligono_recortado = clip_polygon(poligono_original)

    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Desenha a Janela de Recorte
    plot_window(ax)

    # Desenha o Polígono Original
    plot_polygon(ax, poligono_original, color='blue', linestyle=':', label='Polígono Original (Entrada)')
    
    # Desenha o Polígono Recortado
    if poligono_recortado:
        plot_polygon(ax, poligono_recortado, color='green', linestyle='-', label='Polígono Recortado (Saída)')
    else:
        # Se a lista de saída for vazia, significa que o polígono está totalmente fora
        ax.text(0, 0, "Polígono totalmente fora da janela!", color='red', ha='center')

    # Configurações do Gráfico
    ax.set_title("Algoritmo de Recorte de Polígonos Sutherland-Hodgman")
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    
    # Ajusta os limites para mostrar o polígono original e a janela
    all_x = [p[0] for p in poligono_original] + [X_MIN, X_MAX]
    all_y = [p[1] for p in poligono_original] + [Y_MIN, Y_MAX]
    
    x_range = max(all_x) - min(all_x)
    y_range = max(all_y) - min(all_y)
    
    padding = max(x_range, y_range) * 0.15 # Adiciona um pouco de margem
    
    ax.set_xlim(min(all_x) - padding, max(all_x) + padding)
    ax.set_ylim(min(all_y) - padding, max(all_y) + padding)

    ax.set_aspect('equal', adjustable='box') # Garante que as coordenadas sejam proporcionais
    ax.legend()
    ax.grid(True)
    plt.show()

# --- Menu Principal ---

def menu():
    """Menu de seleção de polígono."""
    print("--- Recorte de Polígonos Sutherland-Hodgman ---")
    print("Escolha o polígono para recortar (e pressione Enter):")
    print("1 - Polígono A ")
    print("2 - Polígono B (Triângulo)")
    print("3 - Polígono C (Cruz)")
    print("4 - Polígono D (Pentágono)")
    
    # Dicionário de polígonos para simplificar a lógica
    opcoes = {
        1: poligonoA,
        2: poligonoB,
        3: poligonoC,
        4: poligonoD
    }
    
    while True:
        try:
            opcao = input("Opção: ")
            if not opcao.isdigit():
                 print("Entrada inválida. Por favor, digite um número (1 a 4).")
                 continue
            
            opcao = int(opcao)

            if opcao in opcoes:
                mostrar(opcoes[opcao])
                break # Sai do loop após mostrar
            else:
                print("Opção inválida! Por favor, escolha 1, 2, 3 ou 4.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número (1 a 4).")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

if __name__ == "__main__":
    menu()