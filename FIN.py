#coding:utf-8
###This code is about establish graph from given file, and then evaluate
###the important node in this network
from numpy import *

###This function can convert the file to a network graph, this can return two
###graphs, the first is an directed graph, which is the real network, and the second
###is also an directed graph,but the direct is opposed to the former one, and the 
###third one is an undirected graph, which would be easy to find the connected
###subset
###file2graph(filename,date)
###return dir_graph1,dir_graph2,undir_graph

def file2graph(filename,date):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)

    dir_graph1={}
    dir_graph2={}
    undir_graph={}
    
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('","')
        if(len(listFromLine)>5 and listFromLine[1]==date):
            if(dir_graph1.has_key(listFromLine[2])==False):
                dir_graph1[listFromLine[2]]={}
            else:
                if(dir_graph1[listFromLine[2]].has_key(listFromLine[5])==False):
                    dir_graph1[listFromLine[2]][listFromLine[5]]=1
            if(dir_graph1.has_key(listFromLine[5])==False):
                dir_graph1[listFromLine[5]]={}

            if(dir_graph2.has_key(listFromLine[5])==False):
                die_graph2[listFromLin[5]]={}
            else:
                if(dir_graph2[listFromLine[5]].has_key(listFromLine[2])==False):
                    dir_graph2[listFromLine[5]][listFromLine[2]]=1
            if(dir_graph2.has_key(listFromLine[2])==False):
                dir_graph2[listFromLine[2]]={}

            if(undir_graph.has_key(listFromLine[2]))==False:
                undir_graph[listFromLine[2]]={}
            else:
                if(undir_graph[listFromLine[2]].has_key(listFromLine[5])==False):
                    undir_graph[listFromLine[2]][listFromLine[5]]=1
            if(undir_graph.has_key(listFromLine[5]))==False:
                undir_graph[listFromLine[5]]={}
            else:
                if(undir_graph[listFromLine[5]].has_key(listFromLine[2])==False):
                    undir_graph[listFromLine[5]][listFromLine[2]]=1

    
    return dir_graph1,dir_graph2,undir_graph

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

