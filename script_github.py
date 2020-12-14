import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
import numpy as np
variablex = open("variablex.txt", 'r')
lista_variablex = []
linhas_a_pular = []


def read_variablex(variablex, linhas_a_pular, lista_variablex):
    variablex = variablex
    for line in variablex:
        line = line.split(',')
        try:
            numero = float(line[0] + "." + (line[1].split('\n')[0]))
        except:
            numero = float(line[0].split("\n")[0])
        if numero > 0:
            lista_variablex.append(numero)
        else:
            linhas_a_pular.append(1)

read_variablex(variablex, linhas_a_pular, lista_variablex)

variablex.close()

variabley = open("variabley_original.txt", "r")
lista_variabley = []
def read_flux(variabley, linhas_a_pular, lista_variabley):
	variabley = variabley
	contagem = 0
	for line in variabley:
		contagem = contagem + 1
		if contagem > len(linhas_a_pular):
			line = line.split(',')
			try:
				ante_virgula = line[0]
				pos_virgula = (line[1].split('\n')[0])
				numero =float(ante_virgula+"." + pos_virgula)
			except:
				numero = float(line[0].split("\n")[0])
			lista_variabley.append(numero)

read_flux(variabley, linhas_a_pular, lista_variabley)

variabley.close()

plt.plot(lista_variablex, lista_variabley, "o")
plt.xticks(x, " ")
plt.yticks(y, " ")
plt.show()



#a melhor maneira de resolver este problema é considerar uma linha reta entre x = 1.66e4 e 2.80e4

lista_variablex_ajuste = []
lista_variabley_ajuste = []

def extract_list_to_linear_regression(lista_variablex_ajuste,lista_variabley_ajuste, lista_variablex, lista_variabley ):
	for a in range (len(lista_variablex)):
		if lista_variablex[a] >= 1.70e4 and lista_variablex[a]<= 2.80e4:
			lista_variablex_ajuste.append(lista_variablex[a])
			lista_variabley_ajuste.append(lista_variabley[a])
		
extract_list_to_linear_regression(lista_variablex_ajuste,lista_variabley_ajuste, lista_variablex, lista_variabley )

plt.plot(lista_variablex_ajuste, lista_variabley_ajuste)
plt.xticks(x, " ")
plt.yticks(y, " ")
plt.show()


def linear_regression(lista_variablex_ajuste, lista_variabley_ajuste):
	global intercept, coef
	x = np.asarray(lista_variablex_ajuste).reshape(len(lista_variablex_ajuste),1)
	y = np.asarray(lista_variabley_ajuste).reshape(len(lista_variabley_ajuste),1) # y should be 1D array
	regr = LinearRegression()
	regr.fit(x,y)
	model_score = regr.score(x,y)
	y_predito = regr.predict(x) 
	fig = plt.figure() 
	ax = fig.add_subplot()
	plt.plot(lista_variablex_ajuste, lista_variabley_ajuste, 'o')
	plt.plot(lista_variablex_ajuste, y_predito, '-', color = 'red')
	plt.xticks(x, " ")
	plt.yticks(y, " ")
	plt.show()
	intercept = regr.intercept_
	coef = regr.coef_
	print(model_score)
	print(coef, intercept)
	return coef, intercept

linear_regression(lista_variablex_ajuste, lista_variabley_ajuste)

def filter_with_linear_regression(coef, intercept, lista_variabley, lista_variablex):
	global lista_variablex_final,lista_variabley_final
	lista_variablex_final = []
	lista_variabley_final = []
	for i in range (len(lista_variabley)):
		if (lista_variablex[i] < 30000):
			lista_variabley_final.append(lista_variabley[i])
			lista_variablex_final.append(lista_variablex[i])
		else:
			if abs(lista_variabley[i]- (coef*lista_variablex[i] + intercept))**0.25 < (0.05)**0.25 * lista_variabley[i]**0.25:
				lista_variabley_final.append(lista_variabley[i])
				lista_variablex_final.append(lista_variablex[i])
	return lista_variablex_final, lista_variabley_final

filter_with_linear_regression(coef, intercept, lista_variabley, lista_variablex)
plt.plot(lista_variablex_final, lista_variabley_final)
plt.xticks(x, " ")
plt.yticks(y, " ")
plt.show()


ouvariablexut_variablex = open("tratado_variablex", "w+")
for i in range (len(lista_variablex_final)):
	ouvariablexut_variablex.write(str(lista_variablex_final[i])+ "\n")
ouvariablexut_variablex.close()

ouvariablexut_variabley = open("tratado_variabley", "w+")
for i in range (len(lista_variabley_final)):
	ouvariablexut_variabley.write(str(lista_variabley_final[i])+ "\n")
ouvariablexut_variabley.close()