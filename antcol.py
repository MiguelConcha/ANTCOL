# -*- coding = utf-8 -*-
#!/usr/bin/env python

"""antol.py: Implementación
   de la meteheurística ACO propuesta por Dowsland y Thompson."""
__author__ = "Concha Vázquez Miguel"
__copyright__ = "Copyright (C) 2018 Miguel Concha"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Miguel Concha"
__email__ = "mconcha@ciencias.unam.mx"
__status__ = "Completo"

from utils import *                   # Funciones auxiliares y clases necesarias para el modelado.
import numpy as np 			          # Manipulación de matrices.
import networkx as nx 				  # Gráficas.
import matplotlib.pyplot as plt       # Dibujar las gráficas.
import tableprint as tp 			  # Propósitos estéticos.
from random import uniform            # Generación de números aleatorios.

def tau_ik(i, k, list_color_classes, t):
	"""
	Función para el cálculo de τik del artículo.
	Se refiere al restro ("trail") asociado a colorear el vértoce i
	del color k. Esto depende de los vértices ya coloreados de color k:
	el conjunto Vk.

	:param i: El vértice cuyo rastro será estimado.
	:param k: El color del que habría de colorearse i para el cálculo.
	:param list_color_classes: La lista de clases de colores.
	:param t: La matriz de rastros.
	:return: El rastro asociado de colorear el vértice i de color k.
	:retype: double64.
	"""
	# Se obtiene la clase de color asociado al color k.
	V_k = get_color_class(list_color_classes, k)
	# Viendo el número de vértices en la clase
	length = len(V_k.vertices)
	# Se calcula de acuerdo a la fórmula del artículo.
	summation = 0
	# Recorremos la matriz de rastros.
	for i, row in enumerate(t):
		for j, entry in enumerate(row):
			# Si el vértice está en la clase de color, consideramos su rastro.
			if j in V_k.vertices:
				summation += t[i][j]
	return summation / length

def P_ik(G, list_color_classes, i, k, alpha, beta, t):
	"""
	Función que estima la probabilidad para escoger colorear al vértice
	i del color actual k.

	:param G: networkx.Graph
	:param list_color_classes: La lista de clases de color.
	:param i: El vértice para el que se calculará la probabilidad.
	:param k: La etiqueta del color actual.
	:params alpha beta: Los metaparámetros del ACO.
	:param t: La matriz de rastros.
	:return: La probabilidad de escoger pintar a i del color k.
	:rtype: double64.
	"""
	# Obtenemos la clase de color correspondiente a k
	color_class = get_color_class(list_color_classes, k)
	# A partir de la clase de color, determinando los vértices que puedes
	# ser todavía agregados a ésta.
	w = W(G, color_class)
	if w: 
		if i in w:
			# Calculando los facotres dle numerador de la fórmula (rastro asociado, visibilidad).
			factor_1 = tau_ik(i, k, list_color_classes, t)**alpha
			factor_2 = n_ik(G, list_color_classes, i, k)**beta
			numerator = factor_1 * factor_2
			# Para el denominador, llamamos a otra función auxiliar.
			denominator = _denominator(G, list_color_classes, w, k, alpha, beta, t)
			return numerator / denominator
		# Si es vacía o bien el vértice i no está en w, la probabilidad se define como cero.
		return 0 
	return 0

