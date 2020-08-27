from datetime import datetime
import mysql.connector
import time
import MediaSimples
import MediaExponencial
import GainLoss
opcoes = []
idmein = []
medias = []
tabela = []
dataAtual = []
MesTotal = False
now = datetime.now()
vInicio = time.time()
print('Início', now)

# Cria conexão com banco MySQL
vConexao = mysql.connector.connect(user='root', password='sysdba',
                                host='127.0.0.1',
                                database='db_indicadores')
vCursor = vConexao.cursor()

# Pega todos os valores da tabela
vComando_sql = "SELECT AnoMesDia,Hora,Abe,Max,Min,Fec FROM cruza_medias"
vCursor.execute(vComando_sql)
vResultado_sql = vCursor.fetchall()
vConexao.close()

#DataInicio = input("Data de inicio (AAAA.MM.DD): ")
DataInicio = '2019.01.02'
MesInicio = DataInicio.split('.')
MesInicio = int(MesInicio[1])
DataInicio = datetime.strptime(DataInicio, "%Y.%m.%d").date()

#DataFim = input("Data de fim (AAAA.MM.DD): ")
DataFim = '2019.01.06'
MesFim = DataFim.split('.')
MesFim = int(MesFim[1])
DataFim = datetime.strptime(DataFim, "%Y.%m.%d").date()

if MesFim > MesInicio:
    MesTotal = True
# Transforma as tuplas em listas e filtra com as datas
for i in range(0,len(vResultado_sql)):
    dataAtual.append(vResultado_sql[i][0])
    dataAtual[i] = datetime.strptime(dataAtual[i], "%Y.%m.%d").date()
    if (dataAtual[i] >= DataInicio) and (dataAtual[i] <= DataFim):
        tabela.append(list(vResultado_sql[i]))

# Encontra a Primeira data
primeiradata = 0
while not(dataAtual[primeiradata] >= DataInicio):
    primeiradata += 1

#HoraInicio = input("Horario de inicio (xx:xx): ")
HoraInicio = '9:00'
HoraInicio = HoraInicio.split(':')
HoraInicio = int(HoraInicio[0])*60 + int(HoraInicio[1])

#HoraFim = input("Horario de fim (xx:xx): ")
HoraFim = '17:15'
HoraFim = HoraFim.split(':')
HoraFim = int(HoraFim[0])*60 + int(HoraFim[1])

#intervaloGain = int(input("Defina o Gain: "))
intervaloGain = 400

#intervaloLoss = int(input("Defina o Loss: "))
intervaloLoss = 200


#for i in range(1,3):
#    opcoes.append("Media" + str(i))
#    opcoes.append(input(("Abe - Abertura\nMax - Maxima\nMin - Minina\nFec - Fechamento\nDigite uma das opções: ")).lower().capitalize())
#    opcoes.append(input("S - Simples\nE - Exponencial\nDigite uma das opções: "))
#    opcoes.append(int(input("Digite o intervalo: ")))
#    idmein.append(opcoes)
#    opcoes = []
opcoes.append("Media1")
opcoes.append("Fec")
opcoes.append("S")
opcoes.append(9)
idmein.append(opcoes)
opcoes = []
opcoes.append("Media2")
opcoes.append("Fec")
opcoes.append("E")
opcoes.append(21)
idmein.append(opcoes)
opcoes = []

for i in range(0,2):
    if idmein[i][2] == 'S' or idmein[i][2] == 's':
        medias.append(MediaSimples.MediaSimples(i,idmein,DataInicio,dataAtual,DataFim)) # Calcula as médias simples
    if idmein[i][2] == 'E' or idmein[i][2] == 'e':
        medias.append(MediaExponencial.MediaExponencial(i,idmein,DataInicio,dataAtual,DataFim)) # Calcula as médias exponenciais

for i in range(0,len(medias[0])):
    if medias[0][i] > medias[1][i]: # Verifica se a Media1 é maior que a Media2
        tabela[i+(idmein[-1][3]-1)] = tabela[i+(idmein[-1][3]-1)] + ["Verdadeiro"] # Adiciona Verdadeiro para a tabela
    else:
        tabela[i+(idmein[-1][3]-1)] = tabela[i+(idmein[-1][3]-1)] + ["Falso"] # Adiciona Falso para a tabela

# Os '' serão substituidos por V ou C, de vendido ou comprado
for i in range(0,len(tabela)): 
    tabela[i].append('')
    tabela[i].append('')
    tabela[i].append(0)
    tabela[i].append(0)

GainLoss.GainLoss(idmein[-1][3],tabela,HoraInicio,HoraFim,intervaloGain,intervaloLoss,primeiradata,'',MesTotal) # Faz os ganhos e as perdas

vFim = time.time()
print('O tempo de execução foi:', round(vFim - vInicio, 2), 'segundos.')
