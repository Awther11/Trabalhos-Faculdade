class Carro:
    consumo_km = 1
    def __init__(self, cor, modelo):
        self.cor = cor
        self.modelo = modelo
        self.quantidade_passageiros = 0  
        self.capacidade_bagagem = 500  
        self.tipo_combustivel = 'Água'  
        self.combustivel_nivel = 0 
        self.capacidade_combustivel = 100  
        self.quantidade_portas = 4  
        self.ligado = False
        self.farol_ligado = False
        self.porta_malas_aberto = False
        self.quilometragem = 0
        self.ar_condicionado = False
        self.lista_musicas = ['Pagode russo - Luiz Gonzaga', 'Black - Pearl Jam', 'Sem radar - Ls Jack', 'Chiquitita - ABBA']
        self.musica_atual = None
        self.musica_tocando = False
    
    def abastecer(self, quantidade):
        if quantidade <= 0:
            print('Quantidade inválida!')
            return
        if self.combustivel_nivel + quantidade <= self.capacidade_combustivel:
            self.combustivel_nivel += quantidade
            print(f'O carro {self.modelo} foi abastecido com {quantidade} litros')
            print(f'Combustível atual: {self.combustivel_nivel} / {self.capacidade_combustivel} litros')
        else:
            litros_maximo = self.capacidade_combustivel - self.combustivel_nivel
            self.combustivel_nivel = self.capacidade_combustivel
            print(f'\nO tanque está cheio. {litros_maximo} litros foram abastecidos, e o excesso foi descartado!')
            print(f'Combustível atual: {self.combustivel_nivel} / {self.capacidade_combustivel} litros')

    def ligar(self):
        if not self.ligado:
            self.ligado = True
            print('O carro foi ligado')
        else:
            print('O carro já está ligado')

    def desligar(self):
        if self.ligado:
            self.ligado = False
            print('O carro foi desligado')
        else:
            print('O carro já está desligado')
    
    def ligar_farois(self):
        if not self.farol_ligado:
            self.farol_ligado = True
            print('Os faróis do foram ligados')
        else:
            print('Os faróis já estão ligados')
        
    def desligar_farois(self):
        if self.farol_ligado:
            self.farol_ligado = False
            print('Os faróis foram desligados')
        else:
            print('Os faróis já estão desligados')

    def abrir_porta_malas(self):
        if self.porta_malas_aberto:
            print('O porta-malas já está aberto')
        else:
            self.porta_malas_aberto = True
            print('O porta-malas foi aberto')

    def fechar_porta_malas(self):
        if not self.porta_malas_aberto:
            print('O porta-malas já está fechado')
        else:
            self.porta_malas_aberto = False
            print('O porta-malas foi fechado')

    def embarcar(self):
        if self.quantidade_passageiros < 2: 
            self.quantidade_passageiros += 1
            print(f'Uma pessoa embarcou. Total de passageiros: {self.quantidade_passageiros}')
        else:
            print('O carro já está com a capacidade máxima de passageiros.')

    def desembarcar(self):
        if self.quantidade_passageiros > 0:
            self.quantidade_passageiros -= 1
            print(f'Uma pessoa desembarcou. Total de passageiros: {self.quantidade_passageiros}')
        else:
            print('Não há passageiros para desembarcar')


    def andar(self, distancia):
        if not self.ligado:
            print('O carro não está ligado!')
            return
        if distancia <= 0:
            print('Distância inválida!')
            return
        if self.quantidade_passageiros == 0:
            print('O carro não pode andar sem pelo menos um passageiro!')
            return
    
        consumo_necessario = distancia * Carro.consumo_km
        if self.combustivel_nivel >= consumo_necessario:
            self.combustivel_nivel -= consumo_necessario
            self.quilometragem += distancia
            print(f'O carro percorreu {distancia} km')
            print(f'Combustível restante: {self.combustivel_nivel:.2f} litros')
        elif self.combustivel_nivel > 0:
            distancia_possivel = self.combustivel_nivel / Carro.consumo_km
            self.quilometragem += distancia_possivel
            self.combustivel_nivel = 0
            print(f'O carro percorreu apenas {distancia_possivel:.2f} km por falta de combustível')
            print(f'O tanque agora está vazio')
        else:
            print('O carro está sem combustível e não pode se mover.')




    
    def ligar_ar_condicionado(self):                               # implemento 1 xD
        if not self.ar_condicionado:
            self.ar_condicionado = True
            print('O Ar-condicionado foi ligado')
        else:
            print('O ar-condicionado já estava ligado')

    
    def desligar_ar_condicionado(self):
        if self.ar_condicionado:
            self.ar_condicionado = False
            print('O ar-condicionado foi desligado')
        else:
            print('O ar-condicionado já estava desligado')




    def tocar_musica(self):                                         # implemento 2
        if not self.ligado:
            print('É preciso que o carro esteja ligado para tocar música!')
            return
        if not self.musica_tocando:
            if not self.musica_atual:
                self.musica_atual = 0 
            print(f'Tocando: {self.lista_musicas[self.musica_atual]}')
            self.musica_tocando = True
        else:
            print('A música já está tocando')

    def pausar_musica(self):
        if self.musica_tocando:
            print(f'A música {self.lista_musicas[self.musica_atual]} foi pausada')
            self.musica_tocando = False
        else:
            print('Nenhuma música está tocando')

    def proxima_musica(self):
        if not self.lista_musicas:
            print('Todas as faixas foram tocadas')
            return
        if self.musica_atual is not None:
            self.musica_atual = (self.musica_atual + 1) % len(self.lista_musicas)
        else:
            self.musica_atual = 0
        print(f'Próxima música: {self.lista_musicas[self.musica_atual]}')
        self.musica_tocando = True

    def musica_anterior(self):
        if not self.lista_musicas:
            print('Não há músicas disponíveis')
            return
        if self.musica_atual is not None:
            self.musica_atual = (self.musica_atual - 1) % len(self.lista_musicas)
        else:
            self.musica_atual = len(self.lista_musicas) - 1
        print(f'Música anterior: {self.lista_musicas[self.musica_atual]}')
        self.musica_tocando = True

    def listas_de_musicas(self):
        print('Músicas disponíveis: \n')
        for i, musica in enumerate(self.lista_musicas):
            if i == self.musica_atual:
                print(f'  {i + 1}. {musica} (Tocando)')
            else:
                print(f'  {i + 1}. {musica}')



    def mostrar_dados(self):
        print(f'Modelo: {self.modelo}')
        print(f'Cor: {self.cor}')
        print(f'Passageiros: {self.quantidade_passageiros}/2')
        print(f'Capacidade de bagagem: {self.capacidade_bagagem} L')
        print(f'Combustível: {self.combustivel_nivel}/{self.capacidade_combustivel} litros')
        print(f'Tipo de combustível: {self.tipo_combustivel}')
        print(f'Quilometragem: {self.quilometragem} km')
        print(f'Quantidade de portas: {self.quantidade_portas}')
        print(f'Ligado: {"Sim" if self.ligado else "Não"}')
        print(f'Faróis ligados: {"Sim" if self.farol_ligado else "Não"}')
        print(f'Porta-malas aberto: {"Sim" if self.porta_malas_aberto else "Não"}')
        print(f'Ar-condicionado ligado: {"Sim" if self.ar_condicionado else "Não"}')
        

