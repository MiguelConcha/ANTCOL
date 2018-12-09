from utils import *
import numpy as np 
import networkx as nx 
import matplotlib.pyplot as plt
import tableprint as tp
from random import uniform

def tau_ik(i, k, list_color_classes, t):
	V_k = get_color_class(list_color_classes, k)
	length = len(V_k)
	summation = 0
	for i, row in enumerate(t):
		for j, entry in enumerate(row):
			if j in V_k.vertices:
				summation += t[i][j]
	return summation / length

def P_ik(G, list_color_classes, i, k, alpha, beta, t):
	color_class = get_color_class(list_color_classes, k)
	w = W(G, color_class)
	if w: 
		if i in w:
			factor_1 = tau_ik(i, k, list_color_classes, t)**alpha
			factor_2 = n_ik(G, list_color_classes, i, k)**beta
			numerator = factor_1 * factor_2
			denominator = _denominator(G, list_color_classes, w, k, alpha, beta, t)
			return numerator / denominator
	return 0

def select_pik(G, list_color_classes, alpha, beta, t, F):
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
	tp.banner("Algoritmo ANTCOL (Algoritmo ACO de Dowsland y Thompson).")

	print("> Contruyendo gráfica aleatoria k-partita que sabemos es k-coloreable...")
	G, k = create_k_partite()
	
	print("\n> Mostrando la gráfica generada (cerrar el plot para continuar)...")
	plt.figure()
	title = "Gráfica G original, " + str(k) + "-partita" 
	plt.title(title, color='blue')
	nx.draw(G, node_color='black', with_labels=True, font_weight='bold', font_color='white')
	plt.show()

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

	print("buenos", list_color_classes)
	print("ya")
	sol, total_colors = test(G, k)
	mapping_colors = generate_single_color_list(G, sol)
	colors = get_colors_strings(mapping_colors)
	print("\n> La ejecución ha terminado, dibujando la gráfica...")
	#print("Se pintó con %d colores. Hay un total de %d conflictos." % (len(list_color_classes), count_global_conflicts(G)))
	#mapping_colors = generate_single_color_list(G, list_color_classes)
	plt.figure()
	title = "Gráfica pintada con " + str(total_colors) + " colores" 
	print("No. total de conflictos:", count_global_conflicts(G))
	plt.title(title, color='red')
	nx.draw(G, node_color=colors, with_labels=True, font_weight='bold', font_color='white')
	plt.show()