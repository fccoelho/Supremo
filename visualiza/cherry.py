# -*- coding:utf-8 -*-
"""Cherry tree - Complex 2003 - Licence: Python
Bosque do Supremo

modulo para visualizar produção do supremo 

TODO:

- Embed the tree into a class with keyword arguments
  such as colors, sizes, depth, fullness, etc...
- Add texture to make it more realistic
- Create a small forest
- Implement dynamic looks like the effect of waves of wind

Modifications:
2003.01.24. - Complex (cx@cx.hu) - First release
"""

from visual import *
from math import *
from random import *

leaves=[]
fruits=[]
tdata = materials.loadTGA('folhas.tga')
solo = materials.texture(data=tdata,
                          interpolate=True)

def random_vector():
    return vector(random(),random(),random())

class fruta:
    def __init__(self, frm,p,a,r):
        f=frame(frame=frm, pos=p)
        cylinder(frame=f, pos=(0,0,0), axis=a, radius=r, color=color.green)
        sphere(frame=f, pos=a, radius=5*r, color=color.red)
        self.frame = f

    
def leaf(frm,p,a):
    na=norm(a)
    ex=cross((0,1,0),na)
    ey=cross(ex,na)
    ex=0.075*ex
    ey=0.045*ey
    points=[(0.0,0.1),(0.2,0.3),(0.4,0.5),(0.8,0.3),(1.0,0.0),(0.8,-0.3),(0.4,-0.5),(0.2,-0.3),(0.0,-0.1)]
    f=frame(frame=frm, pos=p)
    ex=rotate(ex, axis=ey, angle=pi*0.5*(random()-0.1))
    cylinder(frame=f, pos=(0,0,0), axis=1.2*ex, radius=0.025*mag(ey), color=color.green)
    c=convex(frame=f, pos=[(x+0.29)*ex+y*ey for x,y in points], color=color.green)
    return f
    
class Folha:
    """
    Modelo de folha
    """
    def __init__(self, frm, pos, ax):
        na=norm(ax)
        ex=cross((0,1,0),na)
        ey=cross(ex,na)
        ex=0.075*ex
        ey=0.045*ey
        points=[(0.0,0.1),(0.2,0.3),(0.4,0.5),(0.8,0.3),(1.0,0.0),(0.8,-0.3),(0.4,-0.5),(0.2,-0.3),(0.0,-0.1)]
        f=frame(frame=frm, pos=p)
        ex=rotate(ex, axis=ey, angle=pi*0.5*(random()-0.1))
        cylinder(frame=f, pos=(0,0,0), axis=1.2*ex, radius=0.025*mag(ey), color=color.green)
        c=convex(frame=f, pos=[(x+0.29)*ex+y*ey for x,y in points], color=color.green)
        self.frm = f
        
class Ramo:
    """
    Modelo de ramo
    """
    def __init__(self,nome,pos, ax, raio, cor):
        self.nome = nome
        self.pos = pos
        self.eixo = ax
        self.raio = raio
        self.cor = cor
        self.shape = cylinder(frame=self.frm, pos=pos, axis=ax, radius=raio, color=cor, material=materials.wood)
        sphere(frame=self.frm, pos=q, radius=raio, color=cor, material=materials.wood)

class Arvore:
    """"""
    def __init__(self):
        """"""
        self.frm = frame(pos=(0,-0.8,0))
        self.ramos = {}
        self.folhas = []
    def add_ramo(self,nome, pos, ax, raio, cor, ml, mr, e, d):
        """Constroi um ramo """
        q = pos+ax #centro da esfera que termina o ramo
        ramo = cylinder(frame=self.frm, pos=pos, axis=ax, radius=raio, color=cor, material=materials.wood)
        ramo.folhas = []
        sphere(frame=self.frm, pos=q, radius=raio, color=cor, material=materials.wood)
        self.ramos[nome] = ramo
    
    def add_folha(self, ramo):
        """Adiciona uma folha ao ramo de nome ramo"""
        eixo = self.ramos[ramo].axis*0.6
        f = Folha(self.frm, self.ramos[ramo].pos,eixo)
        f.frm.rotate(axis=eixo,)
        self.ramos[ramo].folhas.append[f]
        
def tree(frm,p,a,r,c,ml,mr,e,d):
    q,v=p+a,ml*a*(0.8+0.4*random())
    cylinder(frame=frm, pos=p, axis=a, radius=r, color=c)
    sphere(frame=frm, pos=q, radius=r, color=c)
    if d>0 and (d>1 or randrange(3)>0):
        a1,a2=cross(a,(0,0,1)),cross(a,(1,0,0))
        s=rotate(v,axis=a1,angle=e)
        n=3+(randrange(10)>3)
        if d<2: n=2
        for i in range(n):
            tree(frm, q, rotate(rotate(s,axis=a,angle=2.0*pi/n*i+pi/5.0/d*random()), axis=a,angle=pi/4.0*(random()-0.5)), mr*r, c, ml, mr, e, d-1)
    else:
        b=vector(0,-0.05,0)
        if randrange(3)<1:
            t=0.1*p+0.9*q
            fruits.append(fruit(frm,t,rotate(b,axis=a,angle=pi*(1+random())/8.0),0.0025))
            fruits.append(fruit(frm,t,rotate(b,axis=a,angle=-pi*(1+random())/8.0),0.0025))
        for i in range(3):
            l=leaf(frm,q,0.5*v)
            l.rotate(axis=a,angle=2*pi*i/3.0)
            leaves.append(l)

#scene.visible=0
#fr=frame(pos=(0,-0.8,0))
##base
#cylinder(frame=fr,pos=(0,-0.1,0), axis=(0,0.11,0), color=(0,0.5,0))
#tr=tree(fr,vector(0,0,0), vector(0,0.8,0), 0.075, (0.8,0.4,0.1), 0.6, 0.6, pi/3.0, 5)
#scene.visible=1
#
#f=3
#ai=0
#aim=f*100
#while 1:
#    rate(25)
#    a=(ai-aim/2)*pi/50.0
#    ai+=f
#    if ai>=aim: ai=0
#    for i in range(len(leaves)/20):
#        for l in (leaves,fruits):
#            o=choice(l)
#            o.rotate(axis=o.up, angle=(a-pi)/200.0)

if __name__=="__main__":
    scene.visible=0
    A = Arvore()
    #base
    cylinder(frame=A.frm,pos=(0,-0.1,0), axis=(0,0.11,0), color=(0.8,0.5,0.1), material=solo)
    A.add_ramo('tronco',vector(0,0,0), vector(0,0.8,0), 0.075, (0.8,0.4,0.1), 0.6, 0.6, pi/3.0, 5)
    scene.visible=1
