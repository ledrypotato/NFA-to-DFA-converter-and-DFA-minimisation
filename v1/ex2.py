#Sujet: Gram & Lang - Projet L3
#Auteurs: TAYLOR Matt / SOCHAJ Yoann
#Date: 14/01/2021

#import
from itertools import islice
import itertools
from pathlib import Path

#global
while(1):
		try:
			fileName = (input("Enter file name: (without .txt)\n")) #on demande le nom du fichier a l'user
		except ValueError:
			print("Sorry, I didn't understand that.")
			continue
		if (not Path(fileName+".txt").is_file()): #on verifie que le fichier existe
			print("File does not exist.")
			continue
		else:
			break

#fonction pour lire le fichier texte (repris de l'exercice 1 (AFN -> AFD))
def readFile(name):
	listEtat = []
	listTransitions = []
	listEtatTerminaux = []
	listAFN = []
	compteur = 0 #le compteur va servir pour savoir a quelle ligne on se trouve
	with open(name+".txt", "r") as f:
		for line in f:
			if(compteur == 0):
				firstLine = line.split() #la premiere ligne correspond a la liste des etats
				for i in range(len(firstLine)):
					listEtat.append(firstLine[i])
				compteur +=1
			elif(compteur == 1):
				secondLine = line.split() #la deuxieme ligne correspond a l'alphabet
				for i in range(len(secondLine)):
					listTransitions.append(secondLine[i])
				compteur +=1
			elif(compteur == 2):
				thirdLine = line.split() #la troisieme ligne correspond a la liste des etats terminaux
				for i in range(len(thirdLine)):
					listEtatTerminaux.append(thirdLine[i])
				compteur +=1
			else: #le reste concerne l'AFD
				for x in line.split():
					if x.isdigit():
						res = convert(x)
						listAFN.append(res)
					else:
						listAFN.append(x)
	return listEtat, listTransitions, listAFN, listEtatTerminaux

#fonction qui permet de convertir du "text" en int si c'est un entier (enlever les guillemets)
def convert(text):
	try:
		return int(text)
	except ValueError:
		return text

#fonction qui renvoie une liste remplis de 3 de longueur listAFN renvoye de la fonction readFile, elle va nous servir pour separer la liste en sous-listes
def customArr(fileName):
	a, b, c, d = readFile(fileName)
	res = []
	for i in range(int(len(c)/3)):
		res.append(3)
	return res

#fonction qui prend en parametre un etat et retourne le(s) etat(s) vers lequels il "va" avec "a" et "b" (toute l'alphabet)
def destination(state):
	a, b, c, d = readFile(fileName)
	splitL = customArr(fileName)
	newC = iter(c)
	afd = [list(islice(newC, size)) for size in splitL ]

	listDestination = [] #declare an empty list which will contain all the "destination" states
	for sublist in afd:
		if sublist[0] == state:
			listDestination.append(sublist[2]) #on rajoute a notre listDestination l'indice 2 de la sous-liste qui correspond a l'etat "d'arrive"
	return listDestination #return our result

#fonction pour trouver la destination d'une transition en specifiant le depart et le charactere (modifie de l'ex1.py)
def findPath(afd, list, char, printV, newListEtatFinal):
	res  = []
	for state in list:
		for i in range(len(afd)):
			if(afd[i][0] == state and afd[i][1] == char):
				if(afd[i][2] not in res and len(getSublist(newListEtatFinal, afd[i][2])) < 2): #oblige de rajouter cette condition par rapport a l'ex 1 car sinon il va renvoyer vers un etat qui peut ne plus exister
					res.append(afd[i][2])
				else:
					ans = getSublist(newListEtatFinal, afd[i][2]) #on utilise getSublist() pour obtenir la sous liste contenant le resultat pour l'append a res
					if(ans not in res and ans[0] not in res):
						res.append(ans)			
	if(res != [] and printV):
		print("From", list, "with", char, "->", res) #on affiche les informations pour etre lu facilement par l'user
	return res

#fonction qui renvoie la sublist d'une list si elle contient une valeur passe en parametre
def getSublist(l, state):
	for sublist in l:
		for i in range(len(sublist)):
			if state in sublist:
				return sublist

