This is the source code of our project.

scn.py constructe the supply chain network and process it.
naics.py constructe the company to NAICS classification dictionary.
process.py use the preprocessed data of above code to do some deep process.

Usage of our code(in python console):

scn.py:
from scn import *
graph1,graph2=rmUnused()
dir_graph1,dir_graph2=rmLoopNew(graph1,graph2)
dictOfCom=CalPos1(dir_graph1,dir_graph2)

process.py:
from process import *
dict_naics2pos_nor,rate=naics2pos()

