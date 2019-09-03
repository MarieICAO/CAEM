# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:52:48 2019

@author: Maël Akouz
"""

import xlwt
from Database import*

#Import of the needed documents under a usable format :
txt = ExtractText(input('The path of the complete OAG document : ')) #'CAEM/Data/OAG Database/OAG.json'
Data = txt.database_Global()
print('Number of Years in the Database : ' + str(Data.size()))
n = 0
for hmap in Data.htab.values() :
    n = n + hmap.size()
print('Size of the Database : ' + str(n))
txt = ExtractText(input('The path of the document containing the Country Codes : ')) #'CAEM/Data/Country_Codes.txt'
Code = txt.countryCode()
txt = ExtractText(input('The path of the document containing the Runway information by Airport : ')) #'CAEM/Data/Runways/Runways.json'
Runways = txt.rwys_database()
txt = ExtractText(input('The path of the document containing the World Bank Category of Countries : ')) #'CAEM/Data/World_Bank_Income_Classification.txt'
Income = txt.income()

#Creation of the needed databases :
ClassFinal = CatTab('Country Code',['Country Code','Country Name','List of Yearly Classifications'])
InfoFinal = CatTab('Year','Needed Information for the Classfication')
CatLimit = CatTab('Year',['Year','Maximal Size of Small Airports','Maximal Size of Average Airports','Maximal Size of Big Airports'])
n=0
for year in Data.htab.keys() :
    if year<2019 :
        data = Data.database(year)
        Class,Info,limit = data.classification(Code,Runways,Income,year)
        InfoFinal.htab[year] = Info
        CatLimit.htab[year] = limit
        for key,line in Class.htab.items() :
            if key in ClassFinal.htab :
                ClassFinal.htab[key].append(line[3])
            else :
                ClassFinal.htab[key] = line[:2] + ['' for k in range(n)]
                ClassFinal.htab[key].append(line[3])
        n=n+1
    else :
        print("The World Bank Income Classifcation of 2019 isn't disponible yet.")
InfoFinal.edit()

#Registration under Excel format :
spr1 = xlwt.Workbook()
ClassFinal.excel(spr1,'Final Classification')
CatLimit.excel(spr1,'Sizes of Airports Categories')
spr1.save('Classification.xls')
spr2 = xlwt.Workbook()
for year in InfoFinal.htab.keys() :
    InfoFinal.htab[year].excel(spr2,str(year))
spr2.save('Informations.xls')
