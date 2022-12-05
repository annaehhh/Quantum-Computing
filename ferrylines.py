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