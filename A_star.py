import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re

class Node():
    def __init__(self, label, g = None, h = None) -> None:
        self._label = label
        self._g = g
        self._h = h
    
    def __eq__(self, other):
        return self._label == other.label()
    
    def label(self):
        return self._label
    
    def h(self):
        return self._h
    
    def g(self):
        return self._g

    def f(self):
        return self._g+self._h
    
    def get_line(self):
        return self._label[-1]
    
    def __hash__(self):
        return hash(self._label)

class Tree:
    def __init__(self):
        self.G = nx.DiGraph()
        self.pos = None
        self.gs = {}  
        self.hs = {}  
    
    def add_node(self, parent, child, g=None, h = None): 
        if parent is None:
            self.G.add_node(child.label())
        else:
            if parent.label() not in self.G.nodes:
                raise ValueError("Parent node does not exist.")
            self.G.add_edge(parent.label(), child.label())
        self.gs[child.label()] = g 
        self.hs[child.label()] = h  
        self.update_positions()
    
    def add_neighbors(self, parent, neighbors):
        for node in neighbors:
            self.add_node(parent, node, node.g(), node.h())

    def update_positions(self):
        self.pos = nx.nx_agraph.graphviz_layout(self.G, prog="dot")

    def plot_tree(self):
        plt.figure(figsize=(10, 6))  # Define o tamanho da figura

        # Desenha os nós do grafo
        nx.draw(
            self.G,
            pos=self.pos,
            with_labels=True,
            arrows=True,
            node_color="lightblue",
            node_size=800,
            font_weight="bold",
            font_size=10,
        )

        # Adiciona os custos dos nós ao lado dos nós
        for (node_g, g), (node_h, h) in zip(self.gs.items(), self.hs.items()):
            assert node_g == node_h  # Verificar se os nós são os mesmos em ambos os dicionários
            x, y = self.pos[node_g]
            plt.text(x + 6.5, y, f'g: {g}; h: {h}', fontsize=8, ha='left', fontweight='bold')

        # Desenha os nós do melhor caminho em vermelho
        for node in self.path:
            if node in self.G.nodes:
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=[node], node_color='red', node_size=800)

        plt.show()

