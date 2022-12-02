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

df_harbours = pd.read_csv("data_harbours.csv")
print(df_harbours.head())

#Input
#Entering departure and arrival harbour
    #start=  input(str("Please enter start harbour:"))
    #end= input(str("Please enter destination harbour:"))

#Input validation
# 1. Check whether start and end harbour is included in the input data