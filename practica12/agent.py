"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import copy

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
from itertools import product


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        return AccionsRana.ESPERAR


class Estat:

    def __init__(self, info: dict, pes: int, pare=None, cords=None, meta=None, nom_agent=None, nom_adv=None):

        self.__pare = pare
        self.__cord = cords
        self.__info = info
        self.__meta = meta
        self.__pes = pes
        self.__nom_agent = nom_agent
        self.__nom_adv = nom_adv

    def __hash__(self):
        return hash(tuple(self.__info))

    def __getitem__(self, item):
        return self.__info[item]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other) -> bool:
        return self.__cord == other.__cord

    def __lt__(self, other):
        #Si el cost és el mateix desempatam amb l'heurística
        return min(self._dist_manhattan(self.__nom_agent), self._dist_manhattan(self.__nom_agent))

    #Comprovam si la posicíó de algún agent és meta
    def es_meta(self, torn_max=None) -> bool:
        if torn_max is not None and not torn_max:
            return self.__cord[self.__nom_adv] == self.__meta
        else:
            return self.__cord[self.__nom_agent] == self.__meta

    #Metodes per accedir al pare
    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    #Metode per generar els posibles estats que deriven de l'estat actual en funció
    #de les diferentes accions que la granota pot realitzar
    def genera_fill(self, torn_max = None, caselles_anteriors =None) -> list:
        #Accions i direccions de la granota
        lista_accions = [AccionsRana.MOURE, AccionsRana.BOTAR, AccionsRana.MOURE]
        lista_direccions = [Direccio.BAIX, Direccio.DALT, Direccio.DRETA, Direccio.ESQUERRE]

        l_fills = list()
        #Cas per al minimax on mos interesa generar els fills de l'adversari
        if torn_max is not None and not torn_max:
            cords_idx = self.__nom_adv
        else:
            cords_idx = self.__nom_agent


        for accio in product(lista_accions, lista_direccions):#Generam totes les possibles accions

            fill = copy.deepcopy(self)
            fill.pare = (self, accio)# Guardam l'accio per arrivar a aquest estat

            # Actualitzam les coordenades del estat fill i assignam el cost
            if accio[0] == AccionsRana.MOURE:
                fill.__cord[cords_idx] = self.__calc_cord(cord=fill.__cord[cords_idx], direccio=accio[1], increment=1)
                fill.__pes += 1
            elif accio[0] == AccionsRana.BOTAR:
                fill.__cord[cords_idx] = self.__calc_cord(cord=fill.__cord[cords_idx], direccio=accio[1], increment=2)
                fill.__pes += 6
            elif accio[0] == AccionsRana.ESPERAR:
                fill.__pes += 0.5
            # Si l'estat fill generat és un estat vàlid, l'afegim a la llista de fills vàlids
            if fill.es_legal(torn_max, caselles_anteriors):
                l_fills.append(fill)
        return l_fills

    # Metode per actualitzar les coodenades
    def __calc_cord(self, cord, direccio, increment):
        cord = list(cord)
        if direccio == Direccio.DALT:
            cord[1] = cord[1] - increment
        elif direccio == Direccio.BAIX:
            cord[1] = cord[1] + increment
        elif direccio == Direccio.DRETA:
            cord[0] = cord[0] + increment
        elif direccio == Direccio.ESQUERRE:
            cord[0] = cord[0] - increment
        return tuple(cord)

    def es_legal(self, torn_max = None, caselles_anteriors = None) -> bool:
        # Cas trivial per al minimax
        if torn_max is not None:

            if not torn_max:
                idx_1 = self.__nom_adv
                idx_2 = self.__nom_agent
            else:
                idx_1 = self.__nom_agent
                idx_2 = self.__nom_adv

            if self.__cord[idx_1] == self.__cord[idx_2] or self.__cord[idx_1] in caselles_anteriors:
               return False
        else:
            idx_1 = self.__nom_agent

        # Comprovam si la posició és una paret o si la posició ja esta ocupada per una agent o si ja ha passat per aquella casella
        if self.__cord[idx_1] in self[ClauPercepcio.PARETS]:
            return False
        else:
            # Comprovam que la posició no estigui fora del tauler
            if self.__cord[idx_1][0] in range(0,self[ClauPercepcio.MIDA_TAULELL][0]) and self.__cord[idx_1][1] in range(0, self[ClauPercepcio.MIDA_TAULELL][1]):
                return True
            else:
                return False

    # Calculam el cost per l'algorisme A*
    def calc_cost(self):
        return self.__pes+self._dist_manhattan(self.__nom_agent)

    # Càlcul de la distancia Manhattan amb les coordenades d'un agent
    def _dist_manhattan(self, nom_agent):
        # Manhattan
        return abs((self.__cord[nom_agent][0] - self.__meta[0])) + abs(self.__cord[nom_agent][1] - self.__meta[1])
    # Càlcul de l'heurística dels nodes fulla de l'arbre minimax
    def calc_heu_minimax(self):
        return self._dist_manhattan(self.__nom_adv)-self._dist_manhattan(self.__nom_agent)

