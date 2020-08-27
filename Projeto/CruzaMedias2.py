# Calcula os trades conforme a estratégia Cruzamento de Médias

# Cria conexão com banco MySQL
import mysql.connector
import time

vConexao = mysql.connector.connect(user='root', password='sysdba',
                                   host='127.0.0.1',
                                   database='db_indicadores')
vCursor = vConexao.cursor()

# Variáveis utilizadas no programa
# Dados inseridos pelo usuário
# Dados entrada
print ( 'DADOS DE ENTRADA' )
vDataini = '2019.01.01'
vDatafim = '2019.01.03'
vMedia1 = 2
vDado1_user = 'Abe'
vMedia1_tp = 'S'
vMedia2 = 5
vDado2_user = 'Abe'
vMedia2_tp = 'E'

# Variáveis utilizadas no cálculo linha a linha
vDia = str
vHora = str
vAbe = float
vCount = 0
vSoma1 = 0
vSoma2 = 0
vLista_media1 = [0]
vLista_media2 = [0]
vRes_media1 = float
vRes_media2 = float
vVariavel1 = float
vVariavel2 = float

# Inicio tempo execução
vInicio = time.time()

# Apaga dados das colunas médias na tabela cruza_medias
vComando_sql = 'update cruza_medias set Media1 = null, Media2 = null'
vCursor.execute(vComando_sql)

# Pesquisa a planilha cruza_medias
vComando_sql = 'select * from cruza_medias'
vCursor.execute(vComando_sql)

vResultado_sql = vCursor.fetchall()

for vLinha in vResultado_sql:
    vDia = (vLinha[1])
    vHora = (vLinha[2])
    vDic = {'Abe': (vLinha[3]), 'Max': (vLinha[4]), 'Min': (vLinha[5]), 'Fec': (vLinha[6])}
    vDado1 = vDic[vDado1_user]
    vDado2 = vDic[vDado2_user]

    if vCount < vMedia2:  # Alimenta a List com igual aos períodos definidos
        vLista_media2.append(vDado2)
        if vCount > vMedia2 - vMedia1 -1:
            vLista_media1.append(vDado1)
        if vCount == 0:
            vLista_media1.__delitem__ (0)
            vLista_media2.__delitem__ (0)
        vCount = vCount + 1
    elif vCount == vMedia2:  # Deslocamento de 1 linha - Calcula a primeira média
        for x in vLista_media1:
            vSoma1 = vSoma1 + x
        for x in vLista_media2:
            vSoma2 = vSoma2 + x
        vRes_media1 = str(vSoma1 / vMedia1)
        vRes_media2 = str(vSoma2 / vMedia2)
        vCount = vCount + 1
        vComando_sql = 'update cruza_medias set Media1 =' + '"' + vRes_media1 + '"' + ', \
        Media2=' + '"' + vRes_media2 + '"' + 'where cruza_medias.AnoMesDia =' + '"' + vDia + '"' + 'and \
        cruza_medias.Hora =' + '"' + vHora + '"'
        vCursor.execute ( vComando_sql )
        # Certifica que os dados estão no Database
        vConexao.commit()
        vSoma1 = 0
        vSoma2 = 0
    else:  # Neste mmento há diferenciação do cálculo da média conforme o tipo: Simples ou Exponencial
        vLista_media1.append(vDado1)
        vLista_media2.append(vDado2)
        vLista_media1.__delitem__(0)
        vLista_media2.__delitem__(0)
        if vMedia1_tp == 'S':
            for x in vLista_media1:
                vSoma1 = vSoma1 + x
            vRes_media1 = str(vSoma1 / vMedia1)
        # Cálculo média exponencial EMA = (preço * vK) + (EMA1 * (1 - vK)) onde vK = (2/(vPeriodo + 1))
        elif vMedia1_tp == 'E':
            vVariavel1 = 2/(vMedia1 + 1)
            vRes_media1 = str((vLista_media1[vMedia1-2] * vVariavel1) + (float(vRes_media1) * (1 - vVariavel1)))
     # Importante lembrar que a contagem da lista começa no zero, por isto subtrair 2 para alcançar o preço anterior

        if vMedia2_tp == 'S':
            for x in vLista_media2:
                vSoma2 = vSoma2 + x
            vRes_media2 = str(vSoma2/vMedia2)
        # Cálculo média exponencial EMA = (preço * vK) + (EMA1 * (1 - vK)) onde vK = (2/(vPeriodo + 1))
        elif vMedia2_tp == 'E':
            vVariavel2 = 2 / (vMedia2 + 1)
            vRes_media2 = str((vLista_media2[vMedia2-2] * vVariavel2) + (float(vRes_media2) * (1 - vVariavel2)))

        # Insere dados na planilha cruza_medias
        vComando_sql = 'update cruza_medias set Media1 =' + '"' + vRes_media1 + '"' + ', \
                Media2=' + '"' + vRes_media2 + '"' + 'where cruza_medias.AnoMesDia =' + '"' + vDia + '"' + 'and \
                cruza_medias.Hora =' + '"' + vHora + '"'
        vCursor.execute(vComando_sql)
        # Certifica que os dados estão no Database
        vConexao.commit()
        vSoma1 = 0
        vSoma2 = 0

vCursor.close()
vConexao.close()
vFim = time.time()
print('O tempo de execução foi:', round(vFim-vInicio, 2), 'segundos.')