
import mysql.connector

# Cria conexão com banco MySQL
vConexao = mysql.connector.connect(user='root', password='sysdba',host='127.0.0.1',database='db_indicadores')
vCursor = vConexao.cursor()

# Apaga dados da coluna Media da tabela
vComando_sql = 'update tb_WIN5min set MediaS = null'
vCursor.execute(vComando_sql)

indice = input("Abe - Abertura\nMax - Maxima\nMin - Minina\nFec - Fechamento\nDigite uma das opções: ")

mediaS = int(input("intervalo das médias simples: "))

# Conta quantas linhas tem e faz a conversão para inteiro
vComando_sql = "SELECT COUNT(*) FROM tb_WIN5min"
vCursor.execute(vComando_sql)
vResultado_sql = vCursor.fetchall()
for vLinha in vResultado_sql:
    count = int(vLinha[0])

# Faz operação SQL para colocar no banco
i = 1
for valor in range(1,count,mediaS): # de 1 até "count" pulando de "mediaS" em "mediaS"
    vComando_sql = "SET @media = (SELECT SUM("+indice+")/"+str(mediaS)+" FROM tb_WIN5min WHERE id < "+str(valor+mediaS)+" and id >= "+str(valor)+");" # Cria uma variável chamada @media
    vCursor.execute(vComando_sql)
    vComando_sql = "UPDATE tb_WIN5min SET MediaS = @media WHERE id = "+str(i) # Joga @media dentro desse UPDATE e atualiza o banco
    vCursor.execute(vComando_sql)
    i=i+1   

vConexao.commit()
vConexao.close()