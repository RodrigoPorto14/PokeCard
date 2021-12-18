from pygame.locals import *
from auxiliares import *
from random import randint,shuffle
import pygame

class Treinador:
    def __init__(self):
        self.__vidaOriginal = 5000
        self.__vida = 5000
        self.__deck = []
        self.__batalha = []
        self.__compra = []
        self.__insignias = []
    
    # passa os pokemons do campo de batalha de volta ao deck
    def voltaPokemons(self,viraCarta=False):
        for i in range(0,len(self.batalha)):
            self.batalha[0].poderAtual = self.batalha[0].poderOriginal
            self.batalha[0].virada=viraCarta
            passaObjeto(self.batalha,self.deck,0,viraCarta)
            self.deck = sorted(self.deck,key=lambda x:(-x.poderAtual,x.nome),reverse=False)

    @property
    def vidaOriginal(self):
        return self.__vidaOriginal
    @vidaOriginal.setter
    def vidaOriginal(self,vida):
        self.__vidaOriginal = vida 
    @property
    def vida(self):
        return self.__vida
    @vida.setter
    def vida(self,vida):
        self.__vida = vida
    @property
    def deck(self):
        return self.__deck
    @deck.setter
    def deck(self,deck):
        self.__deck = deck
    @property
    def batalha(self):
        return self.__batalha
    @property
    def compra(self):
        return self.__compra
    @property
    def insignias(self):
        return self.__insignias


class Jogador(Treinador):
    # Ao clicar no baralho sorteia 5 cartas e coloca na area de compra do jogador 
    def pegaCincoCartas(self,baralho,mx,my,event,cursor,cardflip,tutorial):
        if(mx>=540 and mx<=589 and my>=281 and my<=358):
            pygame.mouse.set_cursor(cursor[1])
            if(event.type==MOUSEBUTTONDOWN):
                cardflip.play()
                if(not tutorial):
                    if(len(baralho.cartas)>=5):
                        for i in range(0,5):
                            rand = randint(0,len(baralho.cartas)-1)
                            passaObjeto(baralho.cartas,self.compra,rand)
                        return 4 
                    else:
                        print('Acabou as Cartas')
                        return 11
                else:
                    for i in range(0,5):
                        passaObjeto(baralho.cartas,self.compra,0)
                    return 4
        else:
            pygame.mouse.set_cursor(cursor[0])
        return 3

    # Ao clica na carta passa a mesma da area de compra para o deck do jogador
    def escolheDuasCartas(self,baralho,mx,my,evolucoes,event,cursor,audio,tutorial): 
        align = calculaAlinhamento(len(self.compra),310)
        x=0 ; cursorType=0 
        if(tutorial):
            x=3
        for i in range(0,len(self.compra)-x):       
            if(mx>=align+165+65*i and mx<=align+215+65*i and my>=285 and my<=355):
                cursorType=1
                if(event.type==MOUSEBUTTONDOWN):
                    audio[0].play()
                    passaObjeto(self.compra,self.deck,i)  
                    self.deck = evoluiPokemon(self.deck,evolucoes,False,audio[1])                    
                    self.deck = sorted(self.deck,key=lambda x:(-x.poderAtual,x.nome),reverse=False)
        pygame.mouse.set_cursor(cursor[cursorType])
        
        # Aguarda o jogador selecionar duas cartas e esvazia a area de compra, devolvendo as cartas para o deck                         
        if(len(self.compra)==3):
            pygame.mouse.set_cursor(cursor[0])
            for i in range(0,3): 
                passaObjeto(self.compra,baralho.cartas,0)
            return 6
        return 5 

    # Ao clicar nas setas move pelo deck de 7 em 7 cartas
    def moveDeck(self,mx,my,indice,event,click):
        qtdCartasIndice=calculaCartasNoIndice(indice,len(self.deck)) 
        align=calculaAlinhamento(qtdCartasIndice,440)
        larguraCartas=440-2*align
        if(indice>1):
            if(mx>=align+65 and mx<=align+85 and my>=580 and my<=600):
                if(event.type==MOUSEBUTTONDOWN):
                    click.play()
                    indice-=1 
         
        if(len(self.deck)-(7*indice)>0):
            if(mx>=align+115+larguraCartas and mx<=align+135+larguraCartas and my>=580 and my<=600): 
                if(event.type==MOUSEBUTTONDOWN):
                    click.play()
                    indice+=1
        
        
        return indice 

    # Ao clicar na carta passa o pokemon do deck para o campo de batalha
    def posicionaPokemons(self,mx,my,indice,rodada,event,cursor,click,dadosIA,tutorial):
        maxPokemons=min(rodada,9) 
        qtdCartasIndice=calculaCartasNoIndice(indice,len(self.deck)) 
        indiceInicial=7*(indice-1) 
        indiceFinal=indiceInicial+qtdCartasIndice
        align=calculaAlinhamento(qtdCartasIndice,440)
        k=0 # valor utilzado para mudar a posicao x da colisao das cartas com o mouse
        cursorType=0
        for i in range(indiceInicial,indiceFinal):
            if(mx>=align+100+65*k and mx<=align+150+65*k and my>=555 and my<=625):
                if(self.deck[i].tipo=='normal' or rodada<3 or not tutorial):
                    cursorType=1
                    if(event.type==MOUSEBUTTONDOWN):
                        click.play()
                        dadosIA.append(self.deck[i].tipo)
                        passaObjeto(self.deck,self.batalha,i) 
            k+=1
        pygame.mouse.set_cursor(cursor[cursorType])
        # Aguarda ate o jogador preencher os campos ou não ter mais cartas no deck
        if(len(self.batalha)==maxPokemons or len(self.deck)==0):
            pygame.mouse.set_cursor(cursor[0])
            setInsignias(self.batalha,self.insignias) # aplica os efeitos de insiginia, caso haja
            return 8
        return 7




