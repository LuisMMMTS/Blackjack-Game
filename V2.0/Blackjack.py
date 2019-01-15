from random import shuffle as shuffle
import numpy as np
from time import sleep as sleep
from matplotlib import pyplot as plt

def BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count):
    baralho2=baralho.copy()
    acao=None
    if n_baralhos==1:
        filename="1 deck_"
    if n_baralhos==2:
        filename="2 decks_"
    else:
        filename="4-8 decks_"
    if len(mao)==2 and n_baralhos!=3:
        acao=tabela_cartas(filename,regra,n_baralhos,maodealer,mao)
    elif n_baralhos!=3:
        acao=tabela_valores(filename,regra,n_baralhos,maodealer,mao)
    #true_count=running_count/n_baralhos
    if acao==None:
        acao=float(calcula_hint(mao,maodealer,baralho2,""))
    
        #falta introduzir aqui ação da contagem de cartas
        if (acao>0.27 or 0==np.random.choice(2,size=1,p=[acao,1-acao])): #true_count>(valor(mao)-valor(maodealer[0])):
            return "STAND"
        else:
            return "HIT"
    else:
        if acao=="SP" and ("SP" in moves_available):
            return "SPLIT"
        if acao=="H":
            return "HIT"
        elif acao=="D":
            return "DOUBLE"
        else:
            return "STAND"
    
def tabela_cartas(filename,regra,n_baralhos,maodealer,mao):
    filename=filename+"cards.csv"
    file=open(filename,"r")
    lista=list(file)
    i=lista[0].split(";")
    if maodealer[0][0] in i:
        i=i.index(maodealer[0][0])
    else:
        return
    mao.sort(key=lambda x:x[0],reverse=True)
    mao=list(map(lambda x:x[0],mao)) #neste caso não precisamos do naipe da carta
    s=""
    for n in mao:
        s=s+n
    s1=s[0]
    mao=s1
    for j in lista:
        if mao in j.split(";"):
            file.close()
            return j.split(";")[i]

def tabela_valores(filename,regra,n_baralhos,maodealer,mao):
    filename=filename+"points.csv"
    file=open(filename,"r")
    lista=list(file)
    i=lista[0].split(";")
    if maodealer[0][0] in i:
        i=i.index(maodealer[0][0])
    else:
        return
    mao.sort(key=lambda x:x[0],reverse=True)
    for j in lista:
        if valor(mao) in j.split(";"):
            file.close()
            return j.split(";")[i]


def ler_baralho_inicial(n_baralhos):
    """Lê um baralho do ficheiro com o número específicado
    como parâmetro e devolve o baralho contido neste.
    Por exemplo dado 10 como argumento a função deve ler o ficheiro
    de nome "baralho_10.txt".

    Requires: n: um inteiro positivo n, que representa o número do
    baralho a ler.
    Ensures: O baralho contido no ficheiro, como uma lista de
    pares de strings (face, naipe)
    """

    baralho=("baralho_"+"1")
    baralhoronda=open((baralho)+".txt","r")
    stringbaralho=baralhoronda.read()
    listabaralho=stringbaralho.split("\n")
    
    novalista = []
    del listabaralho[52]
    for j in range (len(listabaralho)):
        t = ()
        a,b = listabaralho[j].split(" ")        
        t =(a,b)
        for i in range(n_baralhos):
            novalista.append(t)
    shuffle(novalista)
    baralhoronda.close()
    return novalista

def maoinicialjogador(y):
    """Lê a lista do baralho e devolve a mao inicial do jogador.

    Requires: Uma lista de cartas(pares de strings (face, naipe))ordenados.
    Ensures: Cartas iniciais do jogador em formato de lista de pares de strings(face, naipe).
    """

    maodojogador=(y)[0:4:2]
    return maodojogador

def maoinicialdealer(y):
    """Lê a lista do baralho e devolve a mao inicial do dealer.

    Requires: Uma lista de cartas(pares de strings (face, naipe))ordenados.
    Ensures: Cartas iniciais do dealer em formato de lista de pares de strings(face, naipe).
    """
    maododealer=(y)[1:5:2]
    return maododealer

