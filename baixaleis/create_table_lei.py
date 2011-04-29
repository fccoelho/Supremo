# -*- coding:utf-8 -*-

import MySQLdb
import csv

conn = MySQLdb.connect(host='E04324.fgv.br',
                       user='pablo',
                       passwd='pablo',
                       db='leis')

f = csv.reader(open('constituicao.csv','r'),delimiter=',')
cursor = conn.cursor()

sqlstr = '''
DROP TABLE IF EXISTS leis;
'''
cursor.execute(sqlstr)

sqlstr = '''
CREATE TABLE leis(
  id INT,
  ano INT,
  lei_id INT,
  situacao TEXT,
  titulo INT,
  capitulo INT,
  secao INT,
  sub_secao INT,
  artigo INT,
  sub_artigo INT,
  paragrafo INT,
  inciso INT,
  alinea INT,
  texto TEXT,
  PRIMARY KEY (id) );
'''
cursor.execute(sqlstr)

for row in f:
  if row[0] == 'id':
    continue
  
  sqlstr = '''
  INSERT INTO leis
  VALUES (
  '''
  for i in range(len(row)-1):
    if i == 3:
      sqlstr += "'" + row[i] + "'" + ', '
    else:
      sqlstr += row[i] + ', '
  
  sqlstr += "'" + row[i+1] + "'" + ')'
  cursor.execute(sqlstr)  
