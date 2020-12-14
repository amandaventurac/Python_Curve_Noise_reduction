import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
import numpy as np
tempo = open("tempo_segundos.txt", 'r')
lista_tempo = []
linhas_a_pular = []


def read_tempo(tempo, linhas_a_pular, lista_tempo):
    tempo = tempo
    for line in tempo:
        line = line.split(',')
        try:
            numero = float(line[0] + "." + (line[1].split('\n')[0]))
        except:
            numero = float(line[0].split("\n")[0])
        if numero > 0:
            lista_tempo.append(numero)
        else:
            linhas_a_pular.append(1)

read_tempo(tempo, linhas_a_pular, lista_tempo)

tempo.close()

fluxo = open("fluxo_original.txt", "r")
lista_fluxo = []
def read_flux(fluxo, linhas_a_pular, lista_fluxo):
	fluxo = fluxo
	contagem = 0
	for line in fluxo:
		contagem = contagem + 1
		if contagem > len(linhas_a_pular):
			line = line.split(',')
			try:
				ante_virgula = line[0]
				pos_virgula = (line[1].split('\n')[0])
				numero =float(ante_virgula+"." + pos_virgula)
			except:
				numero = float(line[0].split("\n")[0])
			lista_fluxo.append(numero)

read_flux(fluxo, linhas_a_pular, lista_fluxo)

fluxo.close()

plt.plot(lista_tempo, lista_fluxo, "o")
plt.show()



#a melhor maneira de resolver este problema é considerar uma linha reta entre x = 1.66e4 e 2.80e4

lista_tempo_ajuste = []
lista_fluxo_ajuste = []

def extract_list_to_linear_regression(lista_tempo_ajuste,lista_fluxo_ajuste, lista_tempo, lista_fluxo ):
	for a in range (len(lista_tempo)):
		if lista_tempo[a] >= 1.70e4 and lista_tempo[a]<= 2.80e4:
			lista_tempo_ajuste.append(lista_tempo[a])
			lista_fluxo_ajuste.append(lista_fluxo[a])
		
extract_list_to_linear_regression(lista_tempo_ajuste,lista_fluxo_ajuste, lista_tempo, lista_fluxo )

plt.plot(lista_tempo_ajuste, lista_fluxo_ajuste)
plt.show()


def linear_regression(lista_tempo_ajuste, lista_fluxo_ajuste):
	global intercept, coef
	x = np.asarray(lista_tempo_ajuste).reshape(len(lista_tempo_ajuste),1)
	y = np.asarray(lista_fluxo_ajuste).reshape(len(lista_fluxo_ajuste),1) # y should be 1D array
	regr = LinearRegression()
	regr.fit(x,y)
	model_score = regr.score(x,y)
	y_predito = regr.predict(x) 
	fig = plt.figure() 
	ax = fig.add_subplot()
	plt.plot(lista_tempo_ajuste, lista_fluxo_ajuste, 'o')
	plt.plot(lista_tempo_ajuste, y_predito, '-', color = 'red')
	plt.show()
	intercept = regr.intercept_
	coef = regr.coef_
	print(model_score)
	print(coef, intercept)
	return coef, intercept

linear_regression(lista_tempo_ajuste, lista_fluxo_ajuste)

def filter_with_linear_regression(coef, intercept, lista_fluxo, lista_tempo):
	global lista_tempo_final,lista_fluxo_final
	lista_tempo_final = []
	lista_fluxo_final = []
	for i in range (len(lista_fluxo)):
		if (lista_tempo[i] < 30000):
			lista_fluxo_final.append(lista_fluxo[i])
			lista_tempo_final.append(lista_tempo[i])
		else:
			if abs(lista_fluxo[i]- (coef*lista_tempo[i] + intercept))**0.25 < (0.05)**0.25 * lista_fluxo[i]**0.25:
				lista_fluxo_final.append(lista_fluxo[i])
				lista_tempo_final.append(lista_tempo[i])
	return lista_tempo_final, lista_fluxo_final

filter_with_linear_regression(coef, intercept, lista_fluxo, lista_tempo)
plt.plot(lista_tempo_final, lista_fluxo_final)
plt.show()


output_tempo = open("tratado_tempo", "w+")
for i in range (len(lista_tempo_final)):
	output_tempo.write(str(lista_tempo_final[i])+ "\n")
output_tempo.close()

output_fluxo = open("tratado_fluxo", "w+")
for i in range (len(lista_fluxo_final)):
	output_fluxo.write(str(lista_fluxo_final[i])+ "\n")
output_fluxo.close()