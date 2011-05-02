# -*- coding:utf-8 -*-
"""Law tree - Complex 2011 - Licence: Python
Bosque do Supremo

modulo para visualizar produção do supremo 

Baseado em exemplo cherry.py do site do visual Python
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

class Fruta:
    """
    Cria frutas nos ramos
    """
    def __init__(self, frm,p,a,r):
        f=frame(frame=frm, pos=p)
        cylinder(frame=f, pos=(0,0,0), axis=a, radius=r, color=color.green)
        sphere(frame=f, pos=a, radius=5*r, color=color.red)
        self.frame = f

    
class Folha:
    """
    Modelo de folha
    """
    def __init__(self, frm, pai, eixo):
        na=norm(pai.eixo)#Direção da folha
        ex=cross((0,1,0),na)
        ey=cross(ex,na)
        ex=0.075*ex
        ey=0.045*ey
        pai.folhas.append(self)
        npf = len(pai.folhas)
        ar = 2*pi/npf*(npf+1)#angulo de rotacao da folha
        #print pai.raio,ex,na,ey,mag(ey)
        points=[(0.0,0.1),(0.2,0.3),(0.4,0.5),(0.8,0.3),(1.0,0.0),(0.8,-0.3),(0.4,-0.5),(0.2,-0.3),(0.0,-0.1)]
        f=frame(frame=frm, pos=pai.fim)
        f.rotate(axis=pai.eixo,angle=ar)
        ex=rotate(ex, axis=ey, angle=pi*0.5*(random()-0.1))
        cylinder(frame=f, pos=vector(0,0,0), axis=1.2*ex, radius=0.025*mag(ey), color=color.green)
        c=convex(frame=f, pos=[(x+0.59)*ex+y*ey for x,y in points], color=color.green)#0.29
        self.frm = f
        
class Ramo(object):
    """
    Modelo de ramo
    """
    def __init__(self,nome,pai,frm, cor, ml, mr, e):
        self.pai = pai #ramo pai
        self.nome = nome
        a1,a2 = cross(pai.eixo,(0,0,1)), cross(pai.eixo,(1,0,0))
        self.v = ml*pai.eixo*(0.8+0.4*random())
        s = rotate(self.v,axis=a1,angle=e)
        self.pai.ramos[self.nome]=self
        n = len(pai.ramos)
        self.ramos = {}
        self.pos = pai.fim
        self.frm = frm
        #print n, (2.0*pi/n)*(n-1)+pi/6.0*random()
        self.eixo = rotate(rotate(s,axis=pai.eixo,angle=(2.0*pi/n)*(n-1)+pi/6.0*random()), axis=pai.eixo,angle=pi/4.0*(random()-0.5))
        self.cor = cor
        self.isTronco = False
        self.fim = self.pos+self.eixo
        self.folhas = []
        self.shape = cylinder(frame=self.frm, pos=self.pai.fim, axis=self.eixo, radius=self.raio, color=self.cor, material=materials.wood)
        sphere(frame=self.frm, pos=self.fim, radius=self.raio, color=cor, material=materials.wood)
        

    @property
    def raio(self):
        return .5*0.11*mag(self.eixo)**1.5

class Arvore(object):
    """"""
    _raio = 0
    def __init__(self, altura=0.8, pos=None, cor=(0.7,0.3,0.05)):
        """"""
        self.frm = frame(pos=(0,-0.8,0))
        self.cor = cor
        self.ramos = {}
        self.folhas = []
        if not pos:
            self.pos = vector(0,0,0) #posicao da base do tronco
        else:
            self.pos = pos
        self.eixo = vector(0,altura,0) #vetor representando o eixo do tronco
        self.fim = self.pos+self.eixo
        self._raio = 0.5*0.11*altura**1.5
        self._cria_tronco()

    @property
    def raio(self):
        return self._raio
    @raio.setter
    def raio(self):
        pass
        
    def _cria_tronco(self):
        """
        Cria o Tronco da arvore
        """
        cylinder(frame=self.frm, pos=self.pos, axis=self.eixo, radius=self.raio, color=self.cor, material=materials.wood)
        sphere(frame=self.frm, pos=self.fim, radius=self.raio, color=self.cor, material=materials.wood)
        
    def add_ramo(self,nome,pai,cor, ml, mr, e):
        """Constroi um ramo """
        if nome in self.ramos:
            raise NameError("Já existe um ramo de nome: %s"%nome)
        if pai == 'tronco':
            pai = self
        else:
            pai = self.ramos[pai]
        ramo = Ramo(nome,pai, self.frm, cor, ml, mr, e)
        

    def add_folha(self, ramo):
        """Adiciona uma folha ao ramo de nome ramo"""
        pai = self.ramos[ramo]
        eixo = pai.v*0.5
        f = Folha(self.frm,pai, eixo)
        self.folhas.append(f)
        
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
    #A2 = Arvore(1,vector(2,0,2))
    #base
    cylinder(frame=A.frm,pos=(0,-0.1,0), axis=(0,0.11,0), color=(0.8,0.5,0.1), material=solo)
    A.add_ramo('ramo1','tronco', (0.7,0.3,0.05), 0.6, 0.6, pi/3.0,)
    A.add_ramo('ramo2','tronco', (0.7,0.3,0.05), 0.6, 0.6, pi/3.0,)
    A.add_ramo('ramo3','tronco', (0.7,0.3,0.05), 0.6, 0.6, pi/3.0,)
    [A.add_folha('ramo1') for i in range(15)]
    [A.add_folha('ramo2') for i in range(15)]
    [A.add_folha('ramo3') for i in range(15)]
    
    #f=Folha(A.frm,(0,-0.1,0),(0,0.11,0))

    scene.visible=1