class Oponente(Treinador):

    dadosIA = {'nomes':[],'oTipos':[],'jTipos':[],'evolucoes':{}}
    
    # Sorteia 5 cartas e coloca na area de compra do oponente
    def pegaCincoCartas(self,baralho,tutorial):
        if(len(baralho.cartas)>=5):
            if(not tutorial):
                for i in range(0,5):
                    rand = randint(0,len(baralho.cartas)-1)
                    passaObjeto(baralho.cartas,self.compra,rand)
            else:
                for i in range(0,5):
                    passaObjeto(baralho.cartas,self.compra,0)
        else:
            print('Acabou as Cartas')
    
    # Calcula melhor opcao e seleciona duas cartas da area de compra e passa as mesmas para o deck do oponente
    def escolheDuasCartas(self,baralho,evolucoes,fase):
        if(len(self.compra)>0):
            for i in range(0,2):
                self.dadosIA['nomes'].clear()
                self.dadosIA['oTipos'].clear()
                for i in self.deck:
                    self.dadosIA['nomes'].append(i.nome)
                    self.dadosIA['oTipos'].append(i.tipo)
                x = aplicaIA(self.compra,self.dadosIA,fase)
                passaObjeto(self.compra,self.deck,x,True)
                self.deck = evoluiPokemon(self.deck,evolucoes,True)
                self.deck = sorted(self.deck,key=lambda x:(-x.poderAtual,x.nome),reverse=False)
            
            self.dadosIA['jTipos'].clear()
            for i in range(0,3):
                passaObjeto(self.compra,baralho.cartas,0)
            
        else:
            return
    
     # Calcula melhor forma de como posicionar os pokemons
    def posicionaPokemons(self,rodada):
        tipos = carregaArquivo('arquivos/tipos.txt')
        pokesBatalha = min(rodada,len(self.deck),9)
        infoPokes = [] ; indiceMelhores = [] ; pokesIndice=[] ; indiceOtimos=[]
        melhor=0
        for i in range(0,pokesBatalha):
            infoPokes.append([[i],self.deck[i].poderAtual,1])
        if(pokesBatalha>=3):
            for tipo in tipos:
                pokesEncontrados=[] ; poder=0
                for i in self.deck:
                    if(i.tipo==tipo and not buscaLinear(pokesEncontrados,i.nome)):
                        pokesEncontrados.append(i.nome)
                        pokesIndice.append(self.deck.index(i))
                        poder+=i.poderAtual+300
                    if(len(pokesIndice)==3):
                        infoPokes.append([pokesIndice[:],poder,3])
                        break
                pokesEncontrados.clear()
                pokesIndice.clear()
        infoPokes = sorted(infoPokes,key=lambda x:x[1],reverse=True)

        while(somaQtdPokes(infoPokes)>=pokesBatalha):
            i=0 ; qtd=0 ; poderTotal=0
            while(qtd<pokesBatalha):
                if(not existeRepetido(pokesIndice,infoPokes[i][0])):
                    poderTotal+=infoPokes[i][1]
                    qtd+=infoPokes[i][2]
                    for j in infoPokes[i][0]:
                        pokesIndice.append(j)
                i+=1
            if(poderTotal>melhor):
                melhor=poderTotal
                indiceMelhores = pokesIndice[:]
            pokesIndice.clear()
            removeMaior(infoPokes)
        
        indiceMelhores.sort(reverse=True)



        for i in indiceMelhores:
            passaObjeto(self.deck,self.batalha,i)
        shuffle(self.batalha)

        setInsignias(self.batalha,self.insignias)

        