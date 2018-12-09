import networkx as nx
from random import randint
from random import uniform
from itertools import cycle

def select_with_probability(l, p):
	"""
	Selecciona un elemento de la lista l con probabilidad p.
	"""
	if not l:
		raise Exception("La lista es vacía.")
	else:
		circular_l = cycle(l)
		for element in circular_l:
			coin_toss = uniform(0, 1)
			if coin_toss <= p:
				return element 

def _construct_list_kp(n, k):
	per_partition = n // k
	#print("per partition", per_partition)
	return [per_partition] * k

def create_k_partite():
	n = 1
	k = 3
	while n % k != 0:
		n = randint(2, 20)
		k = randint(5, 10)
	print("Orden de la gráfica (|V|):", n)
	print("Número de particiones (k):", k)
	which_type = randint(1,2)
	if which_type == 1:
		return nx.complete_multipartite_graph(*_construct_list_kp(n, k)), k
	else:
		return nx.turan_graph(n, k), k

def color_map(color_int):
	if color_int == 1: return 'red'
	if color_int == 2: return 'blue'
	if color_int == 3: return 'yellow'
	if color_int == 4: return 'green'
	if color_int == 5: return 'purple'
	if color_int == 6: return 'grey'
	if color_int == 7: return 'orange'
	if color_int == 8: return 'pink'
	if color_int == 9: return 'magenta'
	if color_int == 10: return 'brown'

class ColorClass:

	def __init__(self, color):
		self.color = color
		self.vertices = []

	def __str__(self):
		return "Color: " + str(self.color) + "\nVértices en clase: " + str(self.vertices)

	def __repr__(self):
		return str(self)

def union_lists(l1, l2):
	return list(set(l1).union(set(l2)))

def difference_lists(l1, l2):
	return list(set(l1).difference(set(l2)))

def clear_colors(G):
	"""
	Establece los colores como nulos para todos 
	los vértices de la gráfica G.
	"""
	for v in G.nodes:
		G.node[v]['color'] = None

def color_vertex(G, v, c):
	"""
	Colorea el vértice v de color c.
	"""
	G.node[v]['color'] = c

def no_conflict_adjacent(G, c, v2):
	"""
	Verifica si el colorear en G un vértice
	adyacente al vértice v2 con color c no 
	causa conflicto.
	"""
	return G.node[v2]['color'] != c

def count_conlicts_vertex(G, v):
	conflicts = 0
	my_color = G.node[v]['color']
	for neighbor in list(G.adj[v]):
		if my_color == G.node[neighbor]['color']:
			conflicts += 1
	return conflicts

def count_global_conflicts(G):
	global_conflicts = 0
	for vertex in G.nodes:
		global_conflicts += count_conlicts_vertex(G, vertex)
	return global_conflicts // 2

def W(G, C_k):
	"""
	Devuelve la lista de vértices de G(V) que pueden 
	ser agregados a la clase de color actual C_k.
	Una clase de color tiene un color asociado
	y la lista de vértices en dicha clase.

	Esto se hace iterando los v  V y:
	1.- Checando v.color = None (no coloreado aún).
	2.- v NO sea vecino a uno de los vértices de la clase C_k
	pues en ese caso habría conflicto.  
	"""
	W = []
	for vertex in G.nodes:
		if G.node[vertex]['color'] == None:
			if vertex not in C_k.vertices:
				for potential_neighbor in C_k.vertices:
					if vertex not in list(G.adj[potential_neighbor]):
						W.append(vertex)
	return W

def B(G, C_k):
	"""
	Devuelve la lista de vértices de G(V) que NO pueden 
	ser agregados a la clase de color actual C_k.
	Una clase de color tiene un color asociado
	y la lista de vértices en dicha clase.
	
	Esto se hace iterando los v ∈ V y:
	1.- Checando v.color = None (no coloreado aún).
	2.- v SÍ sea vecino a uno de los vértices de la clase C_k
	pues en ese caso habría conflicto.  
	"""
	B = []
	for vertex in G.nodes:
		if G.node[vertex]['color'] == None:
			if vertex in C_k.vertices:
				B.append(vertex)
			else:
				for potential_neighbor in C_k.vertices:
					if vertex in list(G.adj[potential_neighbor]):
						B.append(vertex)
	return B

def degree_in_subgraph(G, X, i):
	"""
	Recibe una lista de vértices X y nos dice el 
	grado del vértice i en la subgráfica de G
	inducida por X.
	"""
	induced_subgraph = G.subgraph(X)
	return induced.degree(i)

def get_color_class(list_color_classes, color):
	for cc in list_color_classes:
		if cc.color == color:
			return cc
	return None

def n_ik(G, list_color_classes, i, k):
	random_choice = randint(1,3)
	C_k = get_color_class(list_color_classes, k)
	W = W(G, C_k)
	B =  B(G, C_k)
	if random_choice == 1:
		return degree_in_subgraph(G, B, i)
	elif random_choice == 2:
		return len(W) - degree_in_subgraph(G, W, i)
	else:
		return degree_in_subgraph(G, union_lists(B, W), i)

def Gamma(G, F, i):
	"""
	Devuelve la lista de los vecinos del vértice i
	en el conjunto de vértices F, en la gráfica G.
	"""
	neighbors = []
	for v in F:
		if v in G.adj[i]:
			neighbors.append(v)
	return neighbors

def generate_single_color_list(G, list_color_classes):
	n = len(G.nodes)
	mapping = [0] * 8
	for cc in list_color_classes:
		for v in cc.vertices:
			mapping[v] = cc.color
	return mapping


"""
C1 = ColorClass(1)
C2 = ColorClass(2)
C3 = ColorClass(3)
C1.vertices.append(2)
C1.vertices.append(4)
C1.vertices.append(5)
C2.vertices.append(0)
C2.vertices.append(6)
C3.vertices.append(1)
C3.vertices.append(3)
C3.vertices.append(7)
print(C1)
print(C2)
print(C3)
listaa = [C1, C2, C3]
print(generate_single_color_list(listaa))"""