def valorcarta(a):
    """Calcula o valor de uma carta.

    Requires:Uma carta(tuplo com par de strings (face, naipe))
    Ensures: Um inteiro com o valor da carta
    """
    valorcarta=0
    if ("10"==a) or ("K"==a) or ("Q"==a) or ("J"==a):
       valorcarta=10
    elif "9"==a:
       valorcarta=9
    elif "8"==a:
       valorcarta=8
    elif "7"==a:
        valorcarta=7
    elif "6"==a:
        valorcarta=6
    elif "5"==a:
        valorcarta=5
    elif "4"==a:
        valorcarta=4
    elif "3"==a:
        valorcarta=3
    elif "2"==a:
        valorcarta=2
    elif "A"==a:
        valorcarta=11    
    return(valorcarta)

def valor(mao):
    """Calcula o valor de uma mão.
    Por exemplo, dada a seguinte mão:
        [("5", "P"), ("K", "C")]
    A função deve devolver o inteiro 15.

    Requires: Uma mão (lista de pares de strings (face, naipe))
    Ensures: Um inteiro com o valor total da mão
    """
    s=0
    As=0
    for carta in mao:
        a=carta[0]
        s=s+valorcarta(a)
        if "A"==a:
           As+=1
    while s>21 and As>0:
        s-=10
        As-=1
    return(s)

def bust(mao):
    """Verifica se uma mão 'rebenta', ou seja, se o valor da mão
    ultrapassa os 21 pontos.
    Por exemplo, dada a seguinte mão:
        [("10", "P"), ("K", "C"), ("2", "E")]
    A função deve devolver o valor True.

    Requires: mao: uma mão (lista de pares de strings (face, naipe))
    Ensures: um Booleano (True ou False), consoante o valor da mão
    ultrapassa ou não os 21 pontos
    """
    resposta=False
    if valor(mao)>21:
        resposta=True
    return resposta

def blackjack(mao):
    """Verifica se uma mão representa um blackjack, ou seja, se contém
    exactamente um ás e uma carta de valor 10.
    Por exemplo, dada a seguinte mão:
        [("A", "P"), ("10", "C")]
    A função deve devolver o valor True.

    Requires: mao: uma mão (lista de pares de strings (face, naipe))
    Ensures: um Booleano (True ou False), consoante a mão contém
    ou não um ás e uma carta de valor 10.
    """
    resposta=False
    if valor(mao)==21 and len(mao)==2:
        resposta=True
    return resposta

def soft(mao):
    """Verifica se uma mão é 'soft' ou 'hard', ou seja, se a adição de mais uma
    carta à mão nunca fará o jogador 'rebentar'.
    Por exemplo, dada a seguinte mão:
        [("A", "P"), ("6", "C")]
    A função deve devolver o valor True.

    Requires: mao: uma mão (lista de pares de strings (face, naipe))
    Ensures: um Booleano (True ou False). True se a adição de uma carta à mão
    nunca possa fazer o seu valor ultrapassar os 21 pontos (mão 'soft'). False
    False caso a adição de uma carta à mão a possa fazer ultrapassar os 21
    pontos (mão 'hard').
    """
    s=0
    As=0
    for carta in mao:
            a=carta[0]
            s=s+valorcarta(a)
            if "A"==a:
               As+=1
    while s>21 and As>0:
            s-=10
            As-=1
    valorcomasavaler1=valor(mao)-10*As
    diferença=21-valorcomasavaler1
    if diferença>=10:
           resposta=True
    if diferença<10:
           resposta=False
    return resposta


def decisao_dealer(mao,regra):
    """Calcula a decisão do dealer ("HIT" ou "STAND") consoante a mão e a
    regra do casino dadas como argumento.

    Requires: mao: uma mão (lista de pares de strings (face, naipe)); regra: uma
    string ("S17" ou "H17") que indica qual a regra do casino.
    Ensures: uma de duas strings ("HIT" ou "STAND"), consoante o valor da
    mão e a regra do casino dada.
    """
    if valor(mao)<17:
        decisao="HIT"
    elif valor(mao)==17 and regra=="s17":
        decisao="STAND"
    elif valor(mao)==17 and regra=="h17" and soft(mao)==True:
        decisao="HIT"
    elif valor(mao)==17 and regra=="h17" and soft(mao)==False:
        decisao="STAND"
    else:
        decisao="STAND"
    return decisao

