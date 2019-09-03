# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 09:08:56 2019

@author: Maël Akouz
"""

from Database import*

#Import of the needed documents under a usable format :
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Resultats/Civil Aviation Capacities/Classification.txt')
Results = txt.resultbase()
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Resultats/Informations.json')
Infos = txt.infobase()
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Resultats/Category Statistics/Airports.txt')
Limit = txt.airportsCatbase()
txt = ExtractText('C:/Users/Maël Akouz/Desktop/OACI/CAEM/Resultats/Stabilité Index/Stability_Index.txt')
Stab = txt.stabbase()

#Charts describing the evolution of the size of given Categories :
Category = ['Very Low','Very High']
for cat in Category :
    Results.printCat(cat)

#Charts describing the extend of each Category for a given years :
Year = [2003,2008,2013,2018]
for year in Year :
    Results.printStats(year)

#Charts describing the bounds of each airport category :
Category = ['Small','Average','Big']
for cat in Category :
    Limit.printClassAirports(cat)

#Charts giving every useful information about a Country :
Infos.printCountry(Results,'Canada')

#Charts describing the extend of each Stability Category since a given years :
Year = [0,1,2]
for year in Year :
    Stab.printStab(year)
