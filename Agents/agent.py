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

    def __init__(self, info: dict, pes: int, pare=None, cords=None, meta=None, nom_agent=None):

        self.__pare = pare

        self.__cord = self._treure_cords(cords)
        # if len(cords) >1:
        #    self.__cord_adv = self._treur_pos_adv(cords,nom_agent)
        self.__info = info
        self.__meta = meta
        self.__pes = pes

    # @staticmethod
    def _treure_cords(self, cords: dict):
        cordenades = []
        keys = cords.keys()
        for agents in keys:
            cordenades.append(cords[agents])
        return cordenades

    def __hash__(self):
        return hash(tuple(self.__info))

    def __getitem__(self, item):
        return self.__info[item]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other) -> bool:
        return self.__cord == other.__cord

    def __lt__(self, other):
        return min(self.calc_heu(), self.calc_heu())

    def es_meta(self, torn_max=None) -> bool:
        if torn_max is not None and not torn_max:
            return self.__cord[1] == self.__meta
        else:
            return self.__cord[0] == self.__meta

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def genera_fill(self, torn_max=None) -> list:
        lista_accions = [AccionsRana.MOURE, AccionsRana.BOTAR]  # Recordar tornar a posar espera
        lista_direccions = [Direccio.BAIX, Direccio.DALT, Direccio.DRETA, Direccio.ESQUERRE]

        l_fills = list()

        if torn_max is not None and not torn_max:
            cords_idx = 1
        else:
            cords_idx = 0

        for accio in product(lista_accions, lista_direccions):

            fill = copy.deepcopy(self)

            fill.pare = (self, accio)

            if accio[0] == AccionsRana.MOURE:
                fill.__cord[cords_idx] = self.__calc_cord(cord=fill.__cord[cords_idx], direccio=accio[1])
                fill.__pes += 1
            elif accio[0] == AccionsRana.BOTAR:
                fill.__cord[cords_idx] = self.__calc_cord(cord=fill.__cord[cords_idx], direccio=accio[1])
                fill.__cord[cords_idx] = self.__calc_cord(cord=fill.__cord[cords_idx], direccio=accio[1])
                fill.__pes += 6
            elif accio[0] == AccionsRana.ESPERAR:
                fill.__pes += 0.5
            if fill.es_legal(torn_max):
                l_fills.append(fill)
        return l_fills

    # @staticmethod
    def __calc_cord(self, cord, direccio):
        cord = list(cord)
        if direccio == Direccio.DALT:
            cord[1] = cord[1] - 1
        elif direccio == Direccio.BAIX:
            cord[1] = cord[1] + 1
        elif direccio == Direccio.DRETA:
            cord[0] = cord[0] + 1
        elif direccio == Direccio.ESQUERRE:
            cord[0] = cord[0] - 1
        return tuple(cord)

    def es_legal(self, torn_max=None) -> bool:
        if torn_max is not None and not torn_max:
            idx = 1
        else:
            idx = 0
        # Comprovar si la posició és una paret
        if self.__cord[idx] in self[ClauPercepcio.PARETS]:
            return False
        else:
            # Comprovam que la posició no estigui fora del tauler
            if self.__cord[idx][0] in range(0, self[ClauPercepcio.MIDA_TAULELL][0]) and self.__cord[idx][1] in \
                    range(0, self[ClauPercepcio.MIDA_TAULELL][1]):
                return True
            else:
                return False

    def calc_cost(self):
        a = self.calc_heu()
        b = self.__pes
        return b+a

    def calc_heu(self):
        # Manhattan
        c = abs((self.__cord[0][0] - self.__meta[0])) + abs(self.__cord[0][1] - self.__meta[1])
        return c

    def calc_heu_minimax(self):
        a = self.calc_heu()
        b = abs(self.__cord[1][0]-self.__meta[0])+abs(self.__cord[1][1]-self.__meta[1])
        return b-a
