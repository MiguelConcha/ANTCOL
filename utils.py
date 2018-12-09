# -*- coding = utf-8 -*-
#!/usr/bin/env python

"""utils.py: Funciones auxiliares y complementarias para la implementación
   del ACO ANTCOL de Dowsland y Thompson."""
__author__ = "Concha Vázquez Miguel"
__copyright__ = "Copyright (C) 2018 Miguel Concha"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Miguel Concha"
__email__ = "mconcha@ciencias.unam.mx"
__status__ = "Completo"

import networkx as nx 			# Generación y manejo de gráficas con python.
from random import randint		# Obtención de números aleatorios.
from random import uniform
from itertools import cycle     # Tratamiento de listas circulares.

def select_with_probability(l, p):
	"""
	Selecciona un elemento de la lista l con probabilidad p.

	:param l: La lista de la cual se extraerá el elemento.
	:param p: La probabilidad de extracción del elemento actual.
	:return: El elemento elegido de la lista.
	:rtype: any.
	"""
	# Comprobando que en efecto se pueda llevar a cabo la acción.
	if not l:
		raise Exception("La lista es vacía.")
	else:
		# Generamos un iterable circular de la lista.
		circular_l = cycle(l)
		# Para cada elemento lanzamos un volado para determinar si lo elegimos.
		for element in circular_l:
			coin_toss = uniform(0, 1)
			if coin_toss <= p:
				return element 

def _construct_list_kp(n, k):
	"""
	Función auxiliar para la creación de gráficas k-partitas.
	Crea una lista de longitud k, y en cada entrada coloca tantos
	vértices como resulten de la división entera de n entre k.

	:param n: El total de vértices a repartir en cada partición.
	:param k: El número de particiones.
	:return: La lista de longitud k en donde cada entrada es n/k.
	:rtype: list.
	"""
	per_partition = n // k
	return [per_partition] * k

def create_k_partite(maxi):
	"""
	Función para la creación de una gráfica k-partita.

	:param maxi: La cota superior al número de vértices que tendrá
	la gráfica aleatoria generada.
	:return: Una gráfica k-partita de la biblioteca networkx.
	:rtype: nx.Graph
	"""
	n = 1
	k = 3
	# Quiero repartir uniformemente la misma cantidad de vértices en cada partición.
	while n % k != 0:
		# Generando la n y la k (números para vértices y particiones, resp.) de forma
		# aleatoria en un intervalo permitido.
		n = randint(2, maxi)
		k = randint(5, 10)
	print("Orden de la gráfica (|V|):", n)
	print("Número de particiones (k):", k)
	# Dependiendo de un segundo volado, se genera una gráfica k-partida de uno u otro tipo.
	which_type = randint(1,2)
	if which_type == 1:
		return nx.complete_multipartite_graph(*_construct_list_kp(n, k)), k
	else:
		return nx.turan_graph(n, k), k

def color_map(color_int):
	"""
	Función que mapea enteros a cadenas que representan colores. Será útil
	al momento de querer dibujar una gráfica cuyos vértices se coloreen
	con matplotplib. Sabemos que 5 <= k <= 10, así que en el peor caso
	se usan diez colores que hay que definir.

	:param color_int: El código de color a ser transformado.
	:return: La cadena que corresponde a dicho entero.
	:rtype: string.
	"""
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
	"""
	Clase para representar una clase de color.

	Atributos:
	----------

	color: int
		   El color asociado a la clase de color.

	vertices: [int]
			  La lista de los vértices (representados por su etiqueta entera)
			  dentro de la clase de color.
	"""
	
	def __init__(self, color):
		"""
		Contructor de una clase de color. Al principio no hay vértices en su lista.

		:param color: El color asociado con la clase de color.
		"""
		self.color = color
		self.vertices = []

	def __str__(self):
		"""
		Método para devolver la representación en cadena de una clase de color.

		:return: La cadena que simboliza la clase de color.
		:rtype: string.
		"""
		return "\n\nColor: " + str(self.color) + "\nVértices en clase: " + str(self.vertices)

	def __repr__(self):
		"""
		Método para devolver la representación en cadena de una clase de color.

		:return: La cadena que simboliza la clase de color.
		:rtype: string.
		"""
		return str(self)

def union_lists(l1, l2):
	"""
	Función para llevar a cabo la unión de dos listas.
	Para ello primero se convierten a conjuntos y luego se lleva a 
	cabo la operación; finalmente, se transforma el conjutno obtenido
	de la operación a lista nuevamente.

	:params l1 l2: Las dos listas a ser unidas.
	:return: La lista resultante de la unión de las listas.
	:rtype: list
	"""
	return list(set(l1).union(set(l2)))

