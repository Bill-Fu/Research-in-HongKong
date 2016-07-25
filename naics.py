#coding:utf-8

###This code is to handle the data in ac8a0f06a2d2d0b8.txt

from numpy import *

defaultFileName1="C:/Users/fuhao/Dropbox/Industry/ac8a0f06a2d2d0b8new.txt"

###This function convert the file to a dict, which you can use 6 digits cusip id
###to find its naics id
###file2dict(filename=defaultFileName1)
###return dict_naics
def file2dict(filename=defaultFileName1):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)

    dict_naics={}
    dict_sic={}
    fault=0
    S=0
    s=set()

    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split(',')
        if(len(listFromLine[3])>7 and listFromLine[3].find(".")==-1):
            S+=1
            if(len(listFromLine[3])==8):
                cusip="0"+listFromLine[3][0:5]
            else:
                cusip=listFromLine[3][0:6]
            if(dict_naics.has_key(cusip)==False):
                dict_naics[cusip]=listFromLine[5]
            else:
                if(dict_naics[cusip]!=listFromLine[5]):
                    fault+=1
                    s.add(cusip)

    return dict_naics
