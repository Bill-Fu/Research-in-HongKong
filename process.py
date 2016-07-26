#coding:utf-8

###This code is to further process the data base on scn.py and naics.py

from numpy import *
import naics
import scn

###This function find the different position in same kind of naics
###naics2pos()
###return dict_naics2pos,rate
def naics2pos():
    listOfPos,dictOfCom=scn.CalComPos()
    dict_naics=naics.file2dict()

    dict_naics2pos={}
    lost=0
    listtmp=[]
    dict_new={}
    dict_naics2pos_nor={}
    
    for node in dictOfCom:
        if(dict_naics.has_key(node)):
            nc=dict_naics[node][0:2]
            if(dict_naics2pos.has_key(nc)):
                if(dict_naics2pos[nc].has_key(dictOfCom[node])):
                    dict_naics2pos[nc][dictOfCom[node]]+=1
                else:
                    dict_naics2pos[nc][dictOfCom[node]]=1
            else:
                dict_naics2pos[nc]={}
                dict_naics2pos[nc][dictOfCom[node]]=1
        else:
            lost+=1

    for item in dict_naics2pos:
        S=0
        for tmp in dict_naics2pos[item]:
            S+=dict_naics2pos[item][tmp]
        dict_new[item]=S

    for item in dict_naics2pos:
        for tmp in dict_naics2pos[item]:
            if(dict_naics2pos_nor.has_key(item)==False):
                dict_naics2pos_nor[item]={}
                dict_naics2pos_nor[item][tmp]=float(dict_naics2pos[item][tmp])/dict_new[item]
            else:
                dict_naics2pos_nor[item][tmp]=float(dict_naics2pos[item][tmp])/dict_new[item]
            
    return dict_naics2pos,dict_naics2pos_nor,float(lost)/len(dictOfCom)
            
