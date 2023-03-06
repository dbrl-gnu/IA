"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
import random
from queue import PriorityQueue

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
from practica1.agent import Estat


class Rana(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__accions = None
        self.__tamindividus = 20
        self.__nindividus = 10

    def _creuament(self):


    def _fitness(self):



    def _cerca(self):
        for individu in range(self.__nindividus):
            accions = []
            naccions = random.randint(1, self.__tamindividus)

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        estat_inicial = Estat(info=percep.to_dict(), pes = 0, cord=percep[ClauPercepcio.POSICIO][self.nom],
                              meta=percep[ClauPercepcio.OLOR])

        if self.__accions is None:
            self._cerca(estat_inicial)

        if len(self.__accions) > 0:
            accio = self.__accions.pop()
            if accio[0] == AccionsRana.BOTAR:
                accio_aux = tuple([AccionsRana.ESPERAR])
                self.__accions.append(accio_aux)
                self.__accions.append(accio_aux)
            return accio
        else:
            return AccionsRana.ESPERAR

