"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from queue import PriorityQueue

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
from practica1.agent import Estat


class Rana(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None



    def _cerca(self, estat_inicial):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_cost(), estat_inicial))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.genera_fill()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calc_cost(), estat_f))

            self.__tancats.add(actual)

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        estat_inicial = Estat(info=percep.to_dict(), pes = 0, cords=percep[ClauPercepcio.POSICIO],
                              meta=percep[ClauPercepcio.OLOR], nom_agent=self.nom)

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