def calcula_hint(mao,maodealer,baralho,mao2):
    """Calcula a probabilidade de o jogador rebentar se fizer "HIT" sobre a mão
    dada, com base nas cartas que estão visíveis (as suas e as cartas visíveis da
    mão do dealer).

    Requires: mao_jogador: a mão do jogador (lista de pares de strings (face, naipe)), e
    mao_dealer: a mão do dealer (lista de pares de strings (face, naipe))
    Ensures: um float representando a probabilidade de o jogado rebentar se
    fizer "HIT", dadas as cartas em jogo, arredondado à terceira casa decimal
    """
    maoconhecidadealer=[maodealer[0]]
    for z in mao:
        baralho.remove(z)
    for j in maoconhecidadealer:
        baralho.remove(j)
    if len (mao2)>0:
        for z in mao2:
            baralho.remove(z)
    s=0
    As=0
    for c in mao:
        a=c[0]
        s=s+valorcarta(a)
        if "A"==a:
               As+=1
    valor_com_as_a_valer_1=s-10*As
    diferença=21-valor_com_as_a_valer_1
    ncasosfavoraveis=0
    Asnobaralho=4-As
    for e in baralho:
        (x)=e[0]
        if valorcarta(x)>diferença:
            ncasosfavoraveis=ncasosfavoraveis+1
    if ncasosfavoraveis!=0:
        ncasosfavoraveis=ncasosfavoraveis-Asnobaralho
    else:
        ncasosfavoraveis=ncasosfavoraveis
    probabilidade=format((ncasosfavoraveis/len(baralho)),".3f")
    return probabilidade

def maoaimprimir(mao):
    """funçao que ao receber uma mao(lista de tuplos com pares de strings)) devolve a mao num conjunto de cartas de formato (face,naipe)

    Requires:Uma lista de tuplos com pares de strings
    Devolve:a mao num conjunto de cartas de formato (face,naipe)
    """
    stringmao1=""
    stringmao=(str(mao)).replace("'","").replace("[","").replace("]","").replace(" ","")
    indice=1
    for e in stringmao:
        if e!="," or (e=="," and stringmao[(indice)]!="("):
                      stringmao1=stringmao1+e
        indice=indice+1
        
    return stringmao1

def hit(baralho,mao,index,running_count):
    mao.append(baralho[index+1])
    running_count+=run_count(baralho[index+1])
    return (mao,index+1,running_count)

def splitting(baralho,mao,index,running_count):
    mao_aux1,mao_aux2=[],[]
    mao_aux1.append(mao[0])
    mao_aux1.append(baralho[index+1])
    mao_aux2.append(mao[1])
    mao_aux2.append(baralho[index+2])
    running_count+=run_count([baralho[index+1],baralho[index+2]])
    return mao_aux1,mao_aux2,index,running_count

def run_count(x):
    if type (x)==list:
        value=0
        for i in x:
            value+=run_card_value(i)
        return value
    else:
        return run_card_value(x)

def run_card_value(x):
    if x[0]=="2" or x[0]=="7":
        return 0.5
    elif x[0]=="3" or x[0]=="4" or x[0]=="6":
        return 1
    elif x[0]=="5":
        return 1.5
    elif x[0]=="8":
        return 0
    elif x[0]=="9":
        return (-0.5)
    else:
        return (-1)
    