carro1 = Carro('Preto', 'Kia')

while True:
    print("""\n
Menu de Opções:
[1] Abastecer
[2] Ligar o carro
[3] Desligar o carro
[4] Ligar os faróis
[5] Desligar os faróis
[6] Abrir o porta-malas
[7] Fechar o porta-malas
[8] Embarcar passageiro
[9] Desembarcar passageiro
[10] Andar com o carro
[11] Mostrar dados do carro
[12] Ligar ar-condicionado
[13] Desligar ar-condicionado
[14] Tocar musica
[15] Lista de musicas
[16] Tocar proxima musica
[17] Voltar para a musica anterior
[18] Parar a musica
[19] Sair\n""")

    opcao = input('Escolha uma opção: ')
    
    if opcao == '1':
        quantidade = float(input('Digite a quantidade de combustível para abastecer: '))
        carro1.abastecer(quantidade)
    elif opcao == '2':
        carro1.ligar()
    elif opcao == '3':
        carro1.desligar()
    elif opcao == '4':
        carro1.ligar_farois()
    elif opcao == '5':
        carro1.desligar_farois()
    elif opcao == '6':
        carro1.abrir_porta_malas()
    elif opcao == '7':
        carro1.fechar_porta_malas()
    elif opcao == '8':
        carro1.embarcar()
    elif opcao == '9':
        carro1.desembarcar()
    elif opcao == '10':
        distancia = float(input('Digite a distância em km que o carro deve percorrer: '))
        carro1.andar(distancia)
    elif opcao == '11':
        carro1.mostrar_dados()
    elif opcao == '12':
        carro1.ligar_ar_condicionado()
    elif opcao == '13':
        carro1.desligar_ar_condicionado()
    elif opcao == '14':
        carro1.tocar_musica()
    elif opcao == '15':
        carro1.listas_de_musicas()
    elif opcao == '16':
        carro1.proxima_musica()
    elif opcao == '17':
        carro1.musica_anterior()
    elif opcao == '18':
        carro1.pausar_musica()
    elif opcao == '19':
        print('Encerrando...')
        break
    else:
        print('Opção inválida!')