#fonction de minimisation
def miniAfd():
	a, b, c, listEtatTerminaux = readFile(fileName) #on utilise notre fonction definie au dessus pour lire notre fichier et avoir nos variables
	listEtatNonTerminaux = [x for x in a if x not in listEtatTerminaux] #list comprehension pour creer une liste d'etats non terminaux
	print("Etat(s) non terminaux:", listEtatNonTerminaux)

	splitL = customArr(fileName) #ces lignes permettent de remettre c en une liste de sous-listes
	newC = iter(c)
	res = [list(islice(newC, size)) for size in splitL ]

	print("AFD:", res, "\n") #on affiche l'AFD lu du fichier en forme de liste

	#convert the states in the lists to ints not strings
	newListEtatTerminaux = [] #ce passage est obligatoire pour convertir les entiers dans les listes en "vrai" entier et non pas des strings
	for state in listEtatTerminaux:
		newListEtatTerminaux.append(convert(state))

	newListEtatNonTerminaux = [] #de meme pour les etats non terminaux
	for state in listEtatNonTerminaux:
		newListEtatNonTerminaux.append(convert(state))

	listEtatFinal = [] #this list will contain all of the states of the minimized afd
	
	i = 0
	while (i<2):
		for state in newListEtatTerminaux: #on itere sur chaque etat newListEtatTerminaux 
			listDestination = destination(int(state)) #en utilisant la fonction destination() definie au dessus
			if( not (listDestination[0] in newListEtatTerminaux) or not (listDestination[1] in newListEtatTerminaux) ): # ¬(P ^ Q) <=> ¬(P) v ¬(Q) de Morgan
				if(int(state) not in listEtatFinal): #si il n'est pas deja dans la liste
					listEtatFinal.append(convert(state)) #on l'ajoute

		for state in newListEtatNonTerminaux: #de meme pour newListEtatNonTerminaux
			listDestination = destination(int(state))
			if( not (listDestination[0] in newListEtatNonTerminaux) or not (listDestination[1] in newListEtatNonTerminaux) ):
				if(int(state) not in listEtatFinal):
					listEtatFinal.append(convert(state))

		for state in listEtatFinal:
			if state in newListEtatTerminaux:
				newListEtatTerminaux.remove(state)
			if state in newListEtatNonTerminaux:
				newListEtatNonTerminaux.remove(state)
		i+=1

	newListEtatFinal = [ [x] for x in listEtatFinal ] #list of lists using list comprehension
	if(newListEtatTerminaux != []): #on verifie qu'on ne rajoute pas une liste vide
		newListEtatFinal.append(newListEtatTerminaux)
	if(newListEtatNonTerminaux != []):
		newListEtatFinal.append(newListEtatNonTerminaux)

	newListEtatTerminaux = []
	for state in listEtatTerminaux:
		newListEtatTerminaux.append(convert(state))

	listEtatTerminauxMinimise = [ getSublist(newListEtatFinal,x) for x in newListEtatTerminaux ]
	listEtatTerminauxMinimise.sort()
	listEtatTerminauxMinimise = list(listEtatTerminauxMinimise for listEtatTerminauxMinimise, _ in itertools.groupby(listEtatTerminauxMinimise)) #remove duplicates from list

	print("******* RESULTAT *******\n")
	print("Etats de l'AFD minimise:", newListEtatFinal)
	print("Etats terminaux de l'AFD minimise", listEtatTerminauxMinimise)

	for i in range(len(newListEtatFinal)):
		resA = findPath(res, newListEtatFinal[i], "a", 1, newListEtatFinal)
		resB = findPath(res, newListEtatFinal[i], "b", 1, newListEtatFinal)

# **** MAIN ****
def main():
	a, b, c, d = readFile(fileName)
	print("Etats:", a) #correspond a tous les etats (ligne 1 du fichier)
	print("Transitions:", b) #correspond l'alphabet (ligne 2 du fichier)
	print("Etat(s) terminaux:", d) #correspond a tous les etats terminaux (ligne 3 du fichier)

	miniAfd() #on appelle notre fonction principale sur notre AFD

main() #on lance le main !