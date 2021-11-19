import time
from auxiliares import carregaArquivo

class Timer:
    def __init__(self):
        self.tempoOrigem=0
        self.sec=0
        self.count=[]
    
    def criaContador(self,start):
        self.count.append(start)
    
class Batalha:
    def __init__(self):
        self.__placarJogador=0
        self.__placarOponente=0
    
    @property
    def placarJogador(self):
        return self.__placarJogador
    @placarJogador.setter
    def placarJogador(self,placar):
        self.__placarJogador=placar
    @property
    def placarOponente(self):
        return self.__placarOponente
    @placarOponente.setter
    def placarOponente(self,placar):
        self.__placarOponente=placar

    
    def iniciaConfrontos(self,jBatalha,oBatalha,timer,jVida,oVida,audio):
        #qtdConfrontos=min(rodada,9)
        timer.sec=time.time()-timer.tempoOrigem
        if(len(jBatalha)>timer.count[1] and len(oBatalha)>timer.count[1]):
            if(timer.sec>2+4*timer.count[0]):
                audio['cardflip'].play()
                oBatalha[timer.count[0]].virada = False
                efeitos = carregaArquivo('arquivos/super_efetivo.txt',True)
                for i in efeitos:
                    if(jBatalha[timer.count[0]].tipo==i[0] and oBatalha[timer.count[0]].tipo==i[1]):
                        audio['superefetivo'].play()
                        jBatalha[timer.count[0]].poderAtual+=500
                        
                    elif(jBatalha[timer.count[0]].tipo==i[1] and oBatalha[timer.count[0]].tipo==i[0]):
                        audio['superefetivo'].play()
                        oBatalha[timer.count[0]].poderAtual+=500
                timer.count[0]+=1

            if(timer.sec>4+4*timer.count[1]):
                audio['cardflip'].play()
                if(jBatalha[timer.count[1]].poderAtual > oBatalha[timer.count[1]].poderAtual):
                    oBatalha[timer.count[1]].virada = True
                    self.placarJogador+=1
                elif(jBatalha[timer.count[1]].poderAtual < oBatalha[timer.count[1]].poderAtual):
                    jBatalha[timer.count[1]].virada = True
                    self.placarOponente+=1
                else:
                    oBatalha[timer.count[1]].virada = True
                    jBatalha[timer.count[1]].virada = True
                timer.count[1]+=1

        elif(timer.sec>2+4*timer.count[1]):
            if(len(jBatalha)<=timer.count[1] and len(oBatalha)<=timer.count[1]):
                dif=0
            elif(len(jBatalha)<=timer.count[1]):
                dif = (timer.count[1]-len(jBatalha)+1)
            else:
                dif = (timer.count[1]-len(oBatalha)+1)   
            if(self.placarJogador+dif>self.placarOponente):
                audio['dano'].play()
                oVida-= (self.placarJogador+dif)*100
            elif(self.placarJogador+dif<self.placarOponente):
                audio['dano'].play()
                jVida-= (self.placarOponente+dif)*100
            timer.count[0]=0
            timer.count[1]=0
            self.placarJogador=0
            self.placarOponente=0
            
            return [10,jVida,oVida] 
        
        return [9,jVida,oVida]