# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:03:04 2019

@author: Maël Akouz
"""

import json
from collections import Counter
import matplotlib.pyplot as plt

class Runways :
    "Provide a collection of functions to exploit the Runways database."
    
    def rwys(self,Additional) :
        "Provide an HashMap with the caracteristics of the runways of each airports using a JSON input. The 'Additional' argument matches anoter JSON document as a complement."
        Direction = CatTab('ICAO Airport Code',['Runway Identifier','Runway Length'])
        self.data.extend(Additional.data)
        for line in self.data :
            json_dict = json.loads(line)
            code = json_dict['airport_code']
            _id = json_dict['id']
            length = round(json_dict['rwy_length_feet']*0.3048)
            if code in Direction.htab :
                Direction.htab[code].append([_id,length])
            else :
                Direction.htab[code] = [[_id,length]]
        return Direction
    
    def runways(self) :
        "Provide an HashMap with the number of Runways by Airport using a 'txt' input."
        Runways = CatTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways'])
        for line in self.data[1:] :
            l = line.split('\t')
            Runways.htab[l[0]] = l[:6]
            Runways.htab[l[0]].append(int(l[6][0]))
        return Runways
    
    def fusion(self,Direction) :
        "Merge the two previous HashMap to obtain an unique Runways' database."
        self.legend.append('Runway Identifier & Runway Length')
        for line in self.htab.values() :
            if line[1] in Direction.htab :
                rwys = Direction.htab[line[1]]
                line[6] = len(rwys)
                line.append(rwys)
            else :
                if line[6]<2 :
                    line.append('None')
                elif line[1]=='LSZM' :
                    rwys = Direction.htab['LFSB']
                    line[6] = len(rwys)
                    line.append(rwys)
                else :
                    print(line)
    
    def index(self) :
        "Add the value of the Airport Index according the orientation of its Runways."
        self.legend.append('Runway Index')
        for line in self.htab.values() :
            if line[6]<2 :
                line.append(line[6])
            else :
                orient = []
                for rwys in line[7] :
                    pos = int(rwys[0][:2])
                    if pos<18 :
                        orient.append(pos)
                    else :
                        orient.append(pos-18)
                orient = Counter(orient).most_common()
                mx = list(orient[0])
                for pair in orient[1:] :
                    if mx[0]-2<pair[0]<mx[0]+2 :
                        mx[1] = mx[1]+pair[1]
                if mx[1]==line[6] :
                    line.append(line[6])
                else :
                    line.append(mx[1]+0.5)

    def edit(self,Code,Data,year) :
        "Save the database of Runways under a 'json' format, in adding the airport status."
        data = Data.database(year)
        Flights = data.flights(Code)
        lg = self.legend
        with open('Runways.json','w') as rws :
            for key,line in self.htab.items() :
                Htab = {}
                for i in range(len(lg)) :
                    Htab[lg[i]] = str(line[i])
                if key in Flights.htab :
                    Htab['Airport Status'] = 'Served'
                else :
                    Htab['Airport Status'] = 'Unserved'
                json.dump(Htab,rws)
                rws.write('\n')
    
    def rwys_database(self) :
        "Provide an HashMap with the caracteristics of the runways of each airports using the final JSON Runways' database."
        Runways = CatTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways','Runway Index'])
        for line in self.data :
            json_dict = json.loads(line)
            key = json_dict['IATA Airport Code']
            Runways.htab[key] = [key]
            for word in Runways.legend[1:6] :
                Runways.htab[key].append(json_dict[word])
            Runways.htab[key].append(int(json_dict['Number of Runways']))
            Runways.htab[key].append(float(json_dict['Runway Index']))
        return Runways             


class ExtractText(Runways) :
    "Give an overview of a TXT or JSON document or transform it under a CatTab format."
    
    def __init__(self,link) :
        "Provide a list of the document's lines (the one matching with the given link)." 
        with open(link,'r') as txt :
            self.data = txt.readlines()
    
    def printInt(self,n) :
        "Print the n first lines of the document in interpreting them."
        r=0
        if len(self.data)<n :
            n=len(self.data)
        while r<n :
            print(self.data[r])
            r=r+1

    def printRaw(self,n) :
        "Print the n first lines of the document without interpretation."
        r=0
        if len(self.data)<n :
            n=len(self.data)
        while r<n :
            print([self.data[r]])
            r=r+1

    def database_Global(self) :
        "Provide an HashMap with all the informations including in the complete OAG document using an 'json' input."
        Data = CatTab('Year',['Yearly OAG Database'])
        for line in self.data :
            line = line.split(',')
            l = [int(line[1].split(':')[1])]
            for k in range(2,13) :
                while ':' not in line[k] :
                    del line[k]
                l.append(line[k].split(':')[1][1:-1])
            for k in range(13,16) :
                l.append(int(line[k].split(':')[1].split('}')[0]))
            if l[4]=='SHO' :
                l[5:8] = ['FDSK','KING MSWATI III INTL','SWZ']
            elif l[8]=='SHO' :
                l[9:12] = ['FDSK','KING MSWATI III INTL','SWZ']
            if l[0] in Data.htab :
                key = l[1] + l[4] + l[8]
                Data.htab[l[0]].htab[key] = l
            else :
                Data.htab[l[0]] = CatTab('{Airline + From IATA Airport + To IATA Airport} Code',['Year','Airline Code','Airline Name','Airline Country Code','From IATA Airport Code','From ICAO Airport Code','From Airport Name','From Airport Country Code','To IATA Airport Code','To ICAO Airport Code','To Airport Name','To Airport Country Code','Number of Flights by Year','Number of Seat by Flight','Number of Used Planes'])
                key = l[1] + l[4] + l[8]
                Data.htab[l[0]].htab[key] = l
        return Data
    
    def countryCode(self) :
        "Provide an HashMap with the relevant ISO Codes and their meaning using a 'txt' input."
        Code = CatTab('Alpha-3 Code',['Country','Alpha-2 Code','Alpha-3 Code','Numeric code','Continent'])
        for i in range(1,len(self.data)) :
            l = self.data[i].split(',')
            if len(l)==5 :
                line = []
                for j in range(5) :
                    line.append(l[j].split('"')[1])
                Code.htab[line[2]] = line
            else :
                Code.htab[l[2].split('"')[1]] = l[5].split('"')[1]
        for key,line in Code.htab.items() :
            if type(line) is str :
                Code.htab[key] = Code.htab[line]
        return Code
    
    def income(self) :
        "Provide an HashMap with the Country's wealth groups of the World Bank using a 'txt' input."
        Switcher = {'L':('Low Income',1),'LM':('Lower Middle Income',2),'UM':('Upper Middle Income',3),'H':('High Income',4),}
        Income = CatTab('Country Code',['Country Code','Country Name','Yearly World Bank Income Category'])
        year = self.data[0].split('\t')
        del year[:2]
        year[-1] = year[-1].split('\n')[0]
        year = [int(y) for y in year]
        for line in self.data[1:] :
            l = line.split('\t')
            l[-1] = l[-1].split('\n')[0]
            Cat = CatTab('Year',['Year','World Bank Income Category','Category Number'])
            for k in range(len(year)) :
                if len(l[k+2])>0 :
                    Cat.htab[year[k]] = [year[k]]
                    Cat.htab[year[k]].extend(Switcher[l[k+2]])
                else :
                    Cat.htab[year[k]] = None
            Income.htab[l[0]] = [l[0],l[1],Cat]
        return Income
    
    def resultbase(self) :
        "Provide an HashMap with the classification of each country for the number of year in the OAG document."
        leg = self.data[0].split('\t')
        leg[-1] = leg[-1].split('\n')[0]
        del leg[:2]
        Results = CatTab('Country Name',leg)
        for line in self.data[1:] :
            l = line.split('\t')
            l[-1] = l[-1].split('\n')[0]
            for k in range(2,len(l)) :
                if len(l[k])==0 :
                    l[k] = 0
                else :
                    l[k] = ord(l[k])-64
            Results.htab[l[1]] = l[2:]
        return Results
    
    def infobase(self) :
        "Provide an HashMap with every useful information for the classification using an 'json' format."
        Info = CatTab('Year','Needed Information for the Classfication')
        for line in self.data :
            json_dict = json.loads(line)
            key = json_dict.pop('Year')
            if key not in Info.htab :
                Info.htab[key] = CatTab('Country Name',['Number of Flights In & Out','Global Number of Airports','Number of Small Airports','Number of Average Airports','Number of Big Airports','Global Runway National Index','Synthetic Runway Index','Number of National Airlines','World Bank Income Category'])
            del json_dict['Country Code']
            ligne = []
            for word in json_dict.keys() :
                try :
                    int(json_dict[word])
                    ligne.append(int(json_dict[word]))
                except :
                    try :
                        float(json_dict[word])
                        ligne.append(float(json_dict[word]))
                    except :
                        ligne.append(json_dict[word])
            Info.htab[key].htab[ligne[0]] = ligne[1:]
        return Info
    
    def airportsCatbase(self) :
        "Provide an HashMap with the size of each airports category."
        leg = self.data[0].split('\t')
        leg[-1] = leg[-1].split('\n')[0]
        Limit = CatTab('Year',leg)
        for line in self.data[1:] :
            l = line.split('\t')
            l[-1] = l[-1].split('\n')[0]
            Limit.htab[l[0]] = l
        return Limit
    
    def stabbase(self) :
        "Provide an HashMap with the stability category of each world countries."
        leg = self.data[0].split('\t')
        leg[-1] = leg[-1].split('\n')[0]
        del leg[:2]
        Stab = CatTab('Country Name',leg)
        for line in self.data[1:] :
            l = line.split('\t')
            l[-1] = l[-1].split('\n')[0]
            Stab.htab[l[1]] = l[2:]
        return Stab


class OAGTab :
    "Provide a collection of function to exploit an OAG text document."
    
    def __init__(self,clee,liste) :
        "Provide an object with an HashMap, the type of the HashMap's key and the type of data in this HashMap (under the argument 'legend')."
        self.key = clee
        self.legend = liste
        self.htab = {}

    def database(self,year) :
        "Extract an HashMap with all the informations including in the yearly OAG document using the complete OAG database."
        data = self.htab[year].copy()
        del data.legend[0]
        for line in data.htab.values() :
            del line[0]
        return data

    def airlines(self,Code) :
        "Provide an HashMap of the Airlines and their characteristics using the yearly OAG database." 
        Airline = CatTab('Airline Code',['Airline Code','Airline Name','Country Code','Country Name','Number of Air Links'])
        for line in self.htab.values() :
            if line[0] in Airline.htab :
                al = Airline.htab[line[0]]
                al[4] = al[4]+1
            else :
                al = line[:2]
                code = Code.htab[line[2]]
                al.append(code[2])
                al.append(code[0])
                al.append(1)
                Airline.htab[line[0]] = al
        return Airline
    
    def nationAL(self) :
        "Provide an HashMap with the number of Airlines located in each considered Country using the Airlines' database."
        Country = CatTab('Country Code',['Country Code','Country name','Number of Airlines'])
        for line in self.htab.values() :
            if line[2] in Country.htab :
                if line[0] not in Country.htab[line[2]] :
                    Country.htab[line[2]].append(line[0])
            else :
                Country.htab[line[2]] = [line[2],line[3],line[0]]
        for key,line in Country.htab.items() :
            Country.htab[key] = [line[0],line[1],len(line)-2]
        return Country
    
    def flights(self,Code,fill=0.8) :
        "Provide an HashMap of the Airports and their characteristics using the yearly OAG database. The argument 'fill' matches with the average filling of each flight (to give an idea of the number passengers using this airport)."
        Flight = CatTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','Airport Country Code','Airport Country Name','Number of Flight Out','Number of Flight In','Number of Passenger Out','Number of Passenger In'])
        for line in self.htab.values() :
            if line[3] in Flight.htab :
                port = Flight.htab[line[3]]
                port[5]=port[5]+int(line[11])
                port[7]=port[7]+fill*int(line[12])*int(line[11]) 
            else :
                code = Code.htab[line[6]]
                Flight.htab[line[3]] = [line[3],line[4],line[5],code[2],code[0],int(line[11]),0,fill*int(line[11])*int(line[12]),0]
            if line[7] in Flight.htab :
                port = Flight.htab[line[7]]
                port[6]=port[6]+int(line[11])
                port[8]=port[8]+fill*int(line[12])*int(line[11])
            else :
                code = Code.htab[line[10]]
                Flight.htab[line[7]] = [line[7],line[8],line[9],code[2],code[0],0,int(line[11]),0,fill*int(line[11])*int(line[12])]
        return Flight
    
    def linePorts(self,Data) :
        "Add the number of present Airlines in each Airport in the Flights' database."
        Airterminal = OAGTab('IATA Airport Code',['List of Airlines Using this Airport'])
        for line in Data.htab.values() :
            if line[3] in Airterminal.htab :
                if line[0] not in Airterminal.htab[line[3]] :
                    Airterminal.htab[line[3]].append(line[0])
            else :
                Airterminal.htab[line[3]] = [line[0]]
            if line[7] in Airterminal.htab :
                if line[0] not in Airterminal.htab[line[7]] :
                        Airterminal.htab[line[7]].append(line[0])
            else :
                Airterminal.htab[line[7]] = [line[0]]
        self.legend.append('Number of Airlines Using this Airport')
        for key,line in Airterminal.htab.items() :
            self.htab[key].append(len(line))


class GraphCat :
    "Provide a collection of fonctions to exploit the classification."

    def printCat(self,cat) :
        "Create two bar chart showing the number & the percentage of countries in a category through time using the Results base. The 'cat' argument matches the letter of the wanted category."
        Switcher = {'Very Low':1,'Low':2,'Lower Middle':3,'Upper Middle':4,'High':5,'Very High':6}
        plt.figure('Statistics for ' + cat)
        nbCat = Switcher[cat]
        res = [0 for l in self.legend]
        for line in self.htab.values() :
            for k in range(len(line)) :
                if line[k]==nbCat :
                    res[k] = res[k]+1
        x = self.legend
        plt.subplot(1,2,1)
        plt.bar(x,res,width=0.5,color='#5b92e5')
        plt.title('Number of Countries',fontsize=24,pad=22)
        axes = plt.gca()
        n = 0 
        for label in plt.gca().xaxis.get_ticklabels():
            if n%2==0 :
                label.set_size(14)
            else :
                label.set_size(0)
            n = n+1
        axes.xaxis.set_tick_params(length=6,pad=10)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Number of Countries',fontsize=16,labelpad=10)
        plt.subplot(1,2,2)
        res = [r/self.size() for r in res]
        plt.bar(x,res,width=0.5,color='#5b92e5')
        plt.title('Percentage of Countries',fontsize=24,pad=22)
        axes = plt.gca()
        n = 1
        for label in plt.gca().xaxis.get_ticklabels():
            if n%2==0 :
                label.set_size(14)
            else :
                label.set_size(0)
            n = n+1
        axes.xaxis.set_tick_params(length=6,pad=10)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Percentage of Countries',fontsize=16,labelpad=10)
        plt.suptitle(cat,fontsize=36,x=0.5,y=0.97)
        plt.show()
    
    def printStats(self,year) :
        "Create a pie chart showing the extend of each category using the Results base. The 'year' argument matches the wanted year."
        plt.figure('Extend of each Category in ' + str(year),figsize=(10,10))
        res = [0 for k in range(6)]
        for line in self.htab.values() :
            cat = line[year-2003]-1
            res[cat] = res[cat]+1
        plt.pie(res,colors=['#fe0002','#feac02','#fefc0b','#b2f97f','#9dc9fe','#dedede'],labels=['A','B','C','D','E','F'],textprops={'fontsize':14},autopct=lambda x:str(round(x))+' %',startangle=90,counterclock=False)
        plt.title('Statistics of ' + str(year),fontsize=32,pad=22)
        plt.legend(labels=['Very Low','Low','Lower Middle','Upper Middle','High','Very High'],fontsize=14,loc=(-0.05,-0.05))
        plt.show()

    def printStab(self,year) :
        "Create a pie chart showing the extend of each category using the Stab base. The value of the 'year' argument is 0 since 2003, 1 since 2008 and 2 since 2013."
        plt.figure('Extend of each Category in ' + str(2003+year*5),figsize=(11,10))
        Cat = ['Worrying','Unstable Downwards','Structural Effect','Unstable Upwards','Encouraging','Stable','']
        res = {word:0 for word in Cat}
        for line in self.htab.values() :
            res[line[year]] = res[line[year]]+1
        per = [res[word] for word in Cat]
        plt.pie(per,colors=['#fe0002','#feac02','#fefc0b','#b2f97f','#9dc9fe','#dedede','#ffffff'],labels=Cat,textprops={'fontsize':14},autopct=lambda x:str(round(x))+' %',startangle=90)
        plt.title('Evolution since ' + str(2003+year*5),fontsize=32,pad=22)
        plt.legend(labels=Cat,fontsize=14,loc=(0.75,-0.1))
        plt.show()
    
    def printClassAirports(self,cat) :
        "Create a bar charts showing the evolution of Airports Categories through time using the Airports Statistics' base."
        Switcher = {'Small':1,'Average':2,'Big':3}
        plt.figure(cat + ' Airports')
        x = list(self.htab.keys())
        y = []
        for year in x :
            y.append(self.htab[year][Switcher[cat]])
        plt.bar(x,y,width=0.5,color='#5b92e5')
        plt.title('Growth in Size of ' + cat + ' Airports',fontsize=32,pad='32')
        axes = plt.gca()
        axes.xaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Number of Flights',fontsize=16,labelpad=3)
        plt.show()
        
    def printEvolve(self,name) :
        "Create a bar chart showing the category of a country through time using the Results' base. The 'name' argument matches the name of the wanted country."
        res = self.htab[name]
        x = self.legend
        plt.bar(x,res,width=0.5,color='#5b92e5')
        plt.title(name,fontsize=32,pad='32')
        axes = plt.gca()
        axes.xaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.set_ylim(0,6.5)
        axes.yaxis.set_ticklabels(['None','A','B','C','D','E','F'])
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Category',fontsize=16,labelpad=3)
        plt.show()

    def printFlights(self,name) :
        "Create a bar chart showing the number of Flights In & Out for the considered Country through time using the Information base. The 'name' argument matches the name of the wanted Country."
        x = list(self.htab.keys())
        y = [line.htab[name][0] for line in self.htab.values() if name in line.htab]
        y[:0] = [0 for k in range(len(x)-len(y))]
        plt.bar(x,y,width=0.5,color='#5b92e5')
        plt.title('Number of Flights In & Out',fontsize=24,pad=22)
        axes = plt.gca()
        axes.xaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Number of Flights',fontsize=16,labelpad=10)
        plt.show()

    def printAirports(self,name,mx,sameaxis) :
        "Create four bar chart showing the number of Airports in each Category for the considered Country through time using the Information base. The 'name' argument matches the name of the wanted Country, the 'mx' argument the maximal number of airports and the 'sameaxis' argument demand that the axis of the four chart have the same scale."
        x = list(self.htab.keys())
        colour = [None,'#5b92e5','#fe0002','#feac02','#fefc0b']
        legend = [None,'Global Number of Airports','Number of Small Airports','Number of Average Airports','Number of Big Airports']
        for k in range(1,5) :
            plt.subplot(2,2,k)
            y = [line.htab[name][k] for line in self.htab.values() if name in line.htab]
            y[:0] = [0 for k in range(len(x)-len(y))]
            plt.bar(x,y,width=0.5,color=colour[k])
            axes = plt.gca()
            n = 1 
            for label in plt.gca().xaxis.get_ticklabels():
                if n%2==0 :
                    label.set_size(14)
                else :
                    label.set_size(0)
                n = n+1
            axes.xaxis.set_tick_params(length=6,pad=10)
            axes.set_xlabel('Year',fontsize=16,labelpad=16)
            if sameaxis :
                axes.set_ylim(0,mx)
            axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
            axes.set_ylabel(legend[k],fontsize=16,labelpad=10)
        plt.suptitle('Number of Airports',fontsize=36,x=0.5,y=0.97)
        plt.show()
    
    def printRunways(self,name) :
        "Create two bar chart showing the Runways Index in each Category for the considered Country through time using the Information base. The 'name' argument matches the name of the wanted Country."
        x = list(self.htab.keys())
        legend = [None,None,None,None,None,'Global Runway National Index','Synthetic Runway Index']
        for k in range(5,7) :
            plt.subplot(1,2,k-4)
            y = [line.htab[name][k] for line in self.htab.values() if name in line.htab]
            y[:0] = [0 for k in range(len(x)-len(y))]
            plt.bar(x,y,width=0.5,color='#5b92e5')
            axes = plt.gca()
            n = 1 
            for label in plt.gca().xaxis.get_ticklabels():
                if n%2==0 :
                    label.set_size(14)
                else :
                    label.set_size(0)
                n = n+1
            axes.xaxis.set_tick_params(length=6,pad=10)
            axes.set_xlabel('Year',fontsize=16,labelpad=16)
            axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
            axes.set_ylabel(legend[k],fontsize=16,labelpad=10)
        plt.suptitle('Runways Index',fontsize=36,x=0.5,y=0.97)
        plt.show()
    
    def printAirlines(self,name) :
        "Create a bar chart showing the number of Airlines for the considered Country through time using the Information base. The 'name' argument matches the name of the wanted Country."
        x = list(self.htab.keys())
        y = [line.htab[name][7] for line in self.htab.values() if name in line.htab]
        y[:0] = [0 for k in range(len(x)-len(y))]
        plt.bar(x,y,width=0.5,color='#5b92e5')
        plt.title('Number of Airlines',fontsize=24,pad=22)
        axes = plt.gca()
        axes.xaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Number of Airlines',fontsize=16,labelpad=10)
        plt.show()
    
    def printIncome(self,name) :
        "Create a bar chart showing the World Bank Income category of a country through time using the Information base. The 'name' argument matches the name of the wanted country."
        x = list(self.htab.keys())
        Switcher = {'Low Income':1,'Lower Middle Income':2,'Upper Middle Income':3,'High Income':4}
        y = [Switcher[line.htab[name][8]] for line in self.htab.values() if name in line.htab]
        y[:0] = [0 for k in range(len(x)-len(y))]
        plt.bar(x,y,width=0.5,color='#022e51')
        plt.title('World Bank Income Category',fontsize=32,pad='32')
        axes = plt.gca()
        axes.xaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_xlabel('Year',fontsize=16,labelpad=16)
        axes.set_ylim(0,4.5)
        axes.yaxis.set_ticklabels(['None','','Low','','Lower Middle','','Upper Middle','','High'])
        axes.yaxis.set_tick_params(length=6,pad=10,labelsize=14)
        axes.set_ylabel('Income Category',fontsize=16,labelpad=20)
        plt.show()
    
    def printCountry(self,Results,name,sameaxis=True) :
        "Provide a set of charts describing every useful information for the classification of the Country named 'name' using the Information base."
        limit = str(max([line.htab[name][1] for line in self.htab.values() if name in line.htab]))
        limit = (int(limit[0])+1)*pow(10,len(limit)-1)
        plt.figure(name + ' (World Bank Income Classification)')
        self.printIncome(name)
        plt.figure(name + ' (Airlines)')
        self.printAirlines(name)
        plt.figure(name + ' (Runways Index)')
        self.printRunways(name)
        plt.figure(name + ' (Airports)')
        self.printAirports(name,limit,sameaxis)
        plt.figure(name + ' (Flights)')
        self.printFlights(name)
        plt.figure(name)
        Results.printEvolve(name)
        plt.show()

     
class CatTab(Runways,OAGTab,GraphCat) :
    "Provide a collection of function to classify the world countries according the civil aviation accesibility."

    def __init__(self,clee,liste) :
        "Provide an object with an HashMap, the type of the HashMap's key and the type of data in this HashMap (under the argument 'legend')."
        self.key = clee
        self.legend = liste
        self.htab = {}
    
    def size(self) :
        "Give the size of the HashMap."
        s=0
        for key in self.htab.keys() :
            s=s+1
        return s
    
    def copy(self) :
        "Provide a copy of the HashMap."
        if type(self.legend)!=list :
            raise TypeError("The copy is impossible, with a non-list legend.")
        New = CatTab(self.key,self.legend.copy())
        New.htab = self.htab.copy()
        return New

    def excel(self,spr,shname,convert=False) :
        "Produce an Excel spreadsheet with the given HashMap. The 'convert' argument matches the presence of iterable types in the CatTab Object."
        sheet = spr.add_sheet(shname)
        for k in range(len(self.legend)) :
            sheet.write(0,k,self.legend[k])
        i=1
        for line in self.htab.values() :
            for j in range(len(line)) :
                if convert :
                    word = str(line[j])
                else :
                    word = line[j]
                sheet.write(i,j,word)
            i=i+1

    def airport(self,Flights) :
        "Provide an HashMap with all the needed informations about the world Airports based on the Runways' database."
        Airports = CatTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways','Runway Index','Number of Flights In & Out','Number of Airlines'])
        for key,line in Flights.htab.items() :
            if key in self.htab :
                port = self.htab[key]
                Airports.htab[port[0]] = port.copy()
                Airports.htab[port[0]].extend([max(line[5],line[6]),line[9]])
            else :
                Switcher = {'a':'NAN','nfinit':'INF','Infinit':'INF','ZGC':'LHW','RSI':'IPZ','NDZ':'FCN','PNF':'NNK'}
                if key in Switcher :
                    port = self.htab[Switcher[key]]
                    Airports.htab[port[0]] = port.copy()
                    Airports.htab[port[0]].extend([max(line[5],line[6]),line[9]])
                elif key=='BFJ' and line[1]=='NFFA' :
                    port = self.htab['0BA']
                    Airports.htab[port[0]] = port.copy()
                    Airports.htab[port[0]].extend([max(line[5],line[6]),line[9]])
                else :
                    raise ValueError("The proposed IATA Airport Code is unknown : "+key)
        return Airports

    def classement(self,sizes) :
        "Add the category (based on the attendance levels) of the each Airport in the Airports' database. The argument 'sizes' give the percentage of airports in each categories in ascending order."
        if sum(sizes)!=1.0 :
            raise ValueError("The sum of all elements in sizes must be equal to 1.")
        self.legend.append('Category of the Airport')
        Sort = []
        for key,line in self.htab.items() :
            Sort.append((key,line[8]))
        Sort.sort(key=lambda x:x[1])
        n,nb = len(Sort),len(sizes)
        sizes.insert(0,0)
        Category = []
        for k in range(1,nb) :
            Category.append(int(sizes[k]*n)+1)
            sizes[k] = Category[k-1]+sum(sizes[0:k])
            for pair in Sort[sizes[k-1]:sizes[k]] :
                self.htab[pair[0]].append(k)
        for pair in Sort[sizes[nb-1]:] :
            self.htab[pair[0]].append(nb)
        Category.append(n-sum(Category))
        return Category
    
    def major(self,lim,prop) :
        "Provide an HashMap with the main Airports of each country using the Airports' database. The argument 'lim' give the minimum category starting which all the airports are kept and 'prop' the needed number of flight to be significant regarding the biggest airport in the country."
        PortbyState = CatTab('Country Code',['List of Airport in this Country'])
        for key,line in self.htab.items() :
            if line[4] in PortbyState.htab :
                PortbyState.htab[line[4]].append([line[0],line[8],line[10]])
            else :
                PortbyState.htab[line[4]] = [[line[0],line[8],line[10]]]
        Major = CatTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways','Number of Flights In & Out','Number of Airlines'])
        for key,line in PortbyState.htab.items() :
            mx = line[0][1]
            for port in line[1:] :
                if port[1]>mx :
                    mx = port[1]
            for port in line :
                if port[2]>=lim or port[1]>prop*mx :
                    Major.htab[port[0]] = self.htab[port[0]]
        return Major
    
    def nationRwys(self) :
        "Provide an HashMap with the Runway National Index by Country using the Airports' database."
        Plane = CatTab('Country Code',['Country Code','Country Name','Runway National Index'])
        for line in self.htab.values() :
            if line[4] in Plane.htab :
                admin = Plane.htab[line[4]]
                admin[2] = admin[2] + line[7]
                admin[3] = admin[3] + 1
            else :
                Plane.htab[line[4]] = [line[4],line[5],line[7],1]
        for line in Plane.htab.values() :
            line[2] = (line[2],line[2]/line[3])
            del line[3]
        return Plane
    
    def land1(self,Airlines,Plane) :
        "Provide an HashMap with the needed categories to build the first categorization using the Major Airports' database."
        State = CatTab('Country Code',['Country Code','Country Name','Number of Major Airport','Global Runway National Index','Synthetic Runway Index','Number of National Airlines'])
        for line in self.htab.values() :
            if line[4] in State.htab :
                land = State.htab[line[4]]
                land[2] = land[2]+1
            else :
                State.htab[line[4]] = [line[4],line[5],1]
        for key,line in State.htab.items() :
            if key in Plane.htab :
                line.extend(Plane.htab[key][2])
            else :
                line.append('None')
            if key in Airlines.htab :
                line.append(Airlines.htab[key][2])
            else :
                line.append(0)
        return State
    
    def category1(self) :
        "Provide an HashMap with the category of each Country according their Civil Aviation Facilities using the States' database."
        Class = CatTab('Country Code',['Country Code','Country Name','Country Category 1'])
        for line in self.htab.values() :
            if line[2]>2 :
                Class.htab[line[0]] = [line[0],line[1],'F']
            elif line[2]==2 :
                Class.htab[line[0]] = [line[0],line[1],'E']
            else :
                if line[4]>1 :
                    Class.htab[line[0]] = [line[0],line[1],'D']
                else :
                    if line[5]>1 :
                        Class.htab[line[0]] = [line[0],line[1],'C']
                    elif line[5]==1 :
                        Class.htab[line[0]] = [line[0],line[1],'B']
                    else :
                        Class.htab[line[0]] = [line[0],line[1],'A']
        return Class
    
    def land2(self,nb):
        "Provide an HashMap with the needed categories to build the second categorization using the final Airports' database. The argument 'nb' matches the number of airport categories."
        Country = CatTab('Country Code',['List of Airports in the Country'])
        for key,line in self.htab.items() :
            if line[4] in Country.htab :
                Country.htab[line[4]].append(line)
            else :
                Country.htab[line[4]] = [line]
        World = CatTab('Country Code',['Country Code','Country Name','Number of Flights In & Out','Global Number of Airports','Number of Airports by Categories of Size'])
        for key,line in Country.htab.items() :
            World.htab[key] = [key,line[0][5]]
            Fl = 0
            Category = [0 for k in range(nb)]
            for port in line :
                Fl = Fl+port[8]
                cat = port[10]-1
                Category[cat] = Category[cat]+1
            World.htab[key].append(Fl)
            World.htab[key].append(sum(Category))
            World.htab[key] = World.htab[key] + Category
        return World
    
    def category2(self) :
        "Provide an HashMap with the category of each Country according their National Flight Traffic using the Countries' database."
        Class = CatTab('Country Code',['Country Code','Country Name','Country Category 2'])
        for line in self.htab.values() :
            if line[6]>1 :
                if line[3]>49 :
                    Class.htab[line[0]] = [line[0],line[1],'F']
                else :
                    Class.htab[line[0]] = [line[0],line[1],'E']
            elif line[6]==1 :
                Class.htab[line[0]] = [line[0],line[1],'D']
            else :
                if line[5]>1 :
                    Class.htab[line[0]] = [line[0],line[1],'C']
                elif line[5]==1 :
                    Class.htab[line[0]] = [line[0],line[1],'B']
                else :
                    Class.htab[line[0]] = [line[0],line[1],'A']
        return Class

    def crossing_categories(self,Class1,Class2,year) :
        "Provide an HashMap with the category of each country according Civil Aviation Accessibility using the World Bank Income Classification's database. The argument 'year' matches the year of the classification."
        Class = CatTab('Country Code',['Country Code','Country Name','World Bank Income Category', 'Country Category'])
        for key,line in Class1.htab.items() :
            cat1,cat2 = line[2],Class2.htab[key][2]
            Class.htab[key] = line[:2]
            if cat1==cat2 :
                Class.htab[key].append('Unspecified')
                Class.htab[key].append(cat1)
            elif key in self.htab and self.htab[key][2].htab[year] != None :
                wbank = self.htab[key][2].htab[year][2]
                Class.htab[key].append(self.htab[key][2].htab[year][1])
                if cat1=='A' :
                    if cat2=='B' :
                        if wbank>2 :
                            Class.htab[key].append(cat2)
                        else :
                            Class.htab[key].append('A')
                    elif cat2=='C' :
                        if wbank==4 :
                            Class.htab[key].append('C')
                        elif wbank>1 :
                            Class.htab[key].append('B')
                        else :
                            Class.htab[key].append('A')
                    elif cat2=='D' :
                        if wbank>2 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    else :
                        raise AttributeError("The combinaison between A & E,F is impossible.")
                elif cat1=='B' :
                    if cat2=='A' :
                        Class.htab[key].append('A')
                    elif cat2=='C' :
                        if wbank>2 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    elif cat2=='D' :
                        if wbank==4 :
                            Class.htab[key].append('D')
                        elif wbank>1 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    else :
                        raise AttributeError("The combinaison between B & E,F is impossible.")
                elif cat1=='C' :
                    if cat2=='A' :
                        Class.htab[key].append('A')
                    elif cat2=='B' :
                        if wbank>2 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    elif cat2=='D' :
                        if wbank>2 :
                            Class.htab[key].append('D')
                        else :
                            Class.htab[key].append('C')
                    else :
                        raise AttributeError("The combinaison between C & E,F is impossible.")
                elif cat1=='D' :
                    if cat2=='A' :
                        Class.htab[key].append('A')
                    elif cat2=='B' :
                        if wbank==4 :
                            Class.htab[key].append('D')
                        elif wbank>1 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    elif cat2=='C' :
                        if wbank>2 :
                            Class.htab[key].append('D')
                        else :
                            Class.htab[key].append('C')
                    else :
                        raise AttributeError("The combinaison between D & E,F is impossible.")
                elif cat1=='E' :
                    if cat2=='A' :
                        Class.htab[key].append('A')
                    elif cat2=='B' :
                        if wbank>2 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    elif cat2=='C' :
                        if wbank>2 :
                            Class.htab[key].append('D')
                        else :
                            Class.htab[key].append('C')
                    elif cat2=='D' :
                        if wbank>2 :
                            Class.htab[key].append('E')
                        else :
                            Class.htab[key].append('D')
                    else :
                        Class.htab[key].append('F')
                else :
                    if cat2=='A' :
                        Class.htab[key].append('A')
                    elif cat2=='B' :
                        if wbank>2 :
                            Class.htab[key].append('C')
                        else :
                            Class.htab[key].append('B')
                    elif cat2=='C' :
                        if wbank>2 :
                            Class.htab[key].append('D')
                        else :
                            Class.htab[key].append('C')
                    elif cat2=='D' :
                        if wbank==4 :
                            Class.htab[key].append('F')
                        elif wbank>1 :
                            Class.htab[key].append('E')
                        else :
                            Class.htab[key].append('D')
                    else :
                        if wbank>2 :
                            Class.htab[key].append('F')
                        else :
                            Class.htab[key].append('E')
            else :
                Class.htab[key].append('None')
                Class.htab[key].append(str([cat1,cat2]))
        return Class

    def airportStats(self,sizes,year) :
        "Provide an list with the limit sizes of each airports categories."
        limit = [year]
        limit.extend([0 for k in range(len(sizes))])
        for line in self.htab.values() :
            if line[8]>limit[line[10]] :
                limit[line[10]] = line[8]
        return limit
    
    def classification(self,Code,Runways,Income,year,sizes=(0.42,0.42,0.16),lim=3,prop=0.5) :
        "Provide two HashMap, one with the final classification of countries for a given year and another with all the useful informations for this classification using the yearly OAG database."
        Airlines = self.airlines(Code)
        Airlines = Airlines.nationAL()
        Flights = self.flights(Code)
        Flights.linePorts(self)
        Airports = Runways.airport(Flights)
        Airports.classement(list(sizes))
        limit = Airports.airportStats(sizes,year)
        if 'GZA' in Airports.htab :
            del Airports.htab['GZA']
        if year<2011 :
            for iata in ['JUB','MAK','RBX','WUU'] :
                if iata in Airports.htab :
                    Airports.htab[iata][4:6] = ['SDN','Sudan']
        Plane = Airports.nationRwys()
        Major = Airports.major(lim,prop)
        State = Major.land1(Airlines,Plane)
        Class1 = State.category1()
        Country = Airports.land2(len(sizes))
        Class2 = Country.category2()
        Class = Income.crossing_categories(Class1,Class2,year)
        Info = CatTab('Country Code',['Country Code','Country Name','Number of Flights In & Out','Global Number of Airports','Number of Small Airports','Number of Average Airports','Number of Big Airports','Global Runway National Index','Synthetic Runway Index','Number of National Airlines','World Bank Income Category'])
        Info.htab = Country.htab.copy()
        for key,line in State.htab.items() :
            Info.htab[key].extend(line[3:])
        for key,line in Income.htab.items() :
            if key in Info.htab and line[2].htab[year]!=None :
                Info.htab[key].append(line[2].htab[year][1])
        return Class,Info,limit           

    def edit(self) :
        "Save the database with every useful information for the classification under a 'json' format."
        with open('Informations.json','w') as info :
            for year,ctab in self.htab.items() :
                lg = ctab.legend
                for line in ctab.htab.values() :
                    Htab = {'Year':str(year)}
                    for i in range(len(line)) :
                        Htab[lg[i]] = str(line[i])
                    json.dump(Htab,info)
                    info.write('\n')

    def stability(self,Code,year) :
        "Provide an HashMap with some Index of Countries for a given time (from 'year' argument until today). The Stability Index is the maximum of variation (always positive) whereas the Evolution Index show the direction of the evolution."
        Stab = CatTab('Country Code',['Country Code','Country Name','Stability Index','Evolution Index','Stability Category'])
        for key,line in self.htab.items() :
            for liste in Code.htab.values() :
                if liste[0]==key :
                    code = liste[2]
                    break
            start = year-2003
            Stab.htab[code] = [code,key,max(line[start:])-min(line[start:]),line[-1]-line[start]]
        for line in Stab.htab.values() :
            if line[3]<0 :
                line.append('Worrying')
            elif line[3]>0 :
                line.append('Encouraging')
            else :
                if line[2]==0 :
                    line.append('Stable')
                else :
                    line.append('Unstable')
        return Stab
                