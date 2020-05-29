import pandas as pd 
import numpy as np
import re

def superMelt(dataFrame, idVariables, mergeValues, variableNames, valueNames):
    for i, columns in enumerate(mergeValues, start=0): 
        dataFrame = pd.melt(dataFrame, id_vars = dataFrame.columns.difference(columns),
                                value_vars=columns, var_name= variableNames[i],
                                value_name=valueNames[i])
        stringPattern = re.split('Team.', dataFrame[variableNames[i]][0])[1]                               
        dataFrame[variableNames[i]] = dataFrame[variableNames[i]].str.replace(stringPattern,'')
        dataFrame['Column'] = np.where(dataFrame[variableNames[i]]==dataFrame['Side'], 'True', None)
        dataFrame = dataFrame.dropna().drop(columns = [variableNames[i],'Column'])
    return dataFrame