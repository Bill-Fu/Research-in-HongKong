#coding:utf-8

###This code is to process the data in scn.txt

from numpy import *
import copy

defaultFileName1="C:/Users/fuhao/Dropbox/scn.txt"
defaultdate1="2003-04"
defLabel=0

G1={}
G2={}
G1[1]={}
G1[2]={}
G1[3]={}
G1[4]={}
G1[5]={}
G1[6]={}
G1[7]={}
G1[8]={}
G2[1]={}
G2[2]={}
G2[3]={}
G2[4]={}
G2[5]={}
G2[6]={}
G2[7]={}
G2[8]={}
G1[1][2]=0
G1[1][3]=0
G1[2][4]=0
G1[2][3]=0
G1[3][2]=0
G1[4][6]=0
G1[5][6]=0
G1[5][7]=0
G1[6][3]=0
G1[6][8]=0
G1[7][8]=0
G2[2][1]=0
G2[3][1]=0
G2[4][2]=0
G2[3][2]=0
G2[2][3]=0
G2[6][4]=0
G2[6][5]=0
G2[7][5]=0
G2[3][6]=0
G2[8][6]=0
G2[8][7]=0

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
        dir_graph1[i[0]][i[1]]=defLabel
        dir_graph2[i[1]][i[0]]=defLabel
        undir_graph[i[0]][i[1]]=defLabel
        undir_graph[i[1]][i[0]]=defLabel

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
###CalComPos1(dir_graph1,dir_graph2)
###return listOfPos,dictOfCom
def CalComPos1():
    graph1,graph2,graph3=file2graph()

    listOfPos=[]
    listOfPos.append(set())
    listOfPos.append(set())
    dictOfCom={}
    tmp=1
    
    for node in graph1:
        dictOfCom[node]=0

    for node in graph2:
        if(len(graph2[node])==0):
            listOfPos[-1].add(node)
            dictOfCom[node]=tmp

    while(len(listOfPos[-1])!=0):
        tmp+=1
        listOfPos.append(set())
        for node in listOfPos[-2]:
            for cus in graph1[node]:
                if(dictOfCom[cus]==0):
                    dictOfCom[cus]=tmp
                    listOfPos[-1].add(cus)

    return listOfPos,dictOfCom

###This function remove the loop in the supply chain graph, by removing the last
###added connections that may cause loop in network
###rmLoop(dir_graph1,dir_graph2,undir_graph)
###return new_dir_graph1,new_dir_graph2,new_undir_graph
def rmLoop(dir_graph1,dir_graph2):
    listOfPos=[[]]
    new_dir_graph1=copy.deepcopy(dir_graph1)
    new_dir_graph2=copy.deepcopy(dir_graph2)
    Sum=0
    rm=0
    
    for node in dir_graph2:
        if(len(dir_graph2[node])==0):
            tmpList=[]
            tmpList.append(node)
            listOfPos[-1].append(tmpList)

    while(len(listOfPos[-1])!=0):
        listOfPos.append([])
        for node in listOfPos[-2]:
            for cus in dir_graph1[node[-1]]:
                Sum+=1
                if(cus in node):
                    if(new_dir_graph1[node[-1]].has_key(cus)):
                        del new_dir_graph1[node[-1]][cus]
                        del new_dir_graph2[cus][node[-1]]
                        rm+=1
                else:
                    tmpLis=[]
                    for item in node:
                        tmpLis.append(item)
                    tmpLis=copy.deepcopy(node)
                    tmpLis.append(cus)
                    listOfPos[-1].append(tmpLis)
                    
    return new_dir_graph1,new_dir_graph2,rm,Sum,listOfPos

###This function remove the loop in the supply chain graph, by removing the last
###added connections that may cause loop in network,this is a new function
###because the last one need too much memory
###rmLoopNew(dir_graph1,dir_graph2,undir_graph)
###return new_dir_graph1,new_dir_graph2,new_undir_graph
def rmLoopNew(dir_graph1,dir_graph2):    
    Stack=[]
    path=[]
    fir_sup=[]

    for node in dir_graph2:
        if(len(dir_graph2[node])==0):
            fir_sup.append(node)
    left=len(fir_sup)
    
    for node in fir_sup:
        print left,"to be processed"
        left-=1
        path.append(node)
        Stack.append([])
        #print path
        for item in dir_graph1[node]:
            Stack[0].append(item)
        while(len(path)!=0):
            while(len(dir_graph1[Stack[-1][-1]])!=0 and (Stack[-1][-1] in path)==False):
                Stack.append([])
                for item in dir_graph1[Stack[-2][-1]]:
                    Stack[-1].append(item)
                path.append(Stack[-2].pop())
                #print path
            if(Stack[-1][-1] in path):
                del dir_graph1[path[-1]][Stack[-1][-1]]
                del dir_graph2[Stack[-1][-1]][path[-1]]
                print "Del",path[-1],"->",Stack[-1][-1]
            Stack[-1].pop()
            while(len(Stack)!=0 and len(Stack[-1])==0):
                Stack.pop()
                path.pop()
                #print path
                
