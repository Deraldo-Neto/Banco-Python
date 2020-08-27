import mysql.connector

def MediaSimples(i,info,DataInicio,dataAtual,DataFim):

    armazenaLinha = []
    mediaFinal = []
    infodatas = []
    somatoria = 0

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
 
    k = 0
    mediamaior = info[-1][3] # O calculo sempre se inicia na Media2
    for j in range(0,len(infodatas)): # Repete enquanto existir linhas
        somatoria += infodatas[j] # Soma o valor a variável somatória
        if (j+1) >= info[i][3]: # A partir do momendo em que o i for maior que a média escolhida, sempre entra nessa condição
            if j >= (mediamaior-1):
                mediaFinal.append(somatoria/info[i][3]) # Faz a média
            somatoria -= infodatas[k] #tira o primeiro elemento da variável somatória
            k += 1


    # Ponto para se iniciar no banco
    k = 0
    while not((dataAtual[k] >= DataInicio) and (dataAtual[k] <= DataFim)):
        k += 1

    # Executa comandos SQL para salvar na tabela enquanto existir médias.
    for j in range(0,len(mediaFinal)):
        vComando_sql = "UPDATE cruza_medias SET "+info[i][0]+" = "+str(mediaFinal[j])+" WHERE AnoMesDia >= '"+DataInicio.strftime("%Y.%m.%d")+"' AND AnoMesDia <= '"+DataFim.strftime("%Y.%m.%d")+"' AND id = "+str(k+mediamaior+j)
        vCursor.execute(vComando_sql)

    vConexao.commit()
    vConexao.close()
    return mediaFinal