class A_star(Tree):
    def __init__(self, start, goal, g_mat, h_mat) -> None:
        super().__init__()

        self.lines = {}
        self.lines['b'] = ["E6","E7", "E3", "E8", "E10", "E12"]
        self.lines['g'] = ["E7", "E2", "E9", "E10", "E13"]
        self.lines['r'] = ["E1",  "E2", "E3", "E4", "E14"]
        self.lines['y'] = ["E11", "E9", "E8", "E4", "E5"]

        self.current_line = start[-1]
        
        self.g_mat = g_mat
        self.h_mat = h_mat

        
        self.goal_node = Node(goal)
        self.starting_node = Node(start, 0, self.get_h(Node(start)))
        


        self.current_g = 0
        self.current_h = self.get_h(self.starting_node)
        self.path = []
        self.previous_path = []


        self.current_node = Node(self.starting_node.label(), 0, self.current_h)
        
        self.add_node(None, self.current_node)
    
    def position_exists(self, label):
        return label[0:-1] in set(self.lines[label[-1]])
    
    def get_state_idx(self, node):
        return int(re.findall(r'\d+', node.label())[0]) - 1

    def is_different_line(self, label):
        return not label in set(self.lines[self.current_line])

    def change_line(self, elements2check):
        if(set(elements2check).issubset(set(self.lines['b']))):
            return 'b'
        elif(set(elements2check).issubset(set(self.lines['g']))):
            return 'g'
        elif(set(elements2check).issubset(set(self.lines['r']))):
            return 'r'
        elif(set(elements2check).issubset(set(self.lines['y']))):
            return 'y'
        
    def _find_neighbors(self):
        neighbors = []
        
        current_idx = self.get_state_idx(self.current_node)

        elms = (self.g_mat[current_idx, :] > 0) & (self.g_mat[current_idx, :] < np.inf)

        potential_neighbors = np.where(elms)[0]
        
        for idx in potential_neighbors:
            label = "E"+str(idx + 1)

            if(self.is_different_line(label)):
                new_line = self.change_line([label, self.current_node.label()[0:-1]])
                new_neighbor  = Node("E"+str(current_idx+1)+new_line, \
                                 self.current_g + 3,\
                                 self.get_h(Node("E"+str(current_idx+1)+new_line)))
                if(new_neighbor not in set(neighbors)):
                    neighbors.append(new_neighbor)
            else:
                neighbors.append(Node(label+self.current_line,\
                                 self.current_g + self.g_mat[self.get_state_idx(Node("E"+str(current_idx+1))), self.get_state_idx(Node(label+self.current_line))],\
                                 self.get_h(Node(label+self.current_line))))

        return neighbors
    
    def _find_parent_child(self, parent, parent_line):
        neighbors = []
        
        current_idx = self.get_state_idx(parent)

        elms = (self.g_mat[current_idx, :] > 0) & (self.g_mat[current_idx, :] < np.inf)

        potential_neighbors = np.where(elms)[0]
        
        for idx in potential_neighbors:
            label = "E"+str(idx + 1)

            if(self.is_different_line(label)):
                new_line = self.change_line([label, parent.label()[0:-1]])
                new_neighbor  = Node("E"+str(current_idx+1)+new_line, \
                                 self.current_g + 3,\
                                 self.get_h(Node("E"+str(current_idx+1)+new_line)))
                if(new_neighbor not in set(neighbors)):
                    neighbors.append(new_neighbor)
            else:
                neighbors.append(Node(label+parent_line,\
                                 self.current_g + self.g_mat[self.get_state_idx(Node("E"+str(current_idx+1))), self.get_state_idx(Node(label+parent_line))],\
                                 self.get_h(Node(label+parent_line))))

        return neighbors


    def is_final_node(self, node):
        return self.goal_node == node
    

    def get_h(self, node):
        return self.h_mat[self.get_state_idx(node), self.get_state_idx(self.goal_node)]



    def get_f(self, node):
        return

    def _get_best_node(self, list):
        min = np.inf
        min_node = None
        for node in list:
            if(min > node.f()):
                min = node.f()
                min_node = node

        return min_node, min_node.get_line()

    def path_changes(self):
        return self.previous_path != self.path

    def run(self):
        # Se a posição ínicial é inválida, não rodar o código
        if(not self.position_exists(self.starting_node.label())):
            raise ValueError("Position doesn't exist!")

        # Cria lista aberta e fechada
        open_list = [self.starting_node]
        closed_list = []

        # adiciona nó atual para a árvore para plotar posteriormente
        self.add_node(None, self.current_node, g = 0, h = self.get_h(self.current_node))
        
        while(open_list):
            # this line below is just for the logic to plot the best path            
            (self.current_node, self.current_line) = self._get_best_node(open_list)
            self.current_g = self.current_node.g()


            # adiciona nó atual ao caminho
            self.path.append(self.current_node.label())

            # se o nó atual for igual ao nó destino, parar algoritmo
            if self.current_node == self.goal_node:
                cleaned_path = [self.goal_node.label()]  # Incluindo o goal node no caminho limpo
                for i in range(len(self.path) - 2, -1, -1):
                    node_label = self.path[i]
                    # Verifica se o nó tem um filho nos nós restantes do caminho
                    if any(edge[0] == node_label for edge in self.G.out_edges(node_label) if edge[1] in self.path[i:]):
                        cleaned_path.insert(0, node_label)
                self.path = cleaned_path
                # Remove nós desnecessários iterativamente até que não haja mais mudanças no caminho
                while True:
                    path_changed = False
                    parent = "none"
                    for i in range(1, len(self.path) - 1):
                        node_label = self.path[i]
                        # Se o nó não tiver filhos no caminho restante e não for o goal node, remova-o
                        if not any(edge[0] == node_label and edge[1] in self.path and edge[1] != parent for edge in self.G.out_edges(node_label)) \
                                and node_label != self.goal_node.label():
                            self.path.remove(node_label)
                            path_changed = True
                            break  # Saia do loop e recalcule o caminho
                        parent = node_label
                    if not path_changed:
                        break  # Se não houver mais mudanças, pare o loop
                return self.path


            # procura por nós vizinhos
            neighbors = self._find_neighbors()

            # elimina nó pai entre nós vizinhos
            neighbors = [x for x in neighbors if x.label() not in set(self.path)]
            
            # adiciona nós vizinhos à arvore para plotar posteriormente
            self.add_neighbors(self.current_node, neighbors)

            # adiciona nós vizinhos à lista aberta
            for node in neighbors:
                if(node not in set(open_list) and node not in set(closed_list)):
                    open_list.append(node)

            # remove nó atual da lista aberta e o adiciona à lista fechada
            closed_list.append(self.current_node)
            open_list.remove(self.current_node)


        # se a solução final, não for encontrada e todo espaço for buscado, terminar algoritmo sem solução.
        return "No solution"