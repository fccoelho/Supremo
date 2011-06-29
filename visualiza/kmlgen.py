# -*- coding:utf-8 -*-
"""
Gera visualizações georeferenciadas em kml
@Autor: Flávio
"""
import xml.dom.minidom
from xml.dom.ext import PrettyPrint
from matplotlib.colors import rgb2hex
from matplotlib import cm
from matplotlib.colors import normalize
from numpy import array

import sys
import copy

class EstadosAnimados(object):
    """
    Cria animação em KML de dados por UF
    """
    def __init__(self, kmlfile, extrude=1):
        self.extrude = extrude
        self.fname = kmlfile
        self.kmlDoc = xml.dom.minidom.parse(kmlfile)
        self.folder = self.kmlDoc.getElementsByTagName("Folder")[0]
        ufElems = self.kmlDoc.getElementsByTagName("Placemark")
        self.pmdict = {}
        for e in ufElems:
            nel = e.getElementsByTagName("name")[0]
            name = self._get_text(nel.childNodes)
            self.pmdict[name] = e
    
    def _get_text(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    def add_data(self, data):
        """
        Adiciona serie temporal para UFs [(UF,tempo,valor),...]
        """
        vals = array([i[2] for i in data])
        norm = normalize(vals.min(), vals.max()) 
        for i, d in enumerate(data):
            print i
            pm = self.pmdict[d[0]]
            #clone placemark to receive new data
            pm_newtime = pm.cloneNode(1)
            # Renaming placemark
            on = pm_newtime.getElementsByTagName('name')[0]
            nn = self.kmlDoc.createElement('name')
            nn.appendChild(self.kmlDoc.createTextNode(d[0]+'-'+str(d[1])))
            pm_newtime.replaceChild(nn, on)
            nl = pm_newtime.childNodes
            #extrude polygon
            pol = pm_newtime.getElementsByTagName('Polygon')[0]
            alt = self.kmlDoc.createElement('altitudeMode')
            alt.appendChild(self.kmlDoc.createTextNode('relativeToGround'))
            ex = self.kmlDoc.createElement('extrude')
            ex.appendChild(self.kmlDoc.createTextNode('1'))
            ts = self.kmlDoc.createElement('tessellate')
            ts.appendChild(self.kmlDoc.createTextNode('1'))
            pol.appendChild(alt)
            pol.appendChild(ex)
            pol.appendChild(ts)
            lr = pm_newtime.getElementsByTagName('LinearRing')[0]
            nlr = self.extrude_polygon(lr, d[2])
            ob = pm_newtime.getElementsByTagName('outerBoundaryIs')[0]
#            ob.replaceChild(nlr, lr)
            ob.removeChild(lr)
            ob.appendChild(nlr)
            #set polygon style
            col = rgb2hex(cm.Oranges(norm(d[2]))[:3])+'ff'
            st = pm_newtime.getElementsByTagName('Style')[0] #style
            nst = self.set_polygon_style(st, col)
            pm_newtime.removeChild(st)
            pm_newtime.appendChild(nst)
            
            #add timestamp
            ts = self.kmlDoc.createElement('TimeStamp')
            w = self.kmlDoc.createElement('when')
            w.appendChild(self.kmlDoc.createTextNode(str(d[1])))
            ts.appendChild(w)
            pm_newtime.appendChild(ts)
            self.folder.appendChild(pm_newtime)
        for pm in self.pmdict.itervalues():
            self.folder.removeChild(pm)
    
    def extrude_polygon(self, lr, alt):
        """
        Adiciona a altitude as coordenadas do anel linear.
        """
        c = lr.getElementsByTagName('coordinates')[0]
        nc = self.kmlDoc.createElement('coordinates')
        ctext = self._get_text(c.childNodes)
        nctext = ' '.join([p+','+str(alt*100) for p in ctext.split(' ')])
#        print nctext
        nc.appendChild(self.kmlDoc.createTextNode(nctext))
        alt = self.kmlDoc.createElement('altitudeMode')
        alt.appendChild(self.kmlDoc.createTextNode('relativeToGround'))
#        altoff = self.kmlDoc.createElement('altitudeOffset')
#        altoff.appendChild(self.kmlDoc.createTextNode(str(d[2]*1000)))
        ex = self.kmlDoc.createElement('extrude')
        ex.appendChild(self.kmlDoc.createTextNode('1'))
        ts = self.kmlDoc.createElement('tessellate')
        ts.appendChild(self.kmlDoc.createTextNode('1'))
        lr.replaceChild(nc, c)
        lr.appendChild(alt)
        if self.extrude:
            lr.appendChild(ex)
            lr.appendChild(ts)
#        lr.appendChild(altoff)
        return lr
        
    
    def set_polygon_style(self,style, color):
        st = style
        pst = st.getElementsByTagName('PolyStyle')[0] #polygon style
        pst1 = self.kmlDoc.createElement('PolyStyle')
        pfill = self.kmlDoc.createElement('fill')
        pcol = self.kmlDoc.createElement('color')
        pfill.appendChild(self.kmlDoc.createTextNode('1'))
        pcol.appendChild(self.kmlDoc.createTextNode(color))
        pst1.appendChild(pfill)
        pst1.appendChild(pcol)
        st.replaceChild(pst1, pst)
        return st
        
    def save(self, fname=''):
        """
        saves the new document
        """
        if not fname:
            fname = self.fname.split('.')[0]+'_animation.kml'
        with open(fname, 'w') as f:
            PrettyPrint(self.kmlDoc, stream=f, indent='  ', encoding='utf-8')
#            f.write(self.kmlDoc.toprettyxml(' ', newl = '\n', encoding = 'utf-8'))

class KmlDoc:
    def __init__(file_name):
        """
        Constroi un documento KML com possibilidade de adicionar 
        placemarks ou barras.
        """
        # This constructs the KML document from the CSV file.
        self.kmlDoc = xml.dom.minidom.Document()
        self.file_name = file_name
        kmlElement = self.kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
        kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
        kmlElement = self.kmlDoc.appendChild(kmlElement)
        self.documentElement = self.kmlDoc.createElement('Document')
        self.documentElement = kmlElement.appendChild(self.documentElement)

    def add_placemark(self, listofpm):
        for pr in listofpm:
            placemarkElement = self.createPlacemark(kmlDoc, row, order)
            self.documentElement.appendChild(placemarkElement)

    def save(self):
        """
        salva o documento kml
        """
        with open(self.file_name, 'w') as kmlfile:
            kmlFile.write(self.kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))
        
    def createPlacemark(row, order):
        """
        Cria um elemento <Placemark> para um dicionario de dados
        row: dicionario
        """
        placemarkElement = self.kmlDoc.createElement('Placemark')
        extElement = self.kmlDoc.createElement('ExtendedData')
        placemarkElement.appendChild(extElement)
        #TODO: ajustar isso para dados genericos
        # Loop through the columns and create a <Data> element for every field that has a value.
        for key in order:
            if row[key]:
                dataElement = self.kmlDoc.createElement('Data')
                dataElement.setAttribute('name', key)
                valueElement =self.kmlDoc.createElement('value')
                dataElement.appendChild(valueElement)
                valueText = self.kmlDoc.createTextNode(row[key])
                valueElement.appendChild(valueText)
                extElement.appendChild(dataElement)

        pointElement = self.kmlDoc.createElement('Point')
        placemarkElement.appendChild(pointElement)
        coordinates = geocoding_for_kml.geocode(extractAddress(row))
        coorElement = self.kmlDoc.createElement('coordinates')
        coorElement.appendChild(self.kmlDoc.createTextNode(coordinates))
        pointElement.appendChild(coorElement)
        return placemarkElement
    
    def add_bar(self, listofbars):
        """
        Adiciona as barras ao documento
        """
        for pr in listofbars:
            barElement = self.create_bar(*pr)
            self.documentElement.appendChild(barElement)
    
    def create_bar(self, coords, altura):
        """
        Cria uma barra de certa altura nas coordenadas
        """
