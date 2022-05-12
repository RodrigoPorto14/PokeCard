import pygame.image,pygame.mixer

# Verifica se arquivo existe
def arquivoExiste(nomeArquivo):
    try:
        arq = open(nomeArquivo,'rt')
        arq.close()
    except FileNotFoundError:
        return False
    else:
        return True

# Passa uma classe de uma lista para a outra
def passaObjeto(lista1,lista2,x,viraCarta=False):
    for j in lista1:
        if(x==lista1.index(j)):
            if(viraCarta):
                j.virada=True
            lista2.append(j)
            lista1.pop(x)
            return

# Verifica se existe elemento repetido em duas listas
def existeRepetido(lista1,lista2):
    for i in lista1:
        for j in lista2:
            if(i==j):
                return True
    return False

# Soma a qtd de pokemons no combo 
def somaQtdPokes(lista):
    soma=0
    for i in lista:
        soma+=i[2]
    return soma

# Remove o combo com maior qtd de pokemons
def removeMaior(lista):
    maior=0 ; indice=0
    for i in lista:
        if(i[2]>=maior):
            maior=i[2]
            indice=lista.index(i)
    lista.pop(indice)

# Calcula o alinhamento para desenhar sprites 
def calculaAlinhamento(qtdCartas,espacoTotal):
    larguraCartas = 50*qtdCartas+15*(qtdCartas-1)
    return (espacoTotal - larguraCartas)/2

# Calcula quantas cartas o jogador possui naquele indice
def calculaCartasNoIndice(indice,cartasTotais):
    if(7*indice<=cartasTotais): 
        return 7
    else:
        return 7-(7*indice-cartasTotais)

# Verifica se um elemento esta na lista
def buscaLinear(lista,x):
    for i in lista:
        if(x==i):
            return True
    return False

# Conta a quantidade de pokemons iguais ao nomes passado na lista
def contaPokeIgual(lista,nome):
    cont=0
    for i in lista:
        if(i.nome==nome):
            cont+=1
    return cont

# Carrega dados do arquivo em uma lista ou dicionario
def carregaArquivo(nomeArquivo,variasLinhas=False,dicionario=False):
    if(dicionario):
        lista={}
    else:
        lista=[]
    if(arquivoExiste(nomeArquivo)):
        arq = open(nomeArquivo,'rt')
        for linha in arq:
            if(variasLinhas):
                lista.append(linha.split())
            elif(dicionario):
                lista[linha.split()[0]] = int(linha.split()[1])
            else:
                lista = linha.split()
        arq.close()
    else:
        print('Arquivo nao existe')
   
    return lista

# Le arquivo carrega objetos e coloca num dicionario
def criaDiretorio(dic,nomeArquivo,audio=False):
    if(arquivoExiste(nomeArquivo)):
        arq = open(nomeArquivo,'rt')
        for linha in arq:
            linha = linha.strip('\n')
            if(audio):
                local = 'audios/' + linha
                dic[linha[:len(linha)-4]]=pygame.mixer.Sound(local)
                dic[linha[:len(linha)-4]].set_volume(0.3)
            else:
                local = 'imagens/' + linha + '.png'
                dic[linha]=pygame.image.load(local)
        arq.close()
    else:
        print('Arquivo nao existe')
    

# Desenha uma sequencia de cartas
def desenhaSequenciaCartas(ox,oy,janela,deck,fonte,indiceInicial,indiceFinal,capa=0):
    k=0
    for i in range(indiceInicial,indiceFinal):
        ajuste = 0
        if(deck[i].poderAtual>=1000):
            ajuste=-3
        if(deck[i].virada):
            janela.blit(capa,(ox+65*k,oy))
        else:
            janela.blit(deck[i].objeto,(ox+65*k,oy))
            if(deck[i].poderAtual>deck[i].poderOriginal):
                cor = (17,126,14)
            else:
                cor = (0,0,0)
            janela.blit(fonte.render(str(deck[i].poderAtual),False,cor),(ajuste+ox+18+65*k,oy+51))      
        k+=1

# Verifica se há 3 pokemons iguais no deck, caso tenha evolui o mesmo
def evoluiPokemon(deck,evolucoes,oponente=False,evolucao=0):
    for i in range(0,len(deck)-2):
        if(contaPokeIgual(deck,deck[i].nome)==3):
            for j in evolucoes:
                if(j.nome==deck[i].evolucao):
                    if(oponente):
                        j.virada=True
                    else:
                        evolucao.play()
                    deck.append(j)
                    evolucoes.remove(j)
                    break
            return list(filter(lambda x:x.nome!=deck[i].nome,deck))
    return deck

# Calcula a carta de maior valor entre as cartas que o oponente comprou
def aplicaIA(compra,dadosIA,fase):
    pontos=[0,0,0,0,0]
    dadosCompra={'nomes':[],'oTipos':[]}
    x=0 # pokemon que esta sendo analisado
    efeitos = carregaArquivo('arquivos/super_efetivo.txt',True)
    # coloca as cartas de compra no banco de dados IA
    if(len(compra)==5): 
        x=1
        for i in compra:
            dadosCompra['nomes'].append(i.nome)
            dadosCompra['oTipos'].append(i.tipo)

    # calcula o valor de cada carta de compra
    for i in compra:
        if(fase>0):
            pontos[compra.index(i)]+= min((dadosIA['nomes'].count(i.nome)),2) * 10000
            pontos[compra.index(i)]+=min((dadosCompra['nomes'].count(i.nome))-x,1) * 10000
            
            if(fase>1):
                pontos[compra.index(i)]+= (dadosIA['oTipos'].count(i.tipo)) * 6000
                pontos[compra.index(i)]+=min((dadosCompra['oTipos'].count(i.tipo))-x,1) * 6000
            
            if(fase>2):
                for j in dadosIA['jTipos']:  
                    for k in efeitos:
                        if(i.tipo==k[0] and j==k[1]):
                                pontos[compra.index(i)]+= 150

            if(i.poderAtual>=1900):
                pontos[compra.index(i)]+=50000

            if((dadosIA['nomes'].count(i.nome))>0):
                pontos[compra.index(i)]+= dadosIA['evolucoes'][i.evolucao]
            else:
                pontos[compra.index(i)]+=i.poderAtual
        else:
            pontos[compra.index(i)]+=i.poderAtual

    dadosCompra.clear()
    dadosCompra.clear()
          
    # retorna o indice da carta com maior valor
    return pontos.index(max(pontos))

# aplica o efeito de insiginia, quando há 3 pokemons diferentes e do mesmo tipo no campo de batalha
def setInsignias(batalha,insignias):
    tipos = carregaArquivo('arquivos/tipos.txt')
    pokesCombo=[]
    for i in tipos:
        for j in batalha:
            if(j.tipo==i and not buscaLinear(pokesCombo,j.nome)):
                pokesCombo.append(j.nome)

        if(len(pokesCombo)>=3):
            insignias.append(i)
            k=0
            for j in batalha:
                for nome in pokesCombo:
                    if(j.nome==nome):
                        j.poderAtual+=300
                        pokesCombo.remove(nome)
                        k+=1
                if(k==3):
                    break
                
        pokesCombo.clear()
    





        



    
            
    




        
            


