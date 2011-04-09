# -*- coding:utf-8 -*-
import MySQLdb

'''
Usando duas conexões com o banco de dados.
A primeira é para o select e a segunda para os updates.
Não sei se é necessário usarmos as duas agora porque
não estamos mais fazendo o select usando server side.

Nota: fazer o teste com apenas uma conexão.

O cursor server side (SSCursor) foi retirado porque 
estava apresentando erros com o update no Mac e no 
Windows, apesar de rodar bem no Linux durante algum 
tempo, até travar.
'''

conn = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )
   
cursor = conn.cursor()

conn2 = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )

cursor2 = conn2.cursor()

'''
Este select pega o conteúdo da tabela que será atualizada.
'''
cursor.execute("select edge_id, lei_id_1, lei_id_2, lei_count from gr_lei_lei")

print "Iniciando fetch"
'''
Variável i:
    Contador de loop geral, para controlar o início e o fim da execução.

Variável j:
    Contador interno do loop. 
    É resetado para 1 toda vez que a lei_id_1 muda.
    É utilizado para indicar a importância de cada relação lei - lei.
    Nota: a tabela está ordenada primeiro por lei_id_1 e depois por
    quantidade de relações lei_id_1 - lei_id_2
'''
i = 0
j = 1
'''
Variável lei_atual:
    Indica qual lei_id_1 está sendo processada no momento.
    Utilizada para comparação com lei_antiga, indicando ter havido
    mudança de grupo de relações (para setar j = 1).

Variável lei_antiga:
    Recebe o valor de lei_atual na primeira iteração de cada grupo formado
    por lei_id_1.
    Serve de variável de controle para identificar a mudança de grupo (quando
    lei_atual != lei_antiga)
'''
lei_atual = lei_antiga = 0

'''
Loop para percorrer todos os resultados da tabela gr_lei_lei
Será executado enquanto a variável i for menor que o total
de itens da tabela - 2.
'''
while i < cursor.rowcount-2:
    ''' 
    Setando variáveis para o resultado do primeiro valor de gr_lei_lei 
    '''
    id, lei_1, lei_2, c = cursor.fetchone()
    ''' 
    Na primeira iteração, seta lei_atual para o lei_1.
    Isso será utilizado para saber quando há mudança para a lei seguinte.
    '''
    lei_atual = lei_1
    if lei_atual != lei_antiga:
        ''' 
        Obrigatoriamente no primeiro loop lei_antiga (vale 0) != lei_atual 
        '''
        lei_antiga = lei_atual
        j = 1
        ''' 
        Setamos lei_antiga = lei_atual para que na próxima iteração este if == False
        Setamos j = 1 para inserir como valor de lei_count
        '''
        # print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        '''
        Faz o update da primeira entrada para o lei_id_1 atual
        '''
        sqlstr = "update gr_lei_lei set lei_count = %s where edge_id = %s"%(str(j),str(id))
        print sqlstr
        cursor2.execute(sqlstr)
    elif j <= 100:
        '''
        Este elif é chamado a partir da segunda iteração do loop, quando
        lei_antiga = lei_atual e enquanto o contador interno j < 100.
        Neste caso o 100 é o limitador de quantas relações desejamos
        marcar com o ordenador.
        A função deste limitador é otimizar o script para que ele não 
        coloque marcador de ordem que nunca utilizaremos.
        '''
        j += 1
        '''
        Incrementamos j para controle usar como marcadores de ordem seguintes.
        '''
        # print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        '''
        Fazendo o update da tabela, inserindo o valor atual de j.
        '''
        sqlstr = "update gr_lei_lei set lei_count = %s where edge_id = %s"% (str(j),str(id))
        print sqlstr
        cursor2.execute(sqlstr)
    else:
        '''
        Válvula de escape do loop quando lei_antiga ainda igual a lei_atual e
        j > 100.
        Parmanecerá entrando neste bloco até lei_atual != lei_antiga.
        O incremento de j aqui é desnecessário, utilizado apenas para controle
        da execução durante a depuração.
        '''
        j += 1
    i += 1
    '''
    Incrementamos i para contagem da quantidade de vezes que o loop foi executado.
    '''
'''
Fecha cursor e conexão.
'''
cursor.close()

conn.close()