def n_ik(G, list_color_classes, i, k):
	"""
	La visibilidad de colorear al vértice i del color actual k
	puede definirse por tres reglas distintas como se menciona en el artículo.
	Menciona también que elegir la regla de forma aleatoria se demostró ser mejor. 
	Así es como lo hago.

	:param G: networkx.Graph
	:param list_color_classes: La lista de clases de color.
	:param i: El vértice para el que se calculará la visibilidad.
	:param k: El color del que habría de pintarse i en el cálculo.
	:return: La visibilidad de pintar al vértice i del color actual k.
	:rtype: double64.
	"""
	# Eligiendo aleatoriamente la regla de visibilidad de usar.
	random_choice = randint(1,3)
	# Obteniendo la clase de color para el color k.
	C_k = get_color_class(list_color_classes, k)
	# Obteniendo los vértices que pueden y no pueden agregarse a la clase de color.
	W = W(G, C_k)
	B =  B(G, C_k)
	# Dependiendo de la regla, de aplica la fórmula mencionada en el artículo.
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

	:param G: networkx.Graph
	:param F: El conjunto de vértices que será tomado en cuenta.
	:param i: El vértice cuyos vecinos serán computados.
	:return: La lista de vecinos del vértice i dentro del conjunto F.
	:rtype: [int]
	"""
	neighbors = []
	# Recorremos los vértices de F y para cada uno de ellos vemos si es adyacente
	# al vértice en cuestión i en cuyo caso lo agregamos a la lista que será devuelta.
	for v in F:
		if v in G.adj[i]:
			neighbors.append(v)
	return neighbors

def select_pik(G, list_color_classes, alpha, beta, t, F):
	"""
	Función que recorre la lista F y selecciona un vértice que 
	es devuelto dependiendo de su probabilidad Pik.

	:param 	
	"""
	circular_l = cycle(F)
	for i in circular_l:
		return i
		k = G.node[i]['color']
		coin_toss = uniform(0, 1)
		if coin_toss <= P_ik(G, list_color_classes, i, k, alpha, beta, t):
			return element 

def _denominator(G, list_color_classes, W, k, alpha, beta, t):
	result = 0
	for j in W:
		result += (tau_ik(j, k, list_color_classes, t)**alpha) * (n_ik(G, list_color_classes, j, k)**beta)
	return result

def initialise_trail_matrix(V):
	n = len(V)
	M = np.zeros((n,n))
	for i in range(n):
		for j in range(n):
			if i != j:
				M[i][j] = 1.
	return M

def initialise_trail_update_matrix(t):
	delta = t
	for row in delta:
		for entry in row:
			entry = 0
	return delta

def ANTCOL(G, ncycles, nants, alpha, beta, rho, k):
	tp.banner("Lista de Vértices V: ")
	V = list(G)
	print(V)
	tp.banner("Lista de aristas E: ")
	E = list(G.edges)
	print(E)
	t = initialise_trail_matrix(V)										# Inicializar matriz de rastros.
	list_color_classes = []
	for cycle in range(1, ncycles + 1):
		print("> ciclo:", cycle)
		delta = initialise_trail_update_matrix(t)						# Inicializar matriz de actualización de rastros.

		for ant in range(1, nants + 1):
			print("\t-- hormiga:", ant)
			X = V                               						# Inicializar la lista de vértices no coloreados.
			k = 0                                               		# Inicializar el número de colores usados.
			while X:
				k = k + 1
				C_k = ColorClass(k)										# Inicializar la clase de color k.
				list_color_classes.append(C_k)
								
				F = X													# Inicializar la lista de vértices aún factibles para colorear con k.												
				i = select_with_probability(F, 1/len(F))	   			# Seleccionar i ∈ F con probabilidad 1/|F|.
				COLOUR_VERTEX(i, k, list_color_classes, F, 	X)				
				while F:
					
					i = select_pik(G, list_color_classes, alpha, beta, t, F)
					COLOUR_VERTEX(i, k, list_color_classes, F, X)		
			
			update_trail_update_matrix(G, delta, k)						# Actualizar matriz de actualización de rastros.
		update_trail_matrix(G, t, delta, rho)							# Actualizar matriz de rastros.
	
	return list_color_classes 											# Regresar las clases de color.

def COLOUR_VERTEX(i, k, list_color_classes, F, X):
	X.remove(i)
	C_k = get_color_class(list_color_classes, k)
	C_k.vertices.append(i)
	F = difference_lists(F, union_lists(Gamma(G, F, i),[i]))

def update_trail_update_matrix(G, delta, k):
	increase = 1 / (k + 1)
	for i,row in enumerate(delta):
		for j, entry in enumerate(row):
			if i != j and G.node[i]['color'] == G.node[j]['color']:
				delta[i][j] += increase

def update_trail_matrix(G, t, delta, rho):
	for i in range(len(G.nodes)):
		for j in range(len(G.nodes)):
			if i != j:
				t[i][j] = (rho * t[i][j]) + delta[i][j]

if __name__ == '__main__':

	# Inicio y pidiendo máximo número de vértices al usuario.
	tp.banner("Algoritmo ANTCOL (Algoritmo ACO de Dowsland y Thompson).")
	num_vertices = int(input("Máximo número de vértices (recomiendo 30): "))
	
	# Contrucción de la gráfica k-partita y dibujándola.
	print("> Contruyendo gráfica aleatoria k-partita que sabemos es k-coloreable...")
	G, k = create_k_partite(num_vertices)
	print("\n> Mostrando la gráfica generada (cerrar el plot para continuar)...")
	plt.figure()
	title = "Gráfica G original, " + str(k) + "-partita" 
	plt.title(title, color='blue')
	nx.draw(G, node_color='black', with_labels=True, font_weight='bold', font_color='white')
	plt.show()
	
	# Inicio:
	print("\n> Comenzando ejecución de la metaheurística sobre G...")
	print("\nMeta-parámetros:")
	ncycles = 100
	nants = len(G.nodes) // 4
	alpha = 1
	beta = 0.5
	rho = 0.5
	print("ncycles: %d\nnants: %d\nα: %.2f\nβ: %.2f\nρ: %.2f" % (ncycles, nants, alpha, beta, rho))
	# Inicializando el atributo de color para los vértices.
	clear_colors(G)
	# Ejecutando el ACO.
	list_color_classes = ANTCOL(G, ncycles, nants, alpha, beta, rho, k)
	sol, total_colors = test(G, k)
	# Obteniendo el mapeo de los colores.
	mapping_colors = generate_single_color_list(G, sol)
	colors = get_colors_strings(mapping_colors)
	
	# Dibujando la gráfica resultante y checando el número de conflictos existentes.
	print("\n> La ejecución ha terminado, dibujando la gráfica...")
	plt.figure()
	title = "Gráfica pintada con " + str(total_colors) + " colores" 
	print("No. total de conflictos:", count_global_conflicts(G))
	plt.title(title, color='red')
	nx.draw(G, node_color=colors, with_labels=True, font_weight='bold', font_color='white')
	plt.show()