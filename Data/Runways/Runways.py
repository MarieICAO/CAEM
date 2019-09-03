# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:29:19 2019

@author: Maël Akouz
"""

from Database import*

txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/OAG.json')
Data = txt.database_Global()
print('Number of Years in the Database : ' + str(Data.size()))
n = 0
for hmap in Data.htab.values() :
    n = n + hmap.size()
print('Size of the Database : ' + str(n))
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Country_Codes.txt')
Code = txt.countryCode()
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Runways.txt')
Runways = txt.runways()
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Rwys.json')
Additional = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Bases_de_Donnees/Rwys_Additional.json')
Direction = txt.rwys(Additional)
Runways.fusion(Direction)
Runways.index()
Runways.edit(Code,Data,2018)