def difference_lists(l1, l2):
	"""
	Función para llevar a cabo la diferencia de dos listas.
	Para ello primero se convierten a conjuntos y luego se lleva a 
	cabo la operación; finalmente, se transforma el conjutno obtenido
	de la operación a lista nuevamente.

	:params l1 l2: l1 es la lista de la cual se obtendrá la diferencia con l2.
	:return: La lista resultante de la diferencia de las listas.
	:rtype: list
	"""
	return list(set(l1).difference(set(l2)))

def clear_colors(G):
	"""
	Establece los colores como nulos para todos 
	los vértices de la gráfica G.
	
	:param G: networkx.Graph
	"""
	for v in G.nodes:
		G.node[v]['color'] = None

def color_vertex(G, v, c):
	"""
	Colorea el vértice v de la gráfica G con el color c.

	:param G: network.Graph
	:param v: La etiqueta entera del vértice a ser coloreado.
	:param c: La etiqueta entera del color se le será asociado.
	"""
	G.node[v]['color'] = c

def no_conflict_adjacent(G, c, v2):
	"""
	Verifica si el colorear en G un vértice
	adyacente al vértice v2 con color c no 
	causa conflicto.

	:param G: networkx.Graph
	:param c: El color del que sería potencialmente pintado un vértice
              adyacente a v2.
    :param v2: El vértice vecino del que se comprueba.
    :return: Verdadero si tendrían colores distintos; falso en el caso contrario.
    :rtype: boolean.
	"""
	return G.node[v2]['color'] != c

def count_conlicts_vertex(G, v):
	"""
	Función que cuenta el númeor de conflictos ocasionados
	por un vértice coloreado v.

	:param G: networkx.Graph
	:param v: El vértice cuyos conflictos de color serán considerados.
	:return: El número de conflictos ocasionados por el vértice v.
	:rtype: int.
	"""
	conflicts = 0
	my_color = G.node[v]['color']
	# Por cada uno de sus vecinos, si coincide con su color, incrementamos
	# el contador de conflictos.
	for neighbor in list(G.adj[v]):
		if my_color == G.node[neighbor]['color']:
			conflicts += 1
	return conflicts

def count_global_conflicts(G):
	"""
	Función que determina el número total de conflictos en toda
	la gráfica.

	:param G: networkx.Graph
	:return: La cantidad de conflictos de color por la coloración de la gráfica.
			 Si el resultado es cero, quiere decir que la coloración de G 
			 es propia.
	:rtype: int.
	"""
	global_conflicts = 0
	# Iteramos sobre los vértices de G e invocamos a la función que cuenta los conflictos
	# ocasionados por cada vértice individual.
	for vertex in G.nodes:
		global_conflicts += count_conlicts_vertex(G, vertex)
	# El resultado lo dividimos entre dos pues las aristas son no dirigidas.
	return global_conflicts // 2

def W(G, C_k):
	"""
	Devuelve la lista de vértices de G(V) que pueden 
	ser agregados a la clase de color actual C_k.

	Esto se hace iterando los v ∈ V y:
	1.- Checando v.color = None (no coloreado aún).
	2.- Que v NO sea vecino a uno de los vértices de la clase C_k
	pues en ese caso habría conflicto.  

	:param G: networkx.Graph
	:param C_k: La clase de color de referencia.
	:return: La lista de vértices de G(V) que pueden 
			 ser agregados a la clase de color actual C_k.
	:rtype: [int]
	"""
	W = []
	for vertex in G.nodes:
		if G.node[vertex]['color'] == None:
			if vertex not in C_k.vertices:
				# Comprobando que el vértice no sea adyacente a uno 
				# de la clase de color.
				for potential_neighbor in C_k.vertices:
					if vertex not in list(G.adj[potential_neighbor]):
						W.append(vertex)
	return W

def B(G, C_k):
	"""
	Devuelve la lista de vértices de G(V) que NO pueden 
	ser agregados a la clase de color actual C_k.
	
	Esto se hace iterando los v ∈ V y:
	1.- Checando v.color = None (no coloreado aún).
	2.- v SÍ sea vecino a uno de los vértices de la clase C_k
	pues en ese caso habría conflicto. 

	:param G: networkx.Graph
	:param C_k: La clase de color de referencia.
	:return: La lista de vértices de G(V) que NO pueden 
			 ser agregados a la clase de color actual C_k.
	:rtype: [int]
	"""
	B = []
	for vertex in G.nodes:
		if G.node[vertex]['color'] == None:
			# Si no tiene color, no lo podríamos meter a la clase
			# de color y lo consideramos.
			if vertex in C_k.vertices:
				B.append(vertex)
			else:
				# El otro caso es que sea vecino a uno de los vértices
				# en la lista asociada a la clase de color de referencia.
				for potential_neighbor in C_k.vertices:
					if vertex in list(G.adj[potential_neighbor]):
						B.append(vertex)
	return B

