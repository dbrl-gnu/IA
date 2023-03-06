from practica1 import joc, agent_noinformat, agent_aestrella, agent_genetic


def main():
    rana1 = agent_genetic.Rana("Miquel")
    # rana1 = agent_noinformat.Rana("Vicenç")
    # rana1 = agent_minimax.Rana("Josep")
    # rana2 = agent_minimax.Rana("Pau")
    lab = joc.Laberint([rana1], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
