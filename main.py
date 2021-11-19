import pygame
from pygame.locals import *
from sys import exit
import time
from players import *
from cards import Baralho
from battle import *
from auxiliares import carregaArquivo
from telas import Tela

pygame.init()
evolucoes = Baralho('arquivos/evolucoes.txt',2)
tela = Tela()
jogador = Jogador()
oponente = Oponente()
batalha = Batalha()
timer = Timer()

cena=0 ; mx=0 ; my=0 ; indice=1 ; rodada=1 ; tutorial=True
hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
arrow = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
audio={}
criaDiretorio(audio,'arquivos/audios.txt',True)
oponente.dadosIA['evolucoes']=carregaArquivo('arquivos/evolucoes2.txt',False,True)
icon = pygame.image.load('imagens/icon.png')
pygame.display.set_caption('PokeCard')
pygame.display.set_icon(icon)
audio['abertura'].set_volume(0.1)
audio['batalha'].set_volume(0.2)

if(arquivoExiste('arquivos/save.bin')):
    arq = open('arquivos/save.bin','rb')
    tutorial = arq.read()
    print(tutorial)
    arq.close()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if(event.type==MOUSEMOTION):
                mx=pygame.mouse.get_pos()[0]
                my=pygame.mouse.get_pos()[1]
        
        # (0) Cena do menu
        if(cena==0):
            audio['abertura'].play()
            if(mx>=143 and mx<=477 and my>=249 and my<=322):
                pygame.mouse.set_cursor(hand)
                if(event.type==MOUSEBUTTONDOWN):
                    audio['abertura'].stop()
                    audio['click'].play()
                    if(tutorial):
                        cena=1
                    else:
                        cena=2
            else:
                pygame.mouse.set_cursor(arrow)
        
        # (1) Cena do tutorial
        if(cena==1):
            audio['batalha'].play()
            jogador.vida=500 ; oponente.vida=500
            jogador.vidaOriginal=500 ; oponente.vidaOriginal=500
            baralho = Baralho('arquivos/cartas_tutorial.txt',1)
            cena = 3
        
        # (2) Cena liga pokemon
        if(cena==2):
            audio['batalha'].play()
            jogador.vida=5000 ; oponente.vida=5000
            jogador.vidaOriginal=5000 ; oponente.vidaOriginal=5000
            indice=1 ; rodada=1
            baralho = Baralho('arquivos/cartas_comum.txt',6)
            cena = 3
            
        
        # (3-4) Cena de compra das cartas
        elif(cena==3):
            cena = jogador.pegaCincoCartas(baralho,mx,my,event,(arrow,hand),audio['cardflip'],tutorial)
            if(cena==4):
                oponente.pegaCincoCartas(baralho,tutorial)
                cena=5

        # (5-6) Cena de escolha das cartas
        elif(cena==5):
            cena = jogador.escolheDuasCartas(baralho,mx,my,evolucoes.cartas,event,(arrow,hand),(audio['click'],audio['evolucao']),tutorial)
            if(cena==6):
                oponente.escolheDuasCartas(baralho,evolucoes.cartas)            
                cena=7

        # (7-8) Cena de posicionamento dos pokemons
        elif(cena==7):
            cena = jogador.posicionaPokemons(mx,my,indice,rodada,event,(arrow,hand),audio['click'],tutorial)
            if(cena==8):
                oponente.posicionaPokemons(rodada)
                timer.tempoOrigem=time.time()
                if(len(timer.count)<2):
                    timer.criaContador(0)
                    timer.criaContador(0)
                cena=9
        
        indice = jogador.moveDeck(mx,my,indice,event,audio['click'])

    # (9-10) Cena de batalha     
    if(cena==9):
        [cena,jogador.vida,oponente.vida] = batalha.iniciaConfrontos(jogador.batalha,oponente.batalha,timer,jogador.vida,oponente.vida,audio)
        if(cena==10):
            jogador.insignias.clear()
            oponente.insignias.clear()
            jogador.voltaPokemons()
            oponente.voltaPokemons(True)
            rodada+=1
            # Carrega cartas raras e lendarias
            if(rodada==8):
                baralho.carregaCartas('arquivos/cartas_raro.txt',4)
            if(rodada==16): 
                baralho.carregaCartas('arquivos/cartas_lendario1.txt',1)
            if(rodada==24): 
                baralho.carregaCartas('arquivos/cartas_lendario2.txt',1)
            
            if(jogador.vida<=0 or oponente.vida<=0):
                audio['batalha'].stop()
                if(jogador.vida>0):
                    audio['vitoria'].play()
                else:
                    audio['derrota'].play()
                jogador.vida=max(jogador.vida,0)
                oponente.vida=max(oponente.vida,0)
                timer.tempoOrigem=time.time()
                cena=11
            else:
                cena=3
            
    # (11) Cena de fim de jogo
    if(cena==11):
        timer.sec=time.time()-timer.tempoOrigem
        if(timer.sec>=10):
            audio['vitoria'].stop()
            audio['derrota'].stop()
            jogador.deck.clear()
            oponente.deck.clear()
            baralho.cartas.clear()
            if(tutorial):
                tutorial=False
                arq = open('arquivos/save.bin','wb')
                arq.write(bytes(tutorial))
                arq.close()
            cena=0

    # Desenho de sprites
    if(cena==0):
        tela.desenhaTelaTitulo(mx,my)
    else:
        tela.desenhaFundo(rodada)
        tela.desenhaBarraVida((jogador.vida,oponente.vida),(jogador.vidaOriginal,oponente.vidaOriginal))
        tela.desenhaInsignias(jogador.insignias,oponente.insignias)
        tela.desenhaFases(cena)
        tela.desenhaCamposBatalha(rodada)
        tela.desenhaDeckJogador(jogador.deck,indice)
        tela.desenhaDeckOponente(oponente.deck)
        tela.desenhaSetas(len(jogador.deck),indice)
        if(cena==5):
            tela.desenhaCartasCompra(jogador.compra)
        if(len(oponente.batalha)>0 or len(jogador.batalha)>0):
            tela.desenhaCartasBatalha(jogador.batalha,oponente.batalha,rodada)
        if(cena==11):
            tela.desenhaFinalBatalha(jogador.vida)
    
    if(cena>0 and tutorial):
        tela.desenhaTutorial(rodada,cena)
      
    pygame.display.update()