def ronda(nome,i,baralho,jogador,aposta,regra,running_count,n_baralhos):
    """Função que executa a ronda para o jogador com a sua aposta
    Requires: i int para numero de ronda, lista baralho para saber quais as cartas no deck na ronda, str para nome do jogador
    e int para valor apostado
    Ensures: Duplo (resultado, ganho) onde o resultado é "vitória blackjack"
    , "vitória", "derrota" ou "empate"
    e ganho é um valor positivo ou negativo que é o que o jogador ganhou
    ou perdeu nesta ronda
    """
    y=baralho #saber qual é o baralho da ronda
    mao=maoinicialjogador(y) #mão do jogador sendo inicialmente a função maoinicialjogador
    running_count+=run_count(mao)
    maodealer=maoinicialdealer(y)#mão do dealer sendo inicialmente a função maoinicialdealer
    running_count+=run_count(maodealer[0])#o jogador só conhece a primeira carta da mão do dealer
    index=3  #indice para ultima carta a sair
    mao2=[] #no caso de o jogador escolher hint é necessário a variável estar já criada
    split=False
    opçao1=""
    opçao2=""
    moves_available=[]
    ###Texto impresso no início de cada ronda
    print("*** Ronda",i,"***")
    sleep(1)
    print("Dealer:"+(str(maodealer[0]).replace("'","").replace(" ","")+"(?,?)"))
    sleep(1)
    print("Jogador: "+maoaimprimir(mao),"-",valor(mao),"-")
    sleep(1)
    print()
    print("* Joga",jogador,"*")
    sleep(1)
    
    ###Procedimento caso ocorra blackjack inicialmente
    if blackjack(mao):  
        print(jogador,"fez BLACKJACK!")
        sleep(1)
        if valor(maodealer[0])>=10:
            print("Mao dealer:")
            sleep(1)
            print(maoaimprimir(maodealer),"-",valor(maodealer),"-")
            sleep(1)
            if blackjack(maodealer)==True:
                print("Dealer fez BLACKJACK!")
                sleep(1)
                return("empate","0.0"),index,running_count 
            else:
                return("vitoria blackjack",(1.5*aposta)),index,running_count
        else:
            return("vitoria blackjack",(1.5*aposta)),index,running_count
    else:
        i=-1 #contador de decisões do jogador
        while opçao1!="STAND" and not bust(mao)and valor(mao)<21:
            if opçao1!="HINT":
                i+=1
            if split:
                moves_available=["H","S"]
                if nome=="BOT":
                    opçao1=BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count)
                else:
                    opçao1=input((maoaimprimir(mao)+"-"+"HIT, STAND ou HINT ? "))
            elif mao[0][0]==mao[1][0] and i==0:
                moves_available=["H","S","DB","SP"]
                if nome=="BOT":
                    opçao1=BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count)
                else:
                    opçao1=input("HIT, STAND, DOUBLE, SPLIT ou HINT ? ")
            elif mao[0][0]==mao[1][0] and i!=0:
                moves_available=["H","S","SP"]
                if nome=="BOT":
                    opçao1=BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count)
                else:
                    opçao1=input("HIT, STAND, SPLIT ou HINT ? ")
            elif mao[0][0]!=mao[1][0] and i==0:
                moves_available=["H","S","DB"]
                if nome=="BOT":
                    opçao1=BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count)
                else:
                    opçao1=input("HIT, STAND, DOUBLE ou HINT ? ")
            else:
                moves_available=["H","S"]
                if nome=="BOT":
                    opçao1=BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count)
                else:
                    opçao1=input("HIT, STAND ou HINT ? ")
            opçao1=opçao1.upper()
            if opçao1!="HIT" and opçao1!="STAND" and opçao1!="HINT" and opçao1!="SPLIT" and opçao1!="DOUBLE": 
                opçao1="STAND"
            sleep(1)
            print(jogador,"decidiu",opçao1)
            if opçao1=="HIT":
                mao,index,running_count=hit(baralho,mao,index,running_count)
                if bust(mao):
                    opçao1="STAND"
                    print(maoaimprimir(mao),"-",(valor(mao)),"-")
                    sleep(1)
                    print("BUST com",valor(mao),"pontos")
                    sleep(1)
                else:
                    print(maoaimprimir(mao),"-",(valor(mao)),"-")
                    sleep(1)
            elif opçao1=="DOUBLE":
                mao,index,running_count=hit(baralho,mao,index,running_count)
                print("A aposta é agora", str(2*aposta))
                aposta=2*aposta
                opçao1="STAND" #cancela o ciclo pois o jogador não pode receber mais cartas
                if bust(mao):
                    opçao1="STAND"
                    print(maoaimprimir(mao),"-",(valor(mao)),"-")
                    sleep(1)
                    print("BUST com",valor(mao),"pontos")
                    sleep(1)
                else:
                    print(maoaimprimir(mao),"-",(valor(mao)),"-")
                    sleep(1)
            elif opçao1=="SPLIT":
                if mao[0][0]=="A":
                    opçao1="STAND" #neste caso depois já não é permitido fazer hit
                mao,mao2,index,running_count=splitting(baralho,mao,index,running_count)
                split=True
                print(maoaimprimir(mao),"-",(valor(mao)),"-")
                sleep(1)
                print(maoaimprimir(mao2),"-",(valor(mao2)),"-")
                sleep(1)
                print("A aposta é agora", str(2*aposta))
            elif opçao1=="HINT":
                print("A probabilidade de rebentar com a proxima carta e':", calcula_hint(mao,maodealer,baralho,mao2))

        if split:
            while opçao2!="STAND" and not bust(mao2)and valor(mao2)<21:
                if nome=="BOT":
                    moves_available=["H","S"]
                    opçao2=BOT(regra,n_baralhos,maodealer,mao,baralho,moves_available,running_count)
                else:
                    opçao2=input((maoaimprimir(mao2)+"-"+"HIT, STAND ou HINT ? "))
                opçao2=opçao2.upper()
                if opçao2!="HIT" and opçao2!="STAND" and opçao2!="HINT" and opçao2!="SPLIT": 
                    opçao2="STAND"
                print(jogador,"decidiu",opçao2)
                if opçao2=="HIT":
                    mao2,index,running_count=hit(baralho,mao2,index,running_count)
                    if bust(mao2):
                        opçao2=="STAND"
                        print(maoaimprimir(mao2),"-",(valor(mao2)),"-")
                        sleep(1)
                        print("BUST com",valor(mao2),"pontos")
                        sleep(1)
                    else:
                        print(maoaimprimir(mao2),"-",(valor(mao2)),"-")
                        sleep(1)
                elif opçao2=="HINT":
                    print("A probabilidade de rebentar com a proxima carta e':", calcula_hint(mao,maodealer,baralho,mao2))
        if bust(mao) and not split:
            return ("derrota",(-1)*aposta),index,running_count
        elif bust(mao) and split:
            if bust(mao2):
                return ("derrota",(-2)*aposta),index,running_count
        else:
                print()
                print("* Joga dealer *")
                sleep(1)
                print("Mao dealer:")
                sleep(1)
                print(maoaimprimir(maodealer),"-",valor(maodealer),"-")
                running_count+=run_count(maodealer[1])#agora conhecemos a segunda carta da mao do dealeer
                sleep(1)
                if blackjack(maodealer) and valor(mao)<21 and not split: #Se ocorreu blackjack ao dealer e não ao jogador
                    print("Dealer fez BLACKJACK!")
                    sleep(1)
                    return("derrota",(-1)*aposta),index,running_count
                elif blackjack(maodealer) and valor(mao)<21 and split:
                    print("Dealer fez BLACKJACK!")
                    sleep(1)
                    if valor(mao2)==21:
                        return("empate","0.0"),index,running_count
                elif blackjack(maodealer) and valor(mao)==21 and split:
                    print("Dealer fez BLACKJACK!")
                    if valor(mao2)<21:
                        return("empate","0.0"),index,running_count
                    else:
                        return("derrota",(-2)*aposta),index,running_count
                elif blackjack(maodealer) and valor(mao)==21 and not split:
                    print("Dealer fez BLACKJACK!")
                    return("empate","0.0"),index,running_count
                elif not blackjack(maodealer):
                    decisao=decisao_dealer(maodealer,regra)
                    print("Dealer decidiu", decisao)
                    #O ciclo seguinte percorre até o dealer decidir STAND ou ocorra bust ao dealer
                    while decisao!="STAND" and bust(maodealer)==False:
                        index=index+1
                        maodealer.append(y[index])
                        running_count+=run_count(maodealer[-1])
                        decisao=decisao_dealer(maodealer,regra)
                        print("Mao Dealer:")
                        print(maoaimprimir(maodealer),"-",(valor(maodealer)),"-")
                        print("Dealer decidiu",decisao)
                    if bust(maodealer):
                        print("BUST com",valor(maodealer),"pontos")
                        if not split:
                            return("vitoria",aposta),index,running_count
                        elif not bust(mao2):
                            return("vitoria",2*aposta),index,running_count
                        else:
                            return("vitoria na primeira mao e bust na segunda",0.0),index,running_count
                    elif valor(maodealer)>valor(mao):
                        if split:
                            if valor(mao2)>valor(maodealer)and not bust(mao2):
                                return("empate","0.0"),index,running_count
                            elif valor(mao2)==valor(maodealer):
                                return("derrota na primeira mão e empate na segunda mão", (-1)*aposta),index,running_count
                            else:
                                return("derrota",(-2)*aposta),index,running_count
                        else:
                            return("derrota",(-1)*aposta),index,running_count
                    elif valor(maodealer)<valor(mao):
                        if split:
                            if valor(mao2)>valor(maodealer)and not bust(mao2):
                                return("vitoria",2*aposta),index,running_count
                            elif valor(mao(2))==valor(maodealer):
                                return("vitoria na primeira mão e empate na segunda mão",aposta),index,running_count
                            else:
                                return("vitoria na primeira mao e derrota na segunda mao","0.0"),index,running_count
                        else:
                            return("vitoria",aposta),index,running_count
                    else:
                        if split:
                            if valor(mao2)>valor(maodealer)and not bust(mao2):
                                return("empate na primeira mao e vitoria na segunda mão",aposta),index,running_count
                            elif valor(mao2)==valor(maodealer)and not bust(mao2):
                                return("empate em ambas as mãos","0.0"),index,running_count
                            else:
                                return("empate na primeira mão e derrota na segunda",(-1)*aposta),index,running_count
                        else:
                            return("empate","0.0"),index,running_count
                
                

