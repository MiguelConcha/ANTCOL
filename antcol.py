from utils import *
import numpy as np 
import networkx as nx 
import matplotlib.pyplot as plt
import tableprint as tp

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
	W = W(G, color_class)
	if i in W:
		factor_1 = tau_ik(i, k, list_color_classes, t)**alpha
		factor_2 = n_ik(G, list_color_classes, i, k)**beta
		numerator = factor_1 * factor_2
		denominator = _denominator(G, list_color_classes, W, k, alpha, beta, t)
		return numerator / denominator
	return 0

def _denominator(G, list_color_classes, W, k, alpha, beta, t):
	result = 0
	for j in W:
		result += (tau_ik(j, k, list_color_classes, t)**alpha) * (n_ik(G, list_color_classes, j, k)**beta)
	return result


def initialise_trail_matrix(G):
	n = len(G.nodes)
	M = np.zeros((n,n))
	for u in G.nodes:
		for v in G.nodes:
			if u != v:
				M[u][v] = 1.
	return M

def initialise_trail_update_matrix(G):
	n = len(G.nodes)
	return np.zeros((n,n))

def ANTCOL(G, ncycles, nants, alpha, beta, rho):
	t = initialise_trail_matrix(G)
	list_color_classes = []
	for cycle in range(1, ncycles + 1):
		print("ciclo:", cycle)
		delta = initialise_trail_update_matrix(G)
		for ant in range(1, nants + 1):
			print("hormiga:", ant)
			X = G.nodes                              					# Initialise set of uncoloured vertices.
			k = 0                                               		# Initialise number of colors used.
			while X:
				k = k + 1
				C_k = ColorClass(k)										# Initialise colour class k.
				list_color_classes.append(C_k)
				F = X
				print(F)												# Initialise set of vertices still feasible for colour k.
				i = select_with_probability(F, 1/len(F))	   			# Select i ∈ F with probabiliy 1/|F|.
				print(i)
				COLOUR_VERTEX(i, k, list_color_classes, F)				# PENDIENTE
				while F:
					p = P_ik(G, list_color_classes, i, k, alpha, beta, t) 
					i = select_with_probability(F, p)					# Select i ∈ F with probability Pik.
					COLOUR_VERTEX(i, k, list_color_classes, F)			# PENDIENTE
			update_trail_update_matrix(G, delta, k)						# Update trail update matrix.
		update_trail_matrix(G, t, delta, rho)							# Update trail matrix.
	return list_color_classes 											# Return trail matrix.

def COLOUR_VERTEX(i, k, list_color_classes, F):
	X.remove(i)
	C_k = get_color_class(list_color_classes, k)
	C_k.append(i)
	F = difference_lists(F, union_lists(Gamma(G, F, i),[i]))

def update_trail_update_matrix(G, delta, k):
	increase = 1 / k
	for i,row in enumerate(delta):
		for j, entry in enumerate(row):
			if i != j and G.node[i]['color'] != G.node[j]['color']:
				delta[i][j] += increase

def update_trail_matrix(G, t, delta, rho):
	for i,row in enumerate(t):
		for j, entry in enumerate(row):
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

	print("Meta-parámetros:")
	ncycles = 100
	nants = len(G.nodes) // 4
	alpha = 0.5
	beta = 0.5
	rho = 0.5
	print("ncycles: %d\nnants: %d\nα: %.2f\nβ: %.2f\nρ: %.2f" % (ncycles, nants, alpha, beta, rho))


	list_color_classes = ANTCOL(G, ncycles, nants, alpha, beta, rho)

	print("\n> La ejecución ha terminado, dibujando la gráfica...")
	print("Se pintó con %d colores. Hay un total de %d conflictos." % (len(list_color_classes), count_global_conflicts(G)))
	mapping_colors = generate_single_color_list(G, list_color_classes)
	plt.figure()
	title = "Gráfica pintada, " + str(k) + "-partita" 
	plt.title(title, color='red')
	nx.draw(G, node_color=mapping_colors, with_labels=True, font_weight='bold', font_color='white')
	plt.show()