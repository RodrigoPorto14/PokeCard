import pygame
from auxiliares import carregaArquivo

class Carta:
    def __init__(self,nome,poderAtual,poderOriginal,tipo,evolucao):
        local = 'cartas/' + nome + '.png'
        self.__nome = nome
        self.__poderAtual = int(poderAtual)
        self.__poderOriginal = int(poderOriginal)
        self.__tipo = tipo
        self.__evolucao = evolucao
        self.__virada = False
        self.__objeto = pygame.image.load(local)
    
    @property
    def nome(self):
        return self.__nome
    @property
    def poderAtual(self):
        return self.__poderAtual
    @poderAtual.setter
    def poderAtual(self,poder):
        self.__poderAtual=poder
    @property
    def poderOriginal(self):
        return self.__poderOriginal
    @property
    def tipo(self):
        return self.__tipo
    @property
    def evolucao(self):
        return self.__evolucao
    @property
    def virada(self):
        return self.__virada
    @virada.setter
    def virada(self,virada):
        self.__virada=virada
    @property
    def objeto(self):
        return self.__objeto


class Baralho:
    def __init__(self,nomeArquivo,qtd): # Le arquivo e carrega o baralho com cartas comuns
        self.__cartas = []
        dados = carregaArquivo(nomeArquivo,True)
        for i in range(0,len(dados)):
            for j in range(0,qtd):
                self.__cartas.append(Carta(dados[i][0],dados[i][1],dados[i][1],dados[i][2],dados[i][3]))
        del dados
        
    def carregaCartas(self,nomeArquivo,qtd):
        dados = carregaArquivo(nomeArquivo,True)
        for i in range(0,len(dados)):
            for j in range(0,qtd):
                self.__cartas.append(Carta(dados[i][0],dados[i][1],dados[i][1],dados[i][2],dados[i][3]))
        del dados
    
    @property
    def cartas(self):
        return self.__cartas
    