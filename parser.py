import csv
from lxml import etree
import operator
from itertools import groupby

ponctualiteTransilien = etree.Element("ponctualite-transilien")

dictionnary = {}

# gives a map of keys & group
def groupbySortedData(csvData) :
    dictData = {}
    csvGrouped = groupby(csvData, key=operator.itemgetter(0))
    for key , group in csvGrouped :
        dictData[key] = list(group)
    return dictData
    
# extract all info from a row
def extractLigne(train) :
    myDict = {}
    myDict['id'] = train[0]
    myDict['date_depart'] = train[1]
    myDict['service'] = train[2]
    myDict['sigle'] = train[3]
    myDict['nom'] = train[4]
    myDict['ponctualite'] = train[5]
    myDict['satisfaction'] = train[6]
    return myDict
        
# extract mesure info & puting it in racine;
def detailLigne(rootLigne, dataTrain) :
    date = etree.Element("date")
    date.text =  dataTrain['date_depart']

    ponctualite = etree.Element("ponctualite")
    ponctualite.text =  dataTrain['ponctualite']

    satisfaction = etree.Element("satisfaction")
    satisfaction.text =  dataTrain['satisfaction']

    mesure = etree.SubElement(rootLigne, "mesure")

    mesure.append(date)
    mesure.append(ponctualite)
    mesure.append(satisfaction)


# for each group create corresponding mesure

def createDetailGroup(rootLigne,group):
    for train in group :

        detailLigne(rootLigne,extractLigne(train))


def createTrain(infoFirstTrain):
    global ponctualiteTransilien
    mapOneTrain =   extractLigne(infoFirstTrain)
    trainAttributes = {}
    trainAttributes['id'] = mapOneTrain['id']
    trainAttributes['service'] = mapOneTrain['service']
    trainAttributes['sigle'] = mapOneTrain['sigle']
    trainAttributes['nom'] = mapOneTrain['nom']

    return etree.SubElement(ponctualiteTransilien,"ligne",trainAttributes)



with open('ponctualite-mensuelle-transilien.csv', newline='') as csvfile:
    csvReader = csv.reader(csvfile, delimiter = ';')
    sortedData = sorted(csvReader, key=operator.itemgetter(0))
    dictionnary = groupbySortedData(sortedData[1:])


    for key in dictionnary:
        # create Train creates : <ligne id service sigle name /> ==> return ROOT LIGNE !!!!
        ligne = createTrain(dictionnary[key][0])
        createDetailGroup(ligne, dictionnary[key])
    doc = etree.ElementTree(ponctualiteTransilien)
    doc.write('index.xml', xml_declaration = True, pretty_print = True, encoding="utf-8")


    
