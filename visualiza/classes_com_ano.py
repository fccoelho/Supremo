# -*- coding:utf-8 -*-

import ubigraph
import csv
import time
from math import log

u = ubigraph.Ubigraph()
u.clear()

f = csv.reader(open('classes.csv','r'), delimiter=',')

labels = {'AGRAVO DE INSTRUMENTO' : 'AGRAVO DE INSTRUMENTO',
          'RECURSO EXTRAORDINÁRIO' : 'RECURSO EXTRAORDINARIO',
          'HABEAS CORPUS' : 'HABEAS CORPUS',
          'ARGUIÇÃO DE RELEVÂNCIA' : 'ARGUICAO DE RELEVANCIA',
          'RECLAMAÇÃO' : 'RECLAMACAO', 'CARTA ROGATÓRIA' : 'CARTA ROGATORIA',
          'MANDADO DE SEGURANÇA' : 'MANDADO DE SEGURANCA',
          'INTERVENÇÃO FEDERAL' : 'INTERVENCAO FEDERAL',
          'SENTENÇA ESTRANGEIRA' : 'SENTENCA ESTRANGEIRA',
          'PETIÇÃO' : 'PETICAO'
          }

vertexAno = {}
vertexClasse = {}

ano = 1988
x = u.newVertex(color='#ff0000', shape='cube', label=str(ano))
vertexAno[ano] = x

#for i in range(1989,2010):
#    x = u.newVertex(color='#ff0000', shape='cube', label=str(i))
#    vertexAno[i] = x
#    u.newEdge(vertexAno[i-1], x, strength=10,
#              visible='false')

for row in f:
    if row[0] == 'corte':
        continue
    
    if ano != int(row[2]):
        ano += 1
        time.sleep(1)
        x = u.newVertex(color='#ff0000', shape='cube', label=str(ano))
        vertexAno[ano] = x
        u.newEdge(vertexAno[ano-1], x, strength=1, visible='false')
        
        
    if row[1] not in vertexClasse:
        y = u.newVertex(color='#0000ff', shape='sphere', label=labels[row[1]],
                        size=int(row[3])*0.00001)
        vertexClasse[row[1]] = [y, int(row[3])]
        
    u.newEdge(vertexClasse[row[1]][0], vertexAno[ano], strength=int(row[3]),
              spline='true', visible='true')
    classe = vertexClasse[row[1]]
    classe[1] += int(row[3])
    classe[0].set(size=int(classe[1])*0.00001)
