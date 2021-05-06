class Automato:
    def __init__(self, template):
        dados = self.recuperarAtributos(list(template.pop(0)))
        self.alfabeto = dados[0].split(", ")
        self.estados = dados[1].split(", ")
        self.fTransicao = dados[2]
        self.inicial = dados[3]
        self.finais = dados[4].split(", ")
        self.transicao  = self.recuperarFuncaoDeTransicao(template)


    def recuperarAtributos(self, template):
        dados = [] #para retorno
        tempStr = "" #temporario
        capturandoChaves = False
        for currChar in template:
            if capturandoChaves: #necessário pois tudo aquilo que estiver entre chaves deve ser extraído como um unico objeto
                if currChar == "}": #finaliza a captura de dados entre chaves e os "retorna"
                    capturandoChaves = False
                    dados.append(tempStr)
                    tempStr = ""

                else:
                    tempStr += currChar
            
            else:
                if currChar == "{": #inicia a captura de dados entre chaves
                    capturandoChaves = True
                
                elif currChar not in "(), ": #ignorar caracteres desnecessários
                    tempStr += currChar
                
                else:
                    if tempStr:
                        dados.append(tempStr)
                        tempStr = ""

        return dados

    def recuperarFuncaoDeTransicao(self, template): #itera pelas linhas com o formato "estado atual", "caracter", "destino" extraindo todas as transições
        transicao = {}
        for line in template:
            currLine = line.split(", ")
            transicao[(currLine[0], currLine[1])] = currLine[2]

        return transicao

    def processarCaracter(self, estado, caracter):
        if caracter not in self.alfabeto or estado not in self.estados:
            return None #transição para estado inexistente

        else:
            try:
                return self.transicao[(estado, caracter)]
            except KeyError:
                return None

    def processarPalavra(self, palavra):
        atual = self.inicial

        for caracter in palavra: 
            atual = self.processarCaracter(atual, caracter)

        return atual in self.finais

#boilerplate 
if __name__ == "__main__":
    with open("regras.txt", "r") as regras: #editar regras.txt para mudar o comportamento do automato
        tmp = regras.read().split("\n")
        automato = Automato(tmp) #passar como lista simplifica o codigo
        print(automato.processarPalavra("abaaabab"))
        