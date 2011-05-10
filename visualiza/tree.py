# -*- coding:utf-8 -*-

import ubigraph
import csv
import time


def tree(f, n):
    u = ubigraph.Ubigraph()
    u.clear()
    nodes = {}
    row= []
    n += 1
    
    s = u.newVertexStyle(color='#0000ff', shape='sphere', size=0.2)
    x = u.newVertex(color='#00ff00', shape='sphere', size=0.2)
    y = u.newVertex(color='#ff0000', shape='sphere', size=0.2)

    nodes[0], nodes[n] = x, y
    
    for i in f:
        row.append(i)
    
    for i, j in zip(row, range(len(row))):
        if i[0] == 'nivel':
            continue
        if i[0] == '-1':
            break
            
        if row[j+1][0] <= i[0]:
            u.newEdge(nodes[n], nodes[int(i[0])-1], width=int(i[3])/10,
                      label=i[1], oriented='true', spline='true')
        else:
            x = u.newVertex(style=s)
            nodes[int(i[0])] = x
            u.newEdge(nodes[int(i[0])-1], x, label=i[1], oriented='true',
                      width=int(i[3])/10, spline='true', strength='100')
    
    time.sleep(3)          
                        

if __name__ == '__main__':
    f = csv.reader(open('T_Assuntos_CEF.csv', 'r'), delimiter=';')
    g = csv.reader(open('T_Assuntos_Uniao.csv', 'r'), delimiter=';')
    h = csv.reader(open('T_Assuntos_INSS.csv', 'r'), delimiter=';')

    tree(f, 4)
    tree(g, 4)
    tree(h, 4)
