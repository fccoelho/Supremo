"""
Gera visualizações georeferenciadas em kml
"""
import xml.dom.minidom
import sys



class KmlDoc:
    def __init__(file_name):
        """
        Constroi un documento KML 
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