def degree_in_subgraph(G, X, i):
	"""
	Recibe una lista de vértices X y nos dice el 
	grado del vértice i en la subgráfica de G
	inducida por X.

	:param G: networkx.Graph.
	:param X: El conjunto de vértice que induce a al subgráfica.
	:param i: lLa etiqueta entera del vértice de interés.
	:return: El grado del vértice en la subgráfica inducida por X.
	:rtype: int.
	"""
	induced_subgraph = G.subgraph(X)
	return induced_subgraph.degree(i)

def get_color_class(list_color_classes, color):
	"""
	Función que a partir de una lista de clases de colores y una
	etiqueta entera de color obtiene la clase de color asociada
	a dicho número.

	:param list_color_classes: La lista de todas las clases de color.
	:param color: La etiqueta entera del color para el cual se buscará
	              su clase de color.
	:return: La clase de color correspondiente al entero pasado como parámetro.
	:rtype: ColorClass
	"""
	for cc in list_color_classes:
		if cc.color == color:
			return cc
	return None

def generate_single_color_list(G, list_color_classes):
	"""
	Función que a partir de la lista de clases de color, genera una sola lista
	en donde para la i-ésima entrada se coloca la clave de color asociada al vértice
	i en la gráfica G.

	:param G: networks.Graph
	:param list_color_classes: La lista de las clases de color.
	:return: Una lista con las claves de color por cada vértice de G.
	:rtype: [int]
	"""
	# Creando inicialmente una lista de ceros de la longitud de |V|.
	n = len(G.nodes)
	mapping = [0] * n
	# Iterando sobre las clases de color de la lista.
	for cc in list_color_classes:
		# Iterando sobre los vértices de la clase de color.
		for v in cc.vertices:
			# En la posición del vértice en la lista que devolveremos colocamos 
			# la etiqueta entera de su color asociado.
			mapping[v] = cc.color
	return mapping

def get_colors_strings(list_int_colors):
	"""
	Función que a partir de una lista de etiquetas enteras de color, devuelve
	una lista con las cadenas asociadas a cada número.

	:param list_int_colors: La lista con las codificaciones enteras de color.
	:return: Una lista de cadenas asociando cada entero de la lista original
		     con el color que le corresponde bajo la codificación.
	:rtype: [string]
	"""
	res = []
	for i in list_int_colors:
		# Mandamos llamar a la función que mapea un solo entero a la cadena.
		# Hay que incrementar en una unidad pues el mapeo comienza desde el 1
		res.append(color_map(i + 1))
	return res

def test(G, mini):
	"""
	Función con propósitos de prueba para ver si al crear una asignación de vértices
	en clase de colores podemos crear la representación adecuada de la gráfica.

	:param G: networkx.Graph
	:param mini: El mínimo número de colores necesarios para colorear.
	:return: Una lista de clases de colores para colorear la Gráfica G y el total
	         de colores usados.
	:rtype: [ColorClass], int
	"""
	total_used = 0
	list_color_classes = []
	# Tenemos que cerciorarnos de usar mínimamente un número de colores.
	while total_used < mini:
		k = randint(mini, 10)
		# Inciializando una lista de clases de colores.
		list_color_classes = [None] * k
		for number in range(k):
			# Creando una nueva clase de color.
			new_color_class = ColorClass(number)
			# Agregadno al clase de color a la lista de clases de color.
			list_color_classes[number] = new_color_class
		for node in G.nodes:
			# Para cada nodo decidimos qué color le asignamos.
			which_color_class = randint(0, len(list_color_classes) - 1)
			# Lo agregamos a la de vértices de la clase de color que le tocó.
			list_color_classes[which_color_class].vertices.append(node)
			# Coloreando el vértice.
			G.node[node]['color'] = which_color_class
		# Calculando el número de colores que usamos.
		total_used = non_empty(list_color_classes)
	return list_color_classes, total_used

def non_empty(list_of_lists):
	"""
	Función que determina el número de listas no vacías dada una lista de listas.

	:param list_of_lists: Una lista de listas (es una lista de clases de colores).
	:return: El número de listas no vacías en la lista pasada como parámetro.
	:rtype: int.
	"""
	count = 0
	for cc in list_of_lists:
		# Checamos si la longitud de la lsita de vértices de la clase de color es cero o no.
		count += 1 if len(cc.vertices) != 0 else 0
	return count