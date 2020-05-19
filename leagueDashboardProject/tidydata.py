import pandas as pd 
import re

def superMelt(dataFrame, idVariables, mergeValues, variableNames, valueNames):
    for i, columns in enumerate(mergeValues, start=0): 
        dataFrame = pd.melt(dataFrame, id_vars = dataFrame.columns.difference(columns),
                                value_vars=columns, var_name= variableNames[i],
                                value_name=valueNames[i])
        dataFrame[variableNames[i]] = dataFrame[variableNames[i]].str.replace()
    return dataFrame