# Copyright
#
# Rights, distribution?

# Import necessary packages.
import pandas as pd

###
### Preprocessing
###

# Read .csv file containing information on
#   1. harbour names (from=column1, to=line1)
#   2. shortest ferry connection

df_harbours = pd.read_csv("data_harbours_utf8.csv", sep = ";")


#change format the following columns in dataframe connections
#    1. From
#    2. To
#    3. Distance

#rename 'Column1' to 'From'
df_harbours=df_harbours.rename(columns={'Column1':"From"})

#melt data
df_connections= pd.melt(df_harbours,id_vars=['From'],var_name="To",value_name='Distance')
#print(df_connections.columns)

#filter NaN-values
df_connections=df_connections[df_connections["Distance"].notnull()]
#filter out 0.0 values
df_connections=df_connections[df_connections.Distance != 0]
df_connections=df_connections.reset_index(drop=True)
print(df_connections)

###
###Input
###

#Entering departure and arrival harbour
departure=  input(str("Please enter start harbour:"))
destination= input(str("Please enter destination harbour:"))

#Input validation
# 1. Check whether departure and destination harbour is included in the input data

###
###
###

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector
import dwavebinarycsp

class Ferry:
    def __init__(self):
        self.routes = [
        ["Hamburg"  , "Helgoland", 20],
        ["Hamburg"  , "Romo", 60],
        ["Romo"     , "Esberg", 20],
        ["Helgoland", "Esberg", 10],
        #["Hamburg"  , "London", 10],
        #["Start" , "Hamburg",0],
        #["Esberg", "Ende",0]
        ]
        self.csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
        self.ports = set([])
        self.n=0
        for route in self.routes:
            self.ports.add(route[0])
            self.ports.add(route[1])

    def get_label(self,start, end, length):
        return "{start},{end}{length}".format(**locals())

    def sum_to_two_or_zero(self,*args):
        fromList=[]
        toList=[]
        x = 0
        print(args)
        for a in args:
            if x != self.n:
                toList.append(a)
                x=x+1
            else:
                fromList.append(a)

        sum_value0 = sum(fromList)
        sum_value1 = sum(toList)
        return ((sum_value0 == 1 and sum_value1 == 1) or (sum_value0 == 0 and sum_value1 == 0))

    def get_bqm(self):
        print(self.ports)
        for port in self.ports:
            directions = []
            self.n=0
            for route in self.routes:
                if (route[0]==port):
                    directions.append("to"+self.get_label(route[0],route[1],route[2]))
                self.n = self.n+1
            if (port=="Hamburg"):
                self.n = self.n+1
                directions.append("toStart,Hamburg0")
            if (port=="Esberg"):
                directions.append("fromEnde,Esberg0")
            for route in self.routes:
                if (route[1]==port):
                    directions.append("from"+self.get_label(route[1],route[0],route[2])) 
            self.csp.add_constraint(self.sum_to_two_or_zero, directions)
        print(self.csp.constraints)
        self.csp.add_variable("toStart,Hamburg0")
        self.csp.add_variable
        self.csp.fix_variable("toStart,Hamburg0",1)
        self.csp.fix_variable("fromEnde,Esberg0",1)
        bqm = dwavebinarycsp.stitch(self.csp)
        return bqm


f = Ferry()

bqm=f.get_bqm()

print(bqm.to_polystring())

#sampler = EmbeddingComposite(DWaveSampler())
#result = sampler.sample(bqm,
#                        num_reads=100,
#                        chain_strength=1,
#                        label='Example - Maze')
#
#dwave.inspector.show(result)  