#coding:utf-8

###This code is to process the data in scn.txt

from numpy import *

defaultFileName1="C:/Users/fuhao/Dropbox/scn.txt"
defaultdate1="2003-04"
defStren=1

###This function can convert the file to a network graph, this can return two
###graphs, the first is an directed graph, which is the real network, and the second
###is also an directed graph,but the direct is opposed to the former one, and the 
###third one is an undirected graph, which would be easy to find the connected
###subset
###I rewrite the code so that the keys of the graph will be cusip id(6 digits)
###instead of the name of the company
###file2graph(filename=defaultFileName,date=defaultdate)
###return dir_graph1,dir_graph2,undir_graph

def file2graph(filename=defaultFileName1,date=defaultdate1):
    fr=open(filename)
    arrayOLines=fr.readlines()
    
    dir_graph1={}
    dir_graph2={}
    undir_graph={}
    l=[]
    tmp=[]
    
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('","')
        
        if(len(listFromLine)>8 and listFromLine[1]==date):
            if((len(listFromLine[3])==8 or len(listFromLine[3])==9) and (len(listFromLine[6])==8 or len(listFromLine[6])==9)):
                sup_cusip=listFromLine[3][0:6]
                cus_cusip=listFromLine[6][0:6]
                tmp.append(sup_cusip)
                tmp.append(cus_cusip)
                l.append(tmp)
                tmp=[]
    for i in l:
        dir_graph1[i[0]]={}
        dir_graph1[i[1]]={}
        dir_graph2[i[0]]={}
        dir_graph2[i[1]]={}
        undir_graph[i[0]]={}
        undir_graph[i[1]]={}

    for i in l:
        dir_graph1[i[0]][i[1]]=defStren
        dir_graph2[i[1]][i[0]]=defStren
        undir_graph[i[0]][i[1]]=defStren
        undir_graph[i[1]][i[0]]=defStren

    return dir_graph1,dir_graph2,undir_graph

###This function can calculate the company number for each month from 2003-01 to 2015-12
###ComNum(filename=defaultFileName)
###return None

def ComNum(filename=defaultFileName1):
    list1=['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    list2=['01','02','03','04','05','06','07','08','09','10','11','12']
    for i in list1:
        for j in list2:
            graph1,graph2,graph3=file2graph("C:/Users/fuhao/Dropbox/scn.txt",i+'-'+j)
            print i+'-'+j," %s"%len(graph3)

###This function calculate the position of a given company in the supply chain
###for the companies that are not supplied by other companies, the position is 1
###the total number of listOfPos may be not equal to the total number of dictOfCom, cause there are loops
###CalComPos(dir_graph1,dir_graph2)
###return listOfPos,dictOfCom
def CalComPos():
    graph1,graph2,graph3=file2graph()

    listOfPos=[[],[]]
    dictOfCom={}
    tmp=1
    
    for node in graph1:
        dictOfCom[node]=0

    for node in graph2:
        if(len(graph2[node])==0):
            listOfPos[-1].append(node)
            dictOfCom[node]=tmp
    

    while(len(listOfPos[-1])!=0):
        tmp+=1
        listOfPos.append([])
        for node in listOfPos[-2]:
            for cus in graph1[node]:
                if(dictOfCom[cus]==0):
                    dictOfCom[cus]=tmp
                    listOfPos[-1].append(cus)

    return listOfPos,dictOfCom
