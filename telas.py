import pygame
from auxiliares import desenhaSequenciaCartas,calculaAlinhamento,arquivoExiste,calculaCartasNoIndice,criaDiretorio
class Tela:
    def __init__(self):
        self.__img = {}
        self.__janela = pygame.display.set_mode((640,640))
        self.__fonte = pygame.font.SysFont('Arial',11,True)
        self.__fonteTitulo = pygame.font.SysFont('Arial',30,True)
        criaDiretorio(self.img,'arquivos/imagens.txt')
        
    @property
    def img(self):
        return self.__img
    @property
    def janela(self):
        return self.__janela
    @property
    def fonte(self):
        return self.__fonte
    @property
    def fonteTitulo(self):
        return self.__fonteTitulo
    
    def desenhaFundo(self,rodada):
        self.janela.blit(self.img['arena'],(0,0))
        align=0
        if(rodada<10):
            align = 2
        self.janela.blit(self.fonte.render(str(rodada),False,(0,0,0)),(align+316,312))

    def desenhaBarraVida(self,vida,vidaOriginal):
        for i in range(0,2):
            escala=vida[i]/vidaOriginal[i]
            size = round(100*escala)
            desloc = 100-size
            if(size>0):
                self.img['barravida'] = pygame.transform.scale(self.img['barravida'],(size,14))
                self.janela.blit(self.img['barravida'],(desloc+539,526-424*i))
            
            larguraTexto=len(str(vida[i]))*5
            align = (20 - larguraTexto)/2
            self.janela.blit(self.fonte.render(str(vida[i]),False,(0,0,0)),(align+582,527-424*i))


    def desenhaCartasCompra(self,jcompra):
        pygame.draw.rect(self.janela,(0,0,0),(150,275,340,90))
        align = calculaAlinhamento(len(jcompra),310)
        desenhaSequenciaCartas(165+align,285,self.janela,jcompra,self.fonte,0,len(jcompra))

    def desenhaDeckJogador(self,deck,indice):
        qtdCartasNoIndice = calculaCartasNoIndice(indice,len(deck))
        indiceInicial=7*(indice-1)
        indiceFinal = indiceInicial + qtdCartasNoIndice 
        align = calculaAlinhamento(qtdCartasNoIndice,440)
        desenhaSequenciaCartas(align+100,555,self.janela,deck,self.fonte,indiceInicial,indiceFinal)
    
    def desenhaDeckOponente(self,deck):
        indiceFinal=min(len(deck),7)
        align = calculaAlinhamento(indiceFinal,440)
        desenhaSequenciaCartas(align+100,15,self.janela,deck,self.fonte,0,indiceFinal,self.img['capa'])
    
    def desenhaSetas(self,jDeckLen,indice):
        if(7*indice<=jDeckLen):
            qtdCartas=7
        else:
            qtdCartas=7-(7*indice-jDeckLen) 
        align = calculaAlinhamento(qtdCartas,440)
        larguraCartas=440-2*align
        if(indice>1):
            self.janela.blit(self.img['left'],(align+65,580))
        if(jDeckLen-(7*indice)>0):
            self.janela.blit(self.img['right'],(align+115+larguraCartas,580))
    
    def desenhaCamposBatalha(self,rodada):
        qtdCartas=min(rodada,4)
        align=calculaAlinhamento(qtdCartas,245)
        for i in range(0,qtdCartas):
            self.janela.blit(self.img['campo'],(align+195+65*i,370))
            self.janela.blit(self.img['campo'],(align+195+65*i,200))
        qtdCartas=rodada-qtdCartas
        if(qtdCartas>5):
            qtdCartas=5
        align=calculaAlinhamento(qtdCartas,310)
        for i in range(0,qtdCartas):
            self.janela.blit(self.img['campo'],(align+167+65*i,455))
            self.janela.blit(self.img['campo'],(align+167+65*i,115))
    
    def desenhaFases(self,cena):
        if(cena<=5):
            self.janela.blit(self.img['fcompra2'],(38,184))
        else:
            self.janela.blit(self.img['fcompra1'],(38,184))
        if(cena==7):
            self.janela.blit(self.img['fposicao2'],(38,284))
        else:
            self.janela.blit(self.img['fposicao1'],(38,284))
        if(cena==9):
            self.janela.blit(self.img['fbatalha2'],(38,384))
        else:
            self.janela.blit(self.img['fbatalha1'],(38,384))
    
    def desenhaCartasBatalha(self,jBatalha,oBatalha,rodada):
        qtdCartas=min(rodada,4)
        align=calculaAlinhamento(qtdCartas,245)
        qtdCartasJogador=min(len(jBatalha),qtdCartas)
        qtdCartasOponente=min(len(oBatalha),qtdCartas)
        desenhaSequenciaCartas(align+195,370,self.janela,jBatalha,self.fonte,0,qtdCartasJogador,self.img['capa'])
        desenhaSequenciaCartas(align+195,200,self.janela,oBatalha,self.fonte,0,qtdCartasOponente,self.img['capa'])
        if(rodada>4):
            qtdCartas=rodada-qtdCartas
            qtdCartas=min(qtdCartas,5)
            align=calculaAlinhamento(qtdCartas,310)
            qtdCartasOponente= len(oBatalha)-4
            if(len(jBatalha)>4):
                qtdCartasJogador=len(jBatalha)-4
                desenhaSequenciaCartas(align+167,455,self.janela,jBatalha,self.fonte,4,4+qtdCartasJogador,self.img['capa'])
            desenhaSequenciaCartas(align+167,115,self.janela,oBatalha,self.fonte,4,4+qtdCartasOponente,self.img['capa'])
    
    def desenhaInsignias(self,jInsignias,oInsignias):
        for i in range(0,len(jInsignias)):
            self.janela.blit(self.img[jInsignias[i]],(565+25*i,421))
        for i in range(0,len(oInsignias)):
            self.janela.blit(self.img[oInsignias[i]],(565+25*i,202))

    def desenhaTelaTitulo(self,mx,my):
        self.janela.blit(self.img['teladetitulo'],(0,0))
        if(mx>=143 and mx<=477 and my>=249 and my<=322):
            self.janela.blit(self.img['jogar2'],(143,249))
        else:
            self.janela.blit(self.img['jogar1'],(143,249))

        if(mx>=143 and mx<=477 and my>=352 and my<=425):
            self.janela.blit(self.img['sair2'],(143,352))
        else:
            self.janela.blit(self.img['sair1'],(143,352))

    def desenhaTutorial(self,rodada,cena):
        for i in range(1,4):
            if(rodada==i):
                for j in range(1,4):
                    nomeImagem = 'fala' + str(j+(i-1)*3)
                    if(cena==j*2+1):
                        self.janela.blit(self.img[nomeImagem],(163,448))
    
    def desenhaFinalBatalha(self,jVida):
        if(jVida>0):
            vencedor='ASH VENCE'
        else:
            vencedor='BROCK VENCE'
        pygame.draw.rect(self.janela,(0,0,0),(0,281,640,78))
        larguraTexto=len(vencedor)*18
        align = (640 - larguraTexto)/2
        self.janela.blit(self.fonteTitulo.render(vencedor,False,(255,255,255)),(align,303))


        
        


    
