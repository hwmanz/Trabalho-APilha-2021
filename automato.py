class Automato:
    def __init__(self, template): # construtor
        dados = self.recuperarAtributos(list(template.pop(0)))
        self.alfabeto = dados[0].split(", ")
        self.estados = dados[1].split(", ")
        self.fTransicao = dados[2]
        self.inicial = dados[3]
        self.finais = dados[4].split(", ")
        self.transicao = self.recuperarFuncaoDeTransicao(template)

    # recupera os atributos do automato lendo a primeira linha do arquivo descritor, levando em consideração
    # a necessidade de dados entre chaves serem considerados como um dado só 
    def recuperarAtributos(self, template):
        dados = [] # para retorno
        tempStr = "" # temporario
        capturandoChaves = False
        for currChar in template:
            if capturandoChaves: # necessário pois tudo aquilo que estiver entre chaves deve ser extraído como um unico objeto
                if currChar == "}": # finaliza a captura de dados entre chaves e os "retorna"
                    capturandoChaves = False
                    dados.append(tempStr)
                    tempStr = ""

                else:
                    tempStr += currChar
            
            else:
                if currChar == "{": # inicia a captura de dados entre chaves
                    capturandoChaves = True
                
                elif currChar not in "(), ": # se não for um dos caracteres redundantes, capturar
                    tempStr += currChar
                
                else: # se for, adicionar os dados capturados a lista de dados
                    if tempStr:
                        dados.append(tempStr)
                        tempStr = ""

        return dados

    # itera pelos itens do arquivo descritor recuperando todas as transições do automato
    # as transições são guardadas num dicionário com a estrutura {("estado inicial", "caracter lido"): ("estados de destino")}
    def recuperarFuncaoDeTransicao(self, template): #itera pelas linhas com o formato "estado atual", "caracter", "destino" extraindo todas as transições
        transicao = {}
        for line in template:
            currLine = line.split(", ")

            if (currLine[0], currLine[1]) in transicao.keys(): # se ja existe uma transição que parte do estado atual e lê o mesmo caracter, adicione o novo destino na lista de destinos
                transicao[(currLine[0], currLine[1])].append(currLine[2])
            else: # senão, cria uma transição nova
                transicao[(currLine[0], currLine[1])] = [currLine[2]]

        for key in transicao.keys(): # converter de listas para tupla. por segurança
            transicao[key] = tuple(transicao[key])

        return transicao

    # recebe um estado e um caracter e retorna o resultado desse processamenot
    def processarCaracter(self, estado, caracter):
        destinos = []
        if caracter not in self.alfabeto or estado not in self.estados: # se o estádo ou símbolo não existir
            destinos = self.uniao(destinos, [None]) # transição para estado inexistente

        else: # senão tenta processar o caracter atual
            try:
                destinos = self.uniao(destinos, self.transicao[(estado, caracter)])
            except KeyError:
                destinos = self.uniao(destinos, [None])

        return destinos

    # recebe uma palavra e utiliza a função processarCaracter() para processar a palavra iterando por cada caracter
    def processarPalavra(self, palavra):
        atuais = [self.inicial]

        for caracter in palavra: # itera por cada caracter processando e adicionando o resultado do processamento na lista temporária
            tmp = []
            for estado in atuais:
                tmp = self.uniao(tmp, self.processarCaracter(estado, caracter)) 

            atuais = tmp.copy()


        for estado in atuais: # checa se algum dos estados atigidos ao final do processamento é um estado final
            if estado in self.finais:
                return True

        return False

    #utilizada para evitar a repetição de estados na lista de estados atuais
    def uniao(self, a, b):
        # a = [1, 4, 6, 9]
        # b = [0, 3, 6, 9]
        # unido = [1, 4, 6, 9, 0, 3] 
        unido = []

        for item in a: # adiciona todos os items da lista a na lista unida
            if item not in unido and item != None:
                unido.append(item)

        for item in b: # adiciona os itens da lista b na lista unida ignorando itens repetidos
            if item not in unido and item != None:
                unido.append(item)

        return unido

#boilerplate code
if __name__ == "__main__":
    with open("regras.txt", "r") as regras: #editar regras.txt para mudar o comportamento do automato
        tmp = regras.read().split("\n") #passar como lista simplifica o codigo
        automato = Automato(tmp) 
        palavra = input("insira a palavra a ser processada\n")
        print(automato.processarPalavra(palavra))