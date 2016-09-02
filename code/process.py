#coding:utf-8

###This code is to further process the data base on scn.py and naics.py

from numpy import *
import naics
import scn
import csv
import sys
import random
##################################################################
###RETURN THE AVERAGE TIER IN SUPPLY CHAIN NETWORK OF EVERY NAICS  
##################################################################
###This function find the different position in same kind of naics
###indicated by first 2 digits of NAICS
###naics2pos()
###return dict_naics2pos,lostRate
def naics2pos():
    graph1,graph2=scn.rmUnused()
    dir_graph1,dir_graph2=scn.rmLoopNew(graph1,graph2)
    dictOfCom=scn.CalPos1(dir_graph1,dir_graph2)
    
    dict_naics=naics.file2dict()

    dict_naics2pos={}
    lost=0
    dict_naics2pos_nor={}
    
    for node in dictOfCom:
        if(dict_naics.has_key(node)):
            nc=dict_naics[node][0:2]
            if(dict_naics2pos.has_key(nc)):
                dict_naics2pos[nc].append(dictOfCom[node])
            else:
                dict_naics2pos[nc]=[]
                dict_naics2pos[nc].append(dictOfCom[node])
        else:
            lost+=1

    for item in dict_naics2pos:
        dict_naics2pos_nor[item]=sum(dict_naics2pos[item])/len(dict_naics2pos[item])
    
    return dict_naics2pos_nor,float(lost)/len(dictOfCom)

def write_naics2pos_csv():
    graph1,graph2=scn.rmUnused()
    dir_graph1,dir_graph2=scn.rmLoopNew(graph1,graph2)
    dictOfCom=scn.CalPos1(dir_graph1,dir_graph2)
    
    dict_naics=naics.file2dict()

    data=[]
    for node in dictOfCom:
        if(dict_naics.has_key(node)):
            if(dictOfCom[node]==1):
                tmp=(node,0,int(dict_naics[node][0:1]))
            else:
                tmp=(node,int(1+dictOfCom[node]/20)*20,int(dict_naics[node][0:1]))
        else:
            if(dictOfCom[node]==1):
                tmp=(node,0,0)
            else:
                tmp=(node,int(1+dictOfCom[node]/20)*20,0)
        data.append(tmp)

    csvfile=file('com_pos_naics.csv','wb')
    writer=csv.writer(csvfile)
    writer.writerow(['Company','Tier','NAICS'])

    for row in data:
        writer.writerow(row)

    csvfile.close()
            
###################################################################
###WRITE THE NODE AND EDGE INFORMATION OF ORIGINAL GRAPH TO CSV
###################################################################
###This function write the graph information to csv file to draw 
###in the Gephi,currently we draw the original graph with loop
###writeGraph2csv()
###return none
def writeGraph2csv():
    graph1,graph2=scn.rmUnused()
    graph1,graph2=scn.rmLoopNew(graph1,graph2)
    
    data=[]
    for node in graph1:
        for item in graph1[node]:
            tmp=(node,item,"Directed","","",1)
            data.append(tmp)

    csvfile=file('graph_noloop.csv','wb')
    writer=csv.writer(csvfile)
    writer.writerow(['Source','Target','Type','Id','Label','Weight'])
            
    for row in data:
        writer.writerow(row)

    csvfile.close()
	
	
###################################################################
###WRITE THE NODE, EDGE AND NAICS INFORMATION OF LOOP-REMOVED GRAPH TO CSV
###################################################################
###This function write the graph information to csv file to draw 
###in the Gephi, the graph which is already removed loop, we also add
###the NAICS classification information to it. 
###writeNodeLabel2csv()
###return none

def writeNodeLabel2csv():
    graph1,graph2=scn.rmUnused()
    dict_naics=naics.file2dict()
    
    data=[]
    time=0
    for node in graph1:
        if(dict_naics.has_key(node)):
            tmp=(node,int(dict_naics[node][0]),int(dict_naics[node][0]))
            data.append(tmp)
        else:
            tmp=(node,0,0)
            time+=1
            data.append(tmp)

    csvfile=file('node_naics.csv','wb')
    writer=csv.writer(csvfile)
    writer.writerow(['Id','Label','Modularity Class'])

    for row in data:
        writer.writerow(row)

    csvfile.close()

    return len(data),time
