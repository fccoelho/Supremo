# -*- coding:utf-8 -*-

import ubigraph
import csv

u = ubigraph.Ubigraph()
u.clear()

f = csv.reader(open('T_Assuntos_CEF.csv', 'r'), delimiter=';')
nodes = {}

x = u.newVertex(visible='false')
nodes[0] = x

for row in f:
    if row[0] == 'nivel':
        continue
    if row[0] == '-1':
        break
    
    x = u.newVertex(visible='false')
    nodes[int(row[0])] = x
    u.newEdge(x, nodes[int(row[0])-1], label=row[1], width=int(row[3])+1,
              oriented='true')    