def jogar():
    """Joga um jogo completo, com um número variável de rondas.
    Esta função produz toda a  interação com o utilizador (de acordo com o
    ilustrado nos exemplos anexos ao enunciado).

    Requires: a função não recebe argumentos
    Ensures: a função não devolve nenhum valor.
    """
    nome=input("Nome do jogador? ")
    n_baralhos=input("Número de baralhos?")
    
    try:
        n_baralhos=int(n_baralhos)
    except:
        n_baralhos=6
    if n_baralhos<=0:
        n_baralhos=6
    baralho_de_jogo=ler_baralho_inicial(n_baralhos)
    running_count=0
    dinheiro=input("Montante inicial (100)?")
    try:
        dinheiro=float(dinheiro)
    except:
        dinheiro=100.0
    dinheiroi=dinheiro
    dinheiro_evolution=[dinheiroi]
    aposta=input("Valor da aposta(10)")
    try:
        aposta=int(aposta)
    except:
        aposta=10
    if aposta<=dinheiro and dinheiro>0 and aposta>0:   #se a aposta é menor ou igual ao dinheiro inicial e o dinheiro é diferente de zero e a aposta é diferente de zero
        regra1=input("Qual a regra do casino (s17 ou h17)?")
        regra=regra1.lower()
        if regra!="s17" and regra!="h17":
            regra="s17"
        print("\n=== Vamos começar ===\nJogador:", nome)
        sleep(1)
        print("Saldo inicial:",dinheiro)
        sleep(1)
        print("Valor da aposta:",aposta,"\n")
        sleep(1)
        r=1   #variavel que nos diz o numero da ronda inicialmente é um pois a ronda um vai ser jogada
        bj=0   #variavel que nos dirá o numero de vitorias por blackjack
        v=0     #variavel que nos dirá o numero de vitorias 
        e=0     #variavel que nos dirá o numero de empates
        d=0    #variavel que nos dirá o numero de derrotas  
        joga="sim"        
        while (joga!="QUIT" and dinheiro>0 and dinheiro>=aposta):  #ciclo que permitira que se desenrole o jogo enquanto o jogador nao desistir, ainda houver dinheiro, e o dinheiro cubra uma aposta perdida
            if len(baralho_de_jogo)<=((1/3)*(52*n_baralhos)):  #refresh do baralho quando 2/3 tiver sido usado
                baralho_de_jogo=ler_baralho_inicial(n_baralhos)
                running_count=0
            resultadoronda,index,running_count=ronda(nome,r, baralho_de_jogo, nome, aposta,regra,running_count,n_baralhos)      #funçao ronda no programa
            print()
            print("resultado da ronda:",resultadoronda[0],"com ganho",resultadoronda[1])
            sleep(1)
            dinheiro=dinheiro+float(resultadoronda[1])
            dinheiro_evolution.append(dinheiro)
            print("O seu saldo actual é:",dinheiro)
            if resultadoronda[0]=="vitoria blackjack":
                bj=bj+1
            if "vitoria" in resultadoronda[0].split():
                v=v+1
            if "derrota" in resultadoronda[0].split():
                d=d+1
            if "empate" in resultadoronda[0].split():
                e=e+1
            if dinheiro<=aposta:
                joga="QUIT"
            if dinheiro>=aposta and nome!="BOT":
                jogar=input("Mais uma ronda (QUIT para terminar)?")
                joga=jogar.upper()
            elif nome=="BOT" and dinheiro>=aposta:
                if r>=10:
                    jogar=input("Mais uma ronda (QUIT para terminar)?")
                    joga=jogar.upper()
                print()
            if dinheiro<aposta:
                print("Saldo insuficiente para continuar!")
            r=r+1

            for i in range(index):
                del baralho_de_jogo[0]#vai dando delete à carta zero do baralho até que todas as cartas jogadas tenham sido removidas
            
        print()        
        print("=== Algumas estatísticas ===")
        sleep(1)
        print(nome,"jogou",(r-1),"rondas")
        sleep(1)
        print("Entrou no jogo com",dinheiroi,"e agora tem "+str(dinheiro)+".")
        sleep(1)
        print("número de vitórias:",(v+bj))
        sleep(1)
        print("número de derrotas:",d)
        sleep(1)
        print("número de empates:",e)
        sleep(1)
        print("vitórias blackjack:",bj)
        sleep(1)
        draw_plot_1(dinheiroi,dinheiro,v,bj,d,e)
        draw_plot_money(dinheiro_evolution)
        
    else:    #texto a imprimir caso o dinheiro introduzido inicialmente seja negativo ou 0 ou a aposta seja maior que o dinheiro introduzido ou a aposta seja 0 
        print()
        print("Saldo insuficiente para continuar!")
        sleep(1)
        print()
        print("=== Algumas estatísticas ===")
        print(nome,"jogou",0 ,"rondas")
        print("Entrou no jogo com",0,"e agora tem 0.")
        print("número de vitórias:",0)
        print("número de derrotas:",0)
        print("número de empates:",0)
        print("vitórias blackjack:",0)

