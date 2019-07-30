# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:34:03 2019

@author: Maël Akouz
"""

import xlwt
from Database import*

#Import of the needed documents under a usable format :
txt = PrintText(input('The path of the OAG document : ')) #C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/OAG2018.json
Data = HashTab.database(txt)
print('Size of the Database : ' + str(Data.size()))
txt = PrintText(input('The path of the document containing the Country Codes : ')) #C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Country_Codes.txt
Code = HashTab.countryCode(txt)
txt = PrintText(input('The path of the document containing the number of Runways by Airport : ')) #C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Runways.txt
Runways = HashTab.runways(txt)
txt = PrintText(input('The path of the document containing the World Bank Category of Countries : ')) #C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Country_Categories.txt
Income = HashTab.income(txt)

#Creation of the needed databases :
Airlines = Data.airlines(Code)
print('Number of Airlines : ' + str(Airlines.size()))
Airlines = Airlines.nationAL()
print('Number of Countries : ' + str(Airlines.size()))
Flights = Data.flights(Code)
Flights.linePorts(Data)
print('Number of Airports : ' + str(Flights.size()))
Airports = Runways.airport(Flights)
Category = Airports.classement([0.4,0.4,0.2])
print('Number of Airport in each Category : ')
print(Category)

#Categorization and recording of the choosen data in an excel document :
Country = Airports.land2(Airlines,Income,3)
spr = xlwt.Workbook()
Airports.excel(spr,'Airports')
spr.save('Airports.xls')
spr = xlwt.Workbook()
Country.excel(spr,'Country')
spr.save('Country_Class2.xls')