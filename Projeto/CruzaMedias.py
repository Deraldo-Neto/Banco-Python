# Calcula os trades conforme a estratégia Cruzamento de Médias

# Cria conexão com banco MySQL
import mysql.connector
from datetime import datetime
import time

vConexao = mysql.connector.connect(user='root', password='sysdba',
                                   host='127.0.0.1',
                                   database='db_indicadores')
vCursor = vConexao.cursor()

# Variáveis utilizadas no programa
# Dados inseridos pelo usuário
# Dados entrada
print('DADOS DE ENTRADA')
vDataini = '2019.01.01'
vDatafim = '2019.01.03'
vMedia1 = 2
vDado1_user = 'Abe'
vMedia1_tp = 'S'
vMedia2 = 5
vDado2_user = 'Fec'
vMedia2_tp = 'E'

# Variáveis utilizadas no cálculo linha a linha
vId = 0
vId1 = 0
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
vK = 0
vRes_media = 0

def MediaSimples():
    global vDado, vId_ini, vId_fim, vRes_media
    vComando_sql = 'SELECT avg(' + vDado + ')from db_indicadores.cruza_medias where id>= ' + vId_ini + \
                   ' and id <= ' + vId_fim
    vCursor.execute(vComando_sql)
    vResultado_sql = vCursor.fetchone()
    vRes_media = str((vResultado_sql[0]))


# Inicio tempo execução
now = datetime.now()
vInicio = time.time()
print('Início', now)

# Apaga dados das colunas médias na tabela cruza_medias
vComando_sql = 'update cruza_medias set Media1 = null, Media2 = null'
vCursor.execute(vComando_sql)

# Pesquisa a planilha cruza_medias
vComando_sql = 'select * from cruza_medias'
vCursor.execute(vComando_sql)

vResultado_sql = vCursor.fetchall()

for vLinha in vResultado_sql:
    vId = (vLinha[0])
    vDia = (vLinha[1])
    vHora = (vLinha[2])
    vDic = {'Abe': (vLinha[3]), 'Max': (vLinha[4]), 'Min': (vLinha[5]), 'Fec': (vLinha[6])}
    vDado1 = str(vDic[vDado1_user])
    vDado2 = vDic[vDado2_user]

    if vId1 == 0:
        vId1 = vId
    # Calcula a primeira Média Simples que será utilizada no caso de Média Exponencial
    if vId == vMedia2:
        # Cálculo Média 1
        vDado = vDado1_user
        vId_ini = str(vId - vMedia1 + 1)
        vId_fim = str(vId)
        MediaSimples()
        vRes_media1 = str(vRes_media)
        # Cálculo Média 2
        vDado = vDado2_user
        vId_ini = str(vId - vMedia2 + 1)
        vId_fim = str(vId)
        MediaSimples()
        vRes_media2 = vRes_media
        # Insere dados na planilha cruza_medias
        #vComando_sql = 'update cruza_medias set Media1 =' + '"' + vRes_media1 + '"' + ', \
        #        Media2=' + '"' + vRes_media2 + '"' + 'where cruza_medias.AnoMesDia =' + '"' + vDia + '"' + 'and \
        #        cruza_medias.Hora =' + '"' + vHora + '"'
        #vCursor.execute(vComando_sql)
        vRes_media1_ant = float(vRes_media1)
        vRes_media2_ant = float(vRes_media2)
    elif int(vId) > int(vMedia2):
        # Neste mmento há diferenciação do cálculo da média conforme o tipo: Simples ou Exponencial
        # Cálculo Média 1
        if vMedia1_tp == 'S':
            vDado = vDado1_user
            vId_ini = str(int(vId) - int(vMedia1) + 1)
            vId_fim = str(vId)
            MediaSimples()
            vRes_media1 = str(vRes_media)
        else:
            # Cálculo média exponencial
            # Cálculo média exponencial EMA = (preço * vK) + (EMA1 * (1 - vK)) onde vK = (2/(vPeriodo + 1))
            vK = (2 / (vMedia1 + 1))
            vRes_media1 = str((vDado1 * vK) + (vRes_media1_ant * (1 - vK)))

        # Cálculo Média 2
        if vMedia2_tp == 'S':
            vDado = vDado2_user
            vId_ini = str(vId - vMedia2 + 1)
            vId_fim = str(vId)
            MediaSimples()
            vRes_media2 = str(vRes_media)
        else:
            # Cálculo média exponencial
            # Cálculo média exponencial EMA = (preço * vK) + (EMA1 * (1 - vK)) onde vK = (2/(vPeriodo + 1))
            vK = (2 / (vMedia2 + 1))
            vRes_media2 = vRes_media
            vRes_media2_ant = float(vRes_media2)
            vRes_media2 = str((int(vDado2) * vK) + (vRes_media2_ant * (1 - vK)))

        
        # Insere dados na planilha cruza_medias
        #vComando_sql = 'update cruza_medias set Media1 =' + '"' + vRes_media1 + '"' + ', \
        #        Media2=' + '"' + vRes_media2 + '"' + 'where Data =' + '"' + vDia + '"' + 'and \
        #        Hora =' + '"' + vHora + '"'
        #vCursor.execute(vComando_sql)
        # Certifica que os dados estão no Database
        vConexao.commit()
        vRes_media1_ant = float(vRes_media1)
        vRes_media2_ant = float(vRes_media2)

vCursor.close()
vConexao.close()
vFim = time.time()
print('O tempo de execução foi:', round(vFim - vInicio, 2), 'segundos.')
