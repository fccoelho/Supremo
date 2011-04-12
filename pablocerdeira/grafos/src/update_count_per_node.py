# -*- coding:utf-8 -*-
'''
Script para incluir um indicdor de ordem de relevância
nas relações lei - lei na tabela gr_lei_lei

A tabela encontra-se ordenada:
    1o. por id da coluna lei_id_1
    2o. pela quantidade de relações com a lei_id_2
    
Incluíndo um indicador (lei_count) na relação
podemos filtrar apenas pelas n leis mais relevantes
para cada lei_id_1

O código SQL para a seleção é:

select * from gr_lei_lei
where lei_count <= 10

Onde 10 é o número de relações mais relevantes a retornar

O valor pode ir de 0 a 100 na atual configuração do script.

Autores:
    Pablo Cerdeira
    Flávio Coelho

'''
import MySQLdb

'''
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

cursor2 = conn.cursor()

'''
Limpando o campo lei_count na tabela gr_lei_lei para atualizações
'''
cursor.execute("update gr_lei_lei set lei_count = null;")


'''
Pegando conteúdo da tabela que será atualizada.
'''
cursor.execute("select edge_id, lei_id_1, lei_id_2 from gr_lei_lei;")

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
sqlstr = ""
while i < cursor.rowcount-2:
    ''' 
    Setando variáveis para o resultado do primeiro valor de gr_lei_lei 
    '''
    id, lei_1, lei_2 = cursor.fetchone()
    ''' 
    Na primeira iteração, seta lei_atual para o lei_1.
    Isso será utilizado para saber quando há mudança para a lei seguinte.
    '''
    lei_atual = lei_1
    ''' 
    Obrigatoriamente no primeiro loop lei_antiga (vale 0) != lei_atual 
    '''    
    if lei_atual != lei_antiga:
        '''
        Se len(sqlstr) > 2 então não estamos mais no primeiro loop.
        Portanto, vamos executar todos os scripts sql anteriores de uma única vez.
        '''
        if len(sqlstr) > 2:
            print "Enviando updates para o MySQL da lei_id %s..." % str(lei_atual)
            cursor2.execute(sqlstr)
            print "Concluído o update da lei_id %s" % str(lei_atual)

        ''' 
        Setamos lei_antiga = lei_atual para que na próxima iteração este if == False
        Setamos j = 1 para inserir como valor de lei_count
        '''
        lei_antiga = lei_atual
        j = 1
<<<<<<< HEAD
        # print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        sqlstr = "update gr_lei_lei set count_lei = %s where edge_id = %s"%(str(j),str(id))
        print sqlstr
        '''
        A linha abaixo executa, mas trava o script. 
        A execução fica travada no MySQLdb/cursors.py linha 282.
        282 > self._do_get_result()
        Por alguma razão quando ele executa a query ele fica travado.
        Deve ser algum bug no meu MySQLdb.
        Flávio, você poderia tentar rodar por ai, por favor?
        ''' 
        cursor2.execute(sqlstr)
    else:
=======
        '''
        Cria o script de update da primeira entrada para o lei_id_1 atual
        '''
        sqlstr = "update gr_lei_lei set lei_count = %s where edge_id = %s; "%(str(j),str(id))
        # print sqlstr
        # cursor2.execute(sqlstr)
    elif j <= 100:
        '''
        Este elif é chamado a partir da segunda iteração do loop, quando
        lei_antiga = lei_atual e enquanto o contador interno j < 100.
        Neste caso o 100 é o limitador de quantas relações desejamos
        marcar com o ordenador.
        A função deste limitador é otimizar o script para que ele não 
        coloque marcador de ordem que nunca utilizaremos.
        '''
        '''
        Incrementamos j para usar como marcadores de ordem seguintes.
        '''
>>>>>>> 1aab63485a554e4d4d95b8eb6a8d3599f4eb66c9
        j += 1
        '''
        Adicionando script à string sqlstr, inserindo o valor atual de j.
        '''
        sqlstr = sqlstr + "update gr_lei_lei set lei_count = %s where edge_id = %s; " % (str(j),str(id))
        # print sqlstr
        # cursor2.execute(sqlstr)
    i += 1
    '''
    Incrementamos i para contagem da quantidade de vezes que o loop foi executado.
    '''

'''
Faz um check para a última sqlstr.
Se len(sqlstr) > 2 então ela tem query a ser executada.
'''
if len(sqlstr) > 2:
    print "Enviando updates para o MySQL da lei_id %s..." % str(lei_atual)
    cursor2.execute(sqlstr)
    print "Concluído o update da lei_id %s" % str(lei_atual)
        
'''
Fecha cursor e conexão.
'''
cursor.close()

conn.close()
