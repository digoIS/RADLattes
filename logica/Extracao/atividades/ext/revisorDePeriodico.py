

class RevisorDePeriodico:

    periodo = ''
    nomePeriodico = ''

    def __init__(self, partesDoItem):
        # partesDoItem[0] = periodo do trabalho
        # partesDo Item[1] = titulo do periodico
        self.periodo = partesDoItem[0]
        self.nomePeriodico = partesDoItem[1]  
        
        
        
    def __str__(self):
        s  = "\n[REVISOR DE PERIODICO] \n"
        s += "+ PERIODO  : " + str(self.periodo) + "\n"
        s += "+ NOME     : " + str(self.nomePeriodico) + "\n"
        return s

