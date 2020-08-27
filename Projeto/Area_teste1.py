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
vMedia1 = 7
vDado1_user = 'Abe'
vMedia1_tp = 'S'
vMedia2 = 3
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
vMedia = 0

# Inicio tempo execução
vInicio = time.time()
print('Começou o jogo!', vInicio)

# Apaga dados das colunas médias na tabela cruza_medias
vComando_sql = 'update cruza_medias set Media1 = null, Media2 = null'
vCursor.execute(vComando_sql)

# Pesquisa a planilha cruza_medias
vComando_sql = 'select * from cruza_medias'
vCursor.execute(vComando_sql)
vResultado_sql = vCursor.fetchall()

for vLinha in vResultado_sql:
    vReg = int(vLinha[0])
    vReg1 = str(vReg-vMedia1)
    vReg2 = str(vReg)
    if vReg >= vMedia1:
        vComando_sql = 'select * from cruza_medias where'+ '"' + vReg1 + '"' + '<= ID <=' + '"' + vReg2 + '"'
        vCursor.execute(vComando_sql)
        vResultado_sql = vCursor.fetchall()
        for vLinha in vResultado_sql:
            vTeste = int(vLinha[3]) + 2.1
            vMedia = vMedia + int(vLinha[3])
            if (vLinha[0]) == vReg:
                vRes_media1 = str(vMedia/vMedia1)
                print(vMedia, vMedia1, vRes_media1)
                vComando_sql = 'update cruza_medias set Media1 =' + '"' + vRes_media1 + '"' + 'where cruza_medias.id =' '"' + vReg2 + '"'
                vCursor.execute(vComando_sql)
                # Certifica que os dados estão no Database
                vConexao.commit()
                vMedia = 0
                vRes_media1 = ""

vCursor.close()
vConexao.close()
vFim = time.time()
print('O tempo de execução foi:', round(vFim-vInicio, 2), 'segundos.')