def draw_plot_1(dinheiroi,dinheiro,v,bj,d,e):
    p1=plt.figure(1)
    ind=np.arange(5)
    width = 0.35
    if v!=0:
        l=bj/v
    else:
        l=0
    p1=plt.bar(ind,((dinheiro/dinheiroi),((v+bj)/(v+bj+d+e)),l,((d)/(v+bj+d+e)),((e)/(v+bj+d+e))))
    plt.ylabel('Scores em percentagem')
    plt.title('Estatísticas')
    plt.xticks(ind, ('balanço\n monetário', 'vitórias', 'vitórias blackjack', 'derrotas', 'empates'))
    plt.savefig("C:\\Users\\Luis Miguel\\Desktop\\projeto blackjack\\BOT_1 Baralhos\\Hard\\hint_condition_advanced\\3_Stats_plot.png")
    
def draw_plot_money(dinheiro_evolution):
    p1=plt.figure(2)
    x=[]
    for i in range (len(dinheiro_evolution)):
        x.append(i)
    plt.plot(x,dinheiro_evolution)
    plt.xlabel("ronda")
    plt.ylabel("saldo")
    plt.title("evolução do dinheiro por ronda")
    plt.savefig("C:\\Users\\Luis Miguel\\Desktop\\projeto blackjack\\BOT_1 Baralhos\\Hard\\hint_condition_advanced\\3_money_evolution.png")
    
    

jogar()
input()
