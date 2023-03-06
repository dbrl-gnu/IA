"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import copy

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio
from practica1.agent import Estat


class Rana(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__bota = 0
        self.__caselles_anteriors = [] #usat perque la granota no generi
                                       #com a possibles posicions per on ja ha passat

    def _minimax(self, estat, torn_de_max, max_depth):

        #Casos trivials
        if  max_depth == 0 or estat.es_meta(torn_de_max):
            score = estat.calc_heu_minimax()
            return score, estat.pare[1]

        #Generam els nodes fulla amb la heurística corresponent
        #puntuacio_fills = [self._minimax(estat_fill, not torn_de_max, max_depth=max_depth - 1) for estat_fill in
        #                  estat.genera_fill()]

        estats_generats = estat.genera_fill(torn_de_max, self.__caselles_anteriors)
        puntuacio_fills = list()
        for fills in estats_generats:
            puntuacio_fills.append(self._minimax(fills, not torn_de_max, max_depth=max_depth - 1))

        if torn_de_max:
            if estat.pare is None: #Cas final, retornam la branca que suposa la millor jugada
                return self._max_fills(puntuacio_fills,root=True)
            return self._max_fills(puntuacio_fills),estat.pare[1]
        else:
            return self._min_fills(puntuacio_fills),estat.pare[1]

    #Funcions per evaluar els fills del arbre de minimax segons la seva heuristica

        #Retorna fill amb heurística máxima
    def _max_fills(self, puntuacio_fills, root = None):
        max = puntuacio_fills[0]
        for fill in puntuacio_fills:
            if fill[0] > max[0]:
                max = fill
        if root: #Si el node és la rel de l'arbre
            return max
        return max[0]

        #Retorna fill amb heurística mínima
    def _min_fills(self, puntuacio_fills):
        min = puntuacio_fills[0]
        for fill in puntuacio_fills:
            if fill[0] < min[0]:
                min = fill
        return min[0]

        #Funcio auxiliar per extreure el nom de l'adversari desde la percepio
    def _treure_nom_adv(self, percep):
        noms = set(percep[ClauPercepcio.POSICIO].keys())
        noms.remove(self.nom)
        return noms.pop()

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        #Generam l'estat inicial mitjanćant les dades de la percepció
        estat_inicial = Estat(info=percep.to_dict(), pes=0, cords=percep[ClauPercepcio.POSICIO],
                              meta=percep[ClauPercepcio.OLOR], nom_agent=self.nom, nom_adv=self._treure_nom_adv(percep))
        self.__caselles_anteriors.append(percep[ClauPercepcio.POSICIO][self.nom])

        #bloquejam si una rana guanya
        nom_agents = percep[ClauPercepcio.POSICIO].keys()
        for agents in nom_agents:
            if percep[ClauPercepcio.OLOR] == percep[ClauPercepcio.POSICIO][agents]:
                return AccionsRana.ESPERAR

        #Si esta botant espera
        if self.__bota > 0:
            self.__bota -= 1
            return AccionsRana.ESPERAR

        #Calculam la millor jugada
        accio = self._minimax(estat_inicial, torn_de_max=True, max_depth=3)

        #Si ha de botar, prepara la penalització de dos torns
        if accio[1][0] == AccionsRana.BOTAR:
            self.__bota = 2

        #Retorna l'acció a realitzar
        return accio[1]
