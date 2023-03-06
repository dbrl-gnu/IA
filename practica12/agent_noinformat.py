"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
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
        self.__bot = False

    def _cerca(self, estat: Estat):
        self.__oberts = []
        self.__tancats = set()
        self.__oberts.append(estat)

        actual = None
        while len(self.__oberts) > 0:
            actual = self.__oberts[0]
            self.__oberts = self.__oberts[1:]

            if actual in self.__tancats:
                continue

            if not actual.es_legal():
                self.__tancats.add(actual)
                continue

            estats_fills = actual.genera_fill()
            # print("fills generats")
            if actual.es_meta():
                break

            for estat_f in estats_fills:
                self.__oberts.append(estat_f)

            self.__tancats.add(actual)
        if actual is None:
            raise ValueError("Error impossible")

        if actual.es_meta():

            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)

                iterador = pare
            self.__accions = accions
            return True

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        estat_inicial = Estat(info=percep.to_dict(),pes = 0, cords=percep[ClauPercepcio.POSICIO],
                              meta=percep[ClauPercepcio.OLOR], nom_agent=self.nom)

        if self.__accions is None:
            self._cerca(estat_inicial)


        if len(self.__accions) > 0:
            accio = self.__accions.pop()
            if accio[0] == AccionsRana.BOTAR:
                accio_aux = tuple([AccionsRana.ESPERAR])
                self.__accions.append(accio_aux)
                self.__accions.append(accio_aux)
            return  accio
        else:
            return AccionsRana.ESPERAR