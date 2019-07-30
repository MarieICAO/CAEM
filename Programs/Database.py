# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:03:04 2019

@author: Maël Akouz
"""

import xlwt

class PrintText :
    "Give an overview of a TXT or JSON document."
    
    def __init__(self,link) :
        "Provide a list of the document's lines (the one matching with the given link)." 
        txt = open(link,'r')
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
            
    def line(self,k,a,b):
        "Extrat the valuable data of the given line (for an OAG document only)."
        p=0
        while self.data[k][p]!=':' :
            p=p+1
        d=p+a
        while self.data[k][p]!=',' :
            p=p+1
        f=p-b
        return self.data[k][d:f]

class HashTab :
    "Provide a collection of function to exploit an OAG text document."
    
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

    def excel(self,spr,shname) :
        "Produce an Excel spreadsheet with the given HashMap."
        sheet = spr.add_sheet(shname)
        for k in range(len(self.legend)) :
            sheet.write(0,k,self.legend[k])
        i=1
        for line in self.htab.values() :
            for j in range(len(line)) :
                sheet.write(i,j,line[j])
            i=i+1
        
    def database(txt) :
        "Provide an HashMap with all the informations including in the yearly OAG document."
        Data = HashTab('{Airline + From IATA Airport + To IATA Airport} Code',['Airline Code','Airline Name','Airline Country','From IATA Airport Code','From ICAO Airport Code','From Airport Name','From Airport Country','To IATA Airport Code','To ICAO Airport Code','To Airport Name','To Airport Country','Number of Flights by Year','Number of Seat by Flight','Number of Used Planes'])
        i=1
        while i<len(txt.data) :
            l = []
            for j in range(2,13) :
                l.append(txt.line(i+j,3,1))
            l.append(int(txt.line(i+13,2,0))), l.append(int(txt.line(i+14,2,0)))
            l.append(int(txt.data[i+15][-2]))
            Data.htab[l[0]+l[3]+l[7]] = l
            i=i+18
        return Data
    
    def countryCode(txt) :
        "Provide an HashMap with the relevant ISO Codes and their meaning."
        Code = HashTab('Alpha-3 Code',['Country','Alpha-2 Code','Alpha-3 Code','Numeric code','Continent'])
        for i in range(1,len(txt.data)) :
            l = txt.data[i].split(',')
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
    
    def income(txt) :
        "Provide an HashMap with the Country's wealth groups of the World Bank."
        Income = HashTab('Country Code',['Country Code','Country Name','Category'])
        for line in txt.data :
            l = line.split('\t')
            Income.htab[l[3]] = [l[3],l[2],l[6]]
        return Income
    
    def airlines(self,Code) :
        "Provide an HashMap of the Airlines and their characteristics." 
        Airline = HashTab('Airline Code',['Airline Code','Airline Name','Country Code','Country Name','Number of Air Links'])
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
        "Provide an HashMap with the number of Airlines located in each considered Country."
        Country = HashTab('Country Code',['Country Code','Country name','Number of Airlines'])
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
        "Provide an HashMap of the Airports and their characteristics. The argument 'fill' matches with the average filling of each flight (to give an idea of the number passengers using this airport)."
        Flight = HashTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','Airport Country Code','Airport Country Name','Number of Flight Out','Number of Flight In','Number of Passenger Out','Number of Passenger In'])
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
        "Add the number of present Airlines in each Airport in a previous HashMap containing already the attendance levels of each Airport."
        Airterminal = HashTab('IATA Airport Code',['List of Airlines Using this Airport'])
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
    
    def runways(txt) :
        "Provide an HashMap with the number of Runways by Airport."
        Runways = HashTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways'])
        for line in txt.data[1:] :
            l = line.split('\t')
            Runways.htab[l[0]] = [l[0],l[1],l[2],l[3],l[4],l[5],int(l[6][0])]
        return Runways
    
    def airport(self,Flights) :
        "Provide an HashMap with all the needed informations about the world Airports."
        Airports = HashTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways','Number of Flights In & Out','Number of Airlines'])
        for key,line in Flights.htab.items() :
            if key in self.htab :
                port = self.htab[key]
                Airports.htab[port[0]] = [port[0],port[1],port[2],port[3],port[4],port[5],port[6],max(line[5],line[6]),line[9]]
            else :
                if key=='a' :
                    port = self.htab['NAN']
                    Airports.htab[port[0]] = [port[0],port[1],port[2],port[3],port[4],port[5],port[6],max(line[5],line[6]),line[9]]
                elif key=='nfinit' :
                    port = self.htab['INF']
                    Airports.htab[port[0]] = [port[0],port[1],port[2],port[3],port[4],port[5],port[6],max(line[5],line[6]),line[9]]
                else :
                    print(line)
        return Airports

    def classement(self,sizes) :
        "Add the category (based on the attendance levels) of the each Airport in a previous HashMap containing their characteristics. The argument 'sizes' give the percentage of airports in each categories."
        if sum(sizes)!=1 :
            raise ValueError("The sum of all elements in sizes must be equal to 1.")
        self.legend.append('Category of the Airport')
        Sort = []
        for key,line in self.htab.items() :
            Sort.append((key,line[7]))
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
        "Provide an HashMap with the main Airports of each country in the selected document. The argument 'lim' give the minimum category starting which all the airports are kept and 'prop' the needed number of flight to be significant regarding the biggest airport in the country."
        PortbyState = HashTab('Country Code',['List of Airport in this Country'])
        for key,line in self.htab.items() :
            if line[4] in PortbyState.htab :
                PortbyState.htab[line[4]].append([line[0],line[7],line[9]])
            else :
                PortbyState.htab[line[4]] = [[line[0],line[7],line[9]]]
        Major = HashTab('IATA Airport Code',['IATA Airport Code','ICAO Airport Code','Airport Name','City Name','Country Code','Country Name','Number of Runways','Number of Flights In & Out','Number of Airlines'])
        for key,line in PortbyState.htab.items() :
            mx = line[0][1]
            for port in line[1:] :
                if port[1]>mx :
                    mx = port[1]
            for port in line :
                if port[2]>=lim or port[1]>prop*mx :
                    Major.htab[port[0]] = self.htab[port[0]]
        return Major
    
    def land1(self,Country,Income) :
        "Provide an HashMap with the needed categories to build the first categorization."
        State = HashTab('Country Code',['Country Code','Country Name','Number of Airport','Maximum Number of Runways by Airport','Number of National Airlines','World Bank Income Category'])
        for line in self.htab.values() :
            if line[4] in State.htab :
                land = State.htab[line[4]]
                land[2] = land[2]+1
                if land[3]<line[6] :
                    land[3] = line[6]
            else :
                State.htab[line[4]] = [line[4],line[5],1,line[6]]
        for key,line in State.htab.items() :
            if key in Country.htab :
                line.append(Country.htab[key][2])
            else :
                line.append(0)
            if key in Income.htab :
                line.append(Income.htab[key][2])
            else :
                line.append(None)
        return State
    
    def land2(self,Airlines,Income,nb):
        "Provide an HashMap with the needed ctegories to build the first categorization. The argument 'nb' matches the number of airport categories."
        Country = HashTab('Country Code',['List of Airports in the Country'])
        for key,line in self.htab.items() :
            if line[4] in Country.htab :
                Country.htab[line[4]].append(line)
            else :
                Country.htab[line[4]] = [line]
        World = HashTab('Country Code',['Country Code','Country Name','World Bank Income Category','Number of National Airlines','Maximum Number of Runways by Airport','Number of Flights In & Out','Global Number of Airports','Number of Airports by Categories of Size'])
        for key,line in Country.htab.items() :
            World.htab[key] = [key,line[0][5]]
            if key in Income.htab :
                World.htab[key].append(Income.htab[key][2])
            else :
                World.htab[key].append(None)
            if key in Airlines.htab :
                World.htab[key].append(Airlines.htab[key][2])
            else :
                World.htab[key].append(0)
            mx = 0
            Fl = 0
            Category = [0 for k in range(nb)]
            for port in line :
                Fl = Fl+port[7]
                if mx<int(port[6]) :
                    mx = int(port[6])
                cat = port[9]-1
                Category[cat] = Category[cat]+1
            World.htab[key].append(mx)
            World.htab[key].append(Fl)
            World.htab[key].append(sum(Category))
            World.htab[key] = World.htab[key] + Category
        return World
