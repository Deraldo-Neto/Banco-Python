import mysql.connector

def MediaExponencial(i,info,DataInicio,dataAtual,DataFim):

    armazenaLinha = []
    infodatas = []
    # Cria conexão com banco MySQL
    vConexao = mysql.connector.connect(user='root', password='sysdba',
                                    host='127.0.0.1',
                                    database='db_indicadores')
    vCursor = vConexao.cursor()

    # Apaga dados da coluna Media da tabela
    vComando_sql = "update cruza_medias set "+info[i][0]+" = null"
    vCursor.execute(vComando_sql)

    # Pega todos os valores da tabela que o usuário escolher
    vComando_sql = "SELECT "+info[i][1]+" FROM cruza_medias"
    vCursor.execute(vComando_sql)
    vResultado_sql = vCursor.fetchall()

    # Armazena os valores da tabela em uma lista
    for vLinha in vResultado_sql:
        armazenaLinha.append(float(vLinha[0]))

    # Filtra as datas
    for j in range(0,len(armazenaLinha)):
        if (dataAtual[j] >= DataInicio) and (dataAtual[j] <= DataFim):
            infodatas.append(armazenaLinha[j])

    K = 2/(info[i][3]+1) # Multiplicador

    EMA = []
    EMA.append(0) # Preciso de um valor 0 no primeiro item da lista para fazer a somatória

    # A Exponencial precisa começar de algum lugar, tomamos como critério a primeira média simples.
    for j in range(0,info[i][3]):
        EMA[0] += infodatas[j] 
    EMA[0] = EMA[0]/info[i][3]

    # Calcula a EMA
    for j in range(0,(len(infodatas)-info[i][3])):
        EMA.append((infodatas[info[i][3]+j] - EMA[j]) * K + EMA[j]) # (Preço(atual) - EMA(anterior))*K + EMA(anterior) joga o calculo para uma lista

    # Ponto para se iniciar no banco
    k = 0
    while not((dataAtual[k] >= DataInicio) and (dataAtual[k] <= DataFim)):
        k += 1

    # Joga na tabela
    for j in range(0,len(EMA)):
        vComando_sql = "UPDATE cruza_medias SET "+info[i][0]+" = "+str(EMA[j])+" WHERE AnoMesDia >= '"+DataInicio.strftime("%Y.%m.%d")+"' AND AnoMesDia <= '"+DataFim.strftime("%Y.%m.%d")+"' AND id = "+str(k+info[i][3]+j)
        vCursor.execute(vComando_sql)

    vConexao.commit()
    vConexao.close()
    return EMA
