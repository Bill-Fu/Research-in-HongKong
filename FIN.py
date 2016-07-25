#coding:utf-8
###This code is about establish graph from given file, and then evaluate
###the important node in this network
from numpy import *

###This function can convert the file to a network graph
###file2graph(filename,date)
###return graph

def file2graph(filename,date):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)

    graph={}
    
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('","')
        if(len(listFromLine)>5 and listFromLine[1]==date):
            if(graph.has_key(listFromLine[2])==False):
                graph[listFromLine[2]]={}
            else:
                if(graph[listFromLine[2]].has_key(listFromLine[5])==False):
                    graph[listFromLine[2]][listFromLine[5]]=1
            if(graph.has_key(listFromLine[5])==False):
                graph[listFromLine[5]]={}

    return graph

###This function can calculate the company number for each month from 2003-01 to 2015-12
###ComNum(filename)
###return None

def ComNum(filename):
    list1=['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    list2=['01','02','03','04','05','06','07','08','09','10','11','12']
    for i in list1:
        for j in list2:
            graph=file2graph("C:/Users/fuhao/Dropbox/scn.txt",i+'-'+j)
            print i+'-'+j," %s"%len(graph)

