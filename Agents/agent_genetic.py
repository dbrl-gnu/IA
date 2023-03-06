"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import random

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
from itertools import product


class Rana(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__accions = None
        self.__tamindividus = 15
        self.__nindividus = 20

    # Retorna si l'individu a arribat a la pizzaa
    def _es_meta(self, cord, pizza):
        return self._fitnesss(cord, pizza) == 0

    # Calcula les coordenades de l'individu passant per paràmetre la coordenada anterior i la direcció
    def _calc_coords(self, cord, direccio):
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

    # Comprova si l'acció a fer no es fica a una paret o surt del mapa
    def _es_legal(self, cord, parets, mida) -> bool:
        # Comprovar si la posició és una paret
        if cord in parets:
            return False
        else:
            # Comprovam que la posició no estigui fora del tauler
            if cord[0] in range(0, mida[0]) and cord[1] in range(0, mida[1]):
                return True
            else:
                return False

    # Valida si un individu està a una posició legal o ha arribat a la meta després de moure-se
    def _validacio(self, individu, cord, parets, mida, pizza):
        idx = 0
        for accio in individu:
            bckp_cord = cord
            if accio[0] == AccionsRana.MOURE:
                cord = self._calc_coords(cord, accio[1])
            elif accio[0] == AccionsRana.BOTAR:
                cord = self._calc_coords(cord, accio[1])
                cord = self._calc_coords(cord, accio[1])
            if not self._es_legal(cord, parets, mida):
                cord = bckp_cord
                individu = individu[:idx]
                return individu, cord, False
            elif self._es_meta(cord, pizza):
                individu = individu[:idx + 1]
                return individu, cord, True
            idx += 1
        return individu, cord, False

    # Funció que puntua la qualitat d'un individu mirant la seva distancià amb la pizza
    def _fitnesss(self, cord, pizza):
        return abs((cord[0] - pizza[0])) + abs(cord[1] - pizza[1])

    # Modifica una acció de l'individu o l'afegeix una al final
    def _mutacio(self, individu, accions):
        if random.randint(0, 50) == 0:
            ac = random.randrange(len(accions))
            i = random.randrange(len(individu))
            individu[i] = accions[ac]
        if random.randint(0, 50) == 0:
            ac = random.randrange(len(accions))
            individu.append(accions[ac])
        return individu

    # Comprova si un fill ja està dins la llista de progenitors
    def _rep(self, l_fills, fill):
        for p in l_fills:
            if p[1] == fill:
                return True
        return False

    # Ordena la llista de progenitors i creaua els deu primers entre ells,
    # si cap fill és solució, fa una crida recursiva a si mateix
    def _creuament(self, llista, meta, percep, accions):
        cords = percep[ClauPercepcio.POSICIO][self.nom]
        pizza = percep[ClauPercepcio.OLOR]
        parets = percep[ClauPercepcio.PARETS]
        mida = percep[ClauPercepcio.MIDA_TAULELL]
        fill = []
        while not meta:
            llista.sort(key=lambda tup: tup[0])
            llista = llista[:10]
            l_fills = llista
            for pare in llista:
                for mare in llista:
                    if pare == mare:
                        break
                    tall = random.randint(1, len(pare[1]) + 1)
                    fill1 = pare[1][:tall]
                    fill1.extend(mare[1][tall:])
                    fill2 = mare[1][:tall]
                    fill2.extend(pare[1][tall:])
                    fill1 = self._mutacio(fill1, accions)
                    fill2 = self._mutacio(fill2, accions)
                    fill, cordsp, meta = self._validacio(fill1, cords, parets, mida, pizza)
                    if len(fill) > 0:
                        if meta:
                            return fill
                        if not self._rep(l_fills, fill):
                            puntuacio = self._fitnesss(cordsp, pizza)
                            l_fills.append(tuple([puntuacio, fill]))
                    fill, cordsp, meta = self._validacio(fill2, cords, parets, mida, pizza)
                    if len(fill) > 0:
                        if meta:
                            return fill
                        if not self._rep(l_fills, fill):
                            puntuacio = self._fitnesss(cordsp, pizza)
                            l_fills.append(tuple([puntuacio, fill]))
            fill = self._creuament(l_fills, meta, percep)
        return fill

    # Genera aleatòriament un nombre d'individus i si cap arriba a la meta, crida a la funció de creuament
    def _cerca(self, percep):
        inici = percep[ClauPercepcio.POSICIO][self.nom]
        pizza = percep[ClauPercepcio.OLOR]
        parets = percep[ClauPercepcio.PARETS]
        mida = percep[ClauPercepcio.MIDA_TAULELL]

        p_accions = [AccionsRana.MOURE, AccionsRana.BOTAR, AccionsRana.ESPERAR]
        p_direccions = [Direccio.DRETA, Direccio.ESQUERRE, Direccio.DALT, Direccio.BAIX]
        accions = list(product(p_accions, p_direccions))

        progenitors = []
        solucio = False

        for i in range(self.__nindividus):
            individu = []
            n_accions = random.randint(1, self.__tamindividus)
            for p in range(n_accions):
                individu.append(accions[random.randrange(len(accions))])
            individu, cords, solucio = self._validacio(individu, inici, parets, mida, pizza)
            if solucio:
                self.__accions = individu
                return self.__accions
            if len(individu) > 0:
                puntuacio = self._fitnesss(cords, pizza)
                progenitors.append(tuple([puntuacio, individu]))
        individu = self._creuament(progenitors, solucio, percep, accions)
        self.__accions = individu
        return self.__accions

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        if self.__accions is None:
            self._cerca(percep)
            self.__accions = self.__accions[::-1]

        if len(self.__accions) > 0:
            accio = self.__accions.pop()
            if accio[0] == AccionsRana.BOTAR:
                accio_aux = tuple([AccionsRana.ESPERAR])
                self.__accions.append(accio_aux)
                self.__accions.append(accio_aux)
            return accio
        else:
            return AccionsRana.ESPERAR
