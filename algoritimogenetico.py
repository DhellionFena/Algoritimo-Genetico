from random import randint

class Alelo:
    # Atributos unitários de 1 item

    def __init__(self):
        self.valor = randint(0,10)
        self.peso = randint(0,7)
        
        # caso o item não exista mas entre em um cromossomo
        if self.peso == 0:
            self.valor = 0
    
    def sofrer_mutacao(self):
        self.valor = randint(0,10)
        self.peso = randint(0,7)
        
        # caso o item não exista mas entre em um cromossomo
        if self.peso == 0:
            self.valor = 0


class Cromossomo:
    # Conjunto de itens formando um indivíduo
    # ou um cenário ideal para o problema (aka possível solução)

    def __init__(self):
        self.gerar_alelos()
        self.grau_aptidao = 0  # indicador que avalia o quão viável esse cromossomo é para a solução (baseado na soma dos valores)
        self.definir_grau()
        


    def gerar_alelos(self):
        self.cromossomo = []
        for i in range(0,7):
            self.cromossomo.append(Alelo())

    def definir_grau(self):
        soma_valores = 0
        for item in self.cromossomo:
            soma_valores += item.valor
        self.grau_aptidao = soma_valores

    def mostrar_genetica(self):
        print('[')
        for item in self.cromossomo:
            print(f'(Valor: R${item.valor}, Peso: {item.peso})')
        print(']')
    
    def calcular_aptidao(self, peso_max):
        # Cada cromossomo possui um grau de apitidão do quão efetivo a solução é para o problema.
        peso_total = 0
        for item in self.cromossomo:
            peso_total += item.peso
        
        if peso_total > peso_max: #Peso maximo da mochila
            self.grau_aptidao *= 0.2   #Penalidade de 20% caso não cumpra com a solução
    
    def aplicar_taxa_mutacao(self, taxa):
        # A taxa de mutação ocorre para reforçar a randomicidade da solução
        possibilidades = []
        for i in range(1, taxa+1):
            possibilidades.append(i)
        
        for index in range(0, 7):

            # caso a taxa seja 3%, teremos 3/100 chances da mutação ocorrer no alelo 
            if randint(1,100) in possibilidades:
                self.cromossomo[index].sofrer_mutacao()


class Mochila:
    # A mochila é o nosso problema.

    def __init__(self):
        self.peso_max = 15
        self.solucoes = [] # aqui entrarão um conjunto de cromossomos (várias soluções)
        self.povoar_solucoes()


    def povoar_solucoes(self):
        # Adiciona 7 cromossomos
        for i in range (0, 8):
            self.solucoes.append(Cromossomo())
    
    def reodernar_solucoes(self):
        ordem = lambda cromossomo: cromossomo.grau_aptidao
        self.solucoes.sort(key=ordem, reverse=True)
    
    def mostrar_solucoes_atuais(self):
        for item in self.solucoes:
            print(item.mostrar_genetica())
            print("-> Grau: " + str(item.grau_aptidao))
    
    def repovoar_solucoes(self):
        # TODO implementar cruzamento entre cromossomos
        self.reodernar_solucoes()
        aux = self.solucoes[:6] #salva todos menos o ultimo
        cromossomo = self.torneio() #cromossomo novo
        aux.append(cromossomo)
        self.solucoes.clear()
        self.solucoes = aux

        for i in range(0,7):
            self.solucoes[i].calcular_aptidao(15)

        

    def torneio(self):
        self.reodernar_solucoes()
        novo_cromossomo = Cromossomo()
        novo_cromossomo.cromossomo = []
        #juntano o primeiro com o segundo melhor
        for i in self.solucoes[0].cromossomo[:3]:
            novo_cromossomo.cromossomo.append(i)
        
        for i in self.solucoes[1].cromossomo[3:]:
            novo_cromossomo.cromossomo.append(i)
        
        novo_cromossomo.aplicar_taxa_mutacao(5) #5% de mutação por alelo
        novo_cromossomo.definir_grau()

        return novo_cromossomo


mochila = Mochila()
mochila.mostrar_solucoes_atuais()
print ('------------------------------------')
for i in range(0, 2000):
    print('Geração: ' + str(i))
    mochila.repovoar_solucoes()
    mochila.mostrar_solucoes_atuais()
    print ('------------------------------------')


mochila.repovoar_solucoes()
mochila.mostrar_solucoes_atuais()
print ('------------------------------------')