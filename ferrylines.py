# Copyright
#
# Rights, distribution?

# Import necessary packages.
import pandas as pd

###
### Preprocessing
###

# Read .csv file containing information on
#   1. harbour names
#   2. shortest ferry connection

df_harbours = pd.read_csv("data_harbours_utf8.csv")
print(df_harbours.columns)

#change format to the following columns
#    1. from
#    2. to
#    3. shortest direct distance

#from harbours
df_from = df_harbours["Column1"]
df_from.head()

#Input
#Entering departure and arrival harbour
    #start=  input(str("Please enter start harbour:"))
    #end= input(str("Please enter destination harbour:"))

#Input validation
# 1. Check whether start and end harbour is included in the input data