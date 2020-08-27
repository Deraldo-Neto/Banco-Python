import mysql.connector

def GainLoss(Media,tabela,HoraInicio,HoraFim,intervaloGain,intervaloLoss,primeiradata,CV,MesTotal):

    listaGainLoss = []
    GainLoss = []
    RDia = 0
    RMes = []
    contMes = 0
    qtdOp = []
    opqtdop = 0
    alvo = False
    if MesTotal:
        for i in range(0,len(tabela)):
            RMes.append(tabela[i][0].split('.'))
            RMes[-1] = RMes[-1][1]
            qtdOp.append(0)
    for i in range(0,len(tabela)):
            qtdOp.append(0)
    dia = False
    sr = False
    # Cria conexão com banco MySQL
    vConexao = mysql.connector.connect(user='root', password='sysdba',
                                    host='127.0.0.1',
                                    database='db_indicadores')
    vCursor = vConexao.cursor()

    # Zerando as informações da tabela
    vComando_sql = "UPDATE cruza_medias SET CV = null, Posicao = null, Gain = null, Loss = null, QtdOp = null, Resultado = null, RDia = null, RMes = null"
    vCursor.execute(vComando_sql)
    vConexao.commit()

    for i in range((Media+1), len(tabela)): # Da maior média +1 até o tamanho da tabela
        hora = tabela[i][1].split(':') # Divido a hora em duas partes (por exemplo -> 9:10 = 9,10)
        hora = int(hora[0])*60 + int(hora[1]) # Multiplico por 60 a hira e somo com os minutos

        if hora < HoraFim and hora >= HoraInicio: # Se a hora for menor que o final da hora definida e maior ou igual a hora de inicio
            proxhora = tabela[i+1][1].split(':')
            proxhora = int(proxhora[0])*60 + int(proxhora[1])
            # CV é Vendido ou comprado, se tá como Vendido, o cont é igual a True (preciso desse cont para q  a função execute uma única vez, caso não ela não existisse, a função iria executar enquanto o CV permanecesse V)
            # E o Minimo é menor ou igual ao Gain OU o Máximo é menor ou igual ao Gain
            if CV == 'V' and cont == True and ((int(tabela[i][3]) < GainLoss[-1][2]) or (int(tabela[i][4]) < GainLoss[-1][2])) and not(HoraFim == proxhora): # Caso Max < Gain ou Min < Gain
                tabela[i][7] = 'C' # Define essa linha como 'C'
                tabela[i][8] = intervaloGain # Resultado
                RDia += tabela[i][8]
                cont = False
                if opqtdop == 1:
                    qtdOp[i] = 1
                    opqtdop = 0
                alvo = True
                sr = True
            # A diferença é que caso o Máximo NÃO seja menor ou igual ao ao Gain ou o Min NÃO é menor ou igual ao Gain
            if CV == 'C' and cont == True and ((int(tabela[i][3]) > GainLoss[-1][2]) or (int(tabela[i][4]) > GainLoss[-1][2])) and not(HoraFim == proxhora): # Caso Max > Gain ou Min > Gain
                tabela[i][7] = 'V'
                tabela[i][8] = intervaloGain
                RDia += tabela[i][8]
                cont = False
                if opqtdop == 1:
                    qtdOp[i] = 1
                    opqtdop = 0
                alvo = True
                sr = True
            if CV == 'V' and cont == True and ((int(tabela[i][3]) >= GainLoss[-1][3]) or (int(tabela[i][4]) >= GainLoss[-1][3])) and not(HoraFim == proxhora): # Caso Max >= Loss ou Min >= Loss
                tabela[i][7] = 'V'
                tabela[i][8] = -intervaloLoss
                RDia += tabela[i][8]
                cont = False
                if opqtdop == 1:
                    qtdOp[i] = 1
                    opqtdop = 0
                alvo = True
                sr = True
            if CV == 'C' and cont == True and ((int(tabela[i][3]) <= GainLoss[-1][3]) or (int(tabela[i][4]) <= GainLoss[-1][3])) and not(HoraFim == proxhora): # Caso Max <= Loss ou Min <= Loss 
                tabela[i][7] = 'C'
                tabela[i][8] = -intervaloLoss
                RDia += tabela[i][8]
                cont = False
                if opqtdop == 1:
                    qtdOp[i] = 1
                    opqtdop = 0
                alvo = True
                sr = True
            # caso o elemento anterior da tabela seja verdadeiro e o elemento atual seja falso
            if tabela[i-1][6] == 'Verdadeiro' and tabela[i][6] == 'Falso' and not(HoraFim == proxhora):
                tabela[i+1][7] = 'V'
                CV = 'V'
                if dia and not(alvo):
                    tabela[i+1][8] = int(tabela[i+1][2]) - GainLoss[-1][1]
                    RDia += tabela[i+1][8]

                if opqtdop == 1:
                    qtdOp[i+1] = 2
                    opqtdop = 1
                else:
                    qtdOp[i+1] = 1
                    opqtdop = 1

                listaGainLoss.append(i+2+primeiradata)
                listaGainLoss.append(int(tabela[i+1][2]))
                listaGainLoss.append(int(tabela[i+1][2])-intervaloGain)
                listaGainLoss.append(int(tabela[i+1][2])+intervaloLoss)
                GainLoss.append(listaGainLoss)
                listaGainLoss = []
                cont = True
                dia = True
                sr = False

            # Oposto ao caso acima
            if tabela[i-1][6] == 'Falso' and tabela[i][6] == 'Verdadeiro' and not(HoraFim == proxhora):
                tabela[i+1][7] = 'C'
                CV = 'C'
                if dia and not(alvo):
                    tabela[i+1][8] = GainLoss[-1][1] - int(tabela[i+1][2])
                    RDia += tabela[i+1][8]

                if opqtdop == 1:
                    qtdOp[i+1] = 2
                    opqtdop = 1
                else:
                    qtdOp[i+1] = 1
                    opqtdop = 1
                    
                listaGainLoss.append(i+2+primeiradata) # Id para inserir no banco
                listaGainLoss.append(int(tabela[i+1][2])) # preço atual
                listaGainLoss.append(int(tabela[i+1][2])+intervaloGain) # Gain
                listaGainLoss.append(int(tabela[i+1][2])-intervaloLoss) # Loss
                GainLoss.append(listaGainLoss) # Adiciona a uma lista
                listaGainLoss = [] # Zera listaGainLoss, pelo simples motivo de que eu precisava de uma lista dentro de outra lista. Caso essa lista não seja limpa, GainLoss será apenas uma lista dentro de uma lista gigante
                cont = True
                dia = True
                alvo = False
                sr = False
        # Se chegar ao fim do dia, definir como Vendido
        if hora == HoraFim:
            if not(sr) and CV == 'V':
                tabela[i][8] = GainLoss[-1][1] - int(tabela[i][2])
                RDia += tabela[i][8]

            if not(sr) and CV == 'C':
                tabela[i][8] = int(tabela[i][2]) - GainLoss[-1][1]
                RDia += tabela[i][8]

            tabela[i][7] = 'V'

            tabela[i][9] = RDia
            contMes += tabela[i][9]
            CV = ''
            RDia = 0
            dia = False
            qtdOp[i] = opqtdop
            if qtdOp[i] == 0:
                tabela[i][7] = ''
            opqtdop = 0
        if MesTotal:
            if RMes[i] > RMes[i-1]:
                tabela[i][10] = contMes
                contMes = 0




    # Adiciona tudo para a tabela
    for i in range(Media,len(tabela)):
        if tabela[i][7] == '':
            vComando_sql = "UPDATE cruza_medias SET CV = null WHERE id = "+str(i+1)
        else:
            vComando_sql = "UPDATE cruza_medias SET CV = '"+tabela[i][7]+"' WHERE id = "+str(i+1+primeiradata)
        vCursor.execute(vComando_sql)

    for i in range(Media,len(tabela)):
        if tabela[i][8] == '':
            vComando_sql = "UPDATE cruza_medias SET Resultado = null WHERE id = "+str(i+1)
        else:
            vComando_sql = "UPDATE cruza_medias SET Resultado = '"+str(tabela[i][8])+"' WHERE id = "+str(i+1+primeiradata)
        vCursor.execute(vComando_sql)

    for i in range(Media,len(tabela)):
        if tabela[i][9] == 0:
            vComando_sql = "UPDATE cruza_medias SET RDia = null WHERE id = "+str(i+1)
        else:
            vComando_sql = "UPDATE cruza_medias SET RDia = '"+str(tabela[i][9])+"' WHERE id = "+str(i+1+primeiradata)
        vCursor.execute(vComando_sql)

    for i in range(Media,len(tabela)):
        if qtdOp[i] == 0:
            vComando_sql = "UPDATE cruza_medias SET QtdOp = null WHERE id = "+str(i+1)
        else:
            vComando_sql = "UPDATE cruza_medias SET QtdOp = '"+str(qtdOp[i])+"' WHERE id = "+str(i+1+primeiradata)
        vCursor.execute(vComando_sql)
    
    for i in range(Media,len(tabela)):
        if MesTotal:
            if tabela[i][10] == 0:
                vComando_sql = "UPDATE cruza_medias SET RMes = null WHERE id = "+str(i+1)
            else:
                vComando_sql = "UPDATE cruza_medias SET RMes = '"+str(tabela[i][10])+"' WHERE id = "+str(i+primeiradata)
        vCursor.execute(vComando_sql)
            
    
    if not(MesTotal):
        # Preciso achar o ultimo dia e a ultima hora.
        for i in range((Media+1), len(tabela)):
            hora = tabela[i][1].split(':')
            hora = int(hora[0])*60 + int(hora[1])
            if hora == HoraFim:
                idf = i
        vComando_sql = "UPDATE cruza_medias SET RMes = '"+str(contMes)+"' WHERE id = "+str(idf+1)
        vCursor.execute(vComando_sql)


    for i in range(0,len(GainLoss)):
        vComando_sql = "UPDATE cruza_medias SET Posicao = '"+str(GainLoss[i][1])+"' WHERE id = "+str(GainLoss[i][0])
        vCursor.execute(vComando_sql)

    for i in range(0,len(GainLoss)):
        vComando_sql = "UPDATE cruza_medias SET Gain = '"+str(GainLoss[i][2])+"' WHERE id = "+str(GainLoss[i][0])
        vCursor.execute(vComando_sql)

    for i in range(0,len(GainLoss)):
        vComando_sql = "UPDATE cruza_medias SET Loss = '"+str(GainLoss[i][3])+"' WHERE id = "+str(GainLoss[i][0])
        vCursor.execute(vComando_sql)

    vConexao.commit()
    vConexao.close()