""" 
Main Module as comand line interface
"""
import pandas as pd
import sys
import os.path
import numpy as np
import analysisbap
import graphicsbap
import mlbap


actions = ['analys','test','predict','graph']
action = None
ds = None
datasetPath='data/StudentsPerformance.csv'

def main() :
    
    print('=====================================')
    for i in range(6) :
        if(i==3) :
            print('|            StudentBAP             |')
            print('|    Student Background Analysis    |')
            print('|    Coppy right Kamel Haoua 2021   |')
            print('|                                   |')
    print('=====================================')
    
    action = getUserAction()
    if(action==None):
        print('Sorry i can\'t understand your action,! see you next time.')
    elif(action=='exit'):
         exit()
    else:
        executeAction(action)
def loadDataset():
    global ds
    if(os.path.exists(datasetPath)):
        ds= pd.read_csv(datasetPath)
        print('Reading dataset ok')
    else:
        print('file '+datasetPath+' doesn\'t exits. Please check file system and try agin later.' )    

#diplay help
def showHelp():
    print('usage :\n'+ \
    'action [options]\n'+ \
    '\n'+ \
    'Where action is one of the following:\n'+ \
    'analys: perfome all statistical analysis and show result as text\n'+ \
    'graph: display graphic and plts\n'+ \
    'ml: make a pridiction and show features clasification\n'+ \
    'exit: stop script\n')
    
#return user std inpute text
def getUserAction():
    print('What would like to do now.?')
    maxtry=3;
    while(maxtry>0):
        action = input("action: ")
        print(action)
        if(action==None ):
            print ('No action specified!. type help or shoose one action: \n'+', '.join(actions))
            print()
        elif (len( action)==0) :
            print ('No action specified!. type help or shoose one action: \n'+', '.join(actions))
            print()
        elif(action in actions or action=='exit') :
            return action;
        elif(action=='help') :
            showHelp() 
        else:
            print('Not recognized action. "'+action+'"\n'+'type help or choose one action: \n'+', '.join(actions))
            print()
        if(maxtry==0) :
            return None;
        else:
            maxtry-=1;
                
#execute one action                
def executeAction(act=None):
    if(action=='exit') :
        print('Shutting down kernel. good bye.')
        exit()  
    else :  
        loadDataset()
        cleanUpDataset()
        datasetInfos()
        print('executing action: '+act+'\nPlease wait this action may take a while... ')
        
        if (action=='analys'):
            analysis.main()
        elif (action='graph')   
            graphicbap.main() 
        elif (action='ml')   
            mlbap.main() 

# verify dataset

"""
 if there is a missing or wrong value values we have to process each column depending on its data type
 if data type is not numeric we remove the row from dataset, if is nemuric we replace
 non consistence values with NaN and replace NaN values with the mean   of that column
"""

def cleanUpDataset(num_columns=None) :
    print('Process missing and or wrong values..')
    print('--------------------------------------------------------')
    columns= ds.columns
    #some column names contain white-space character, so we have to replace it with underscore character(_)
    print('Correcting columns names..')
    ds.columns=ds.columns.str.replace(' ','_')
    ds.columns=ds.columns.str.replace('\/','_')
    print('Replacing  wrong values with null..')
    if(num_columns==None):
        num_columns=ds.select_dtypes(include='int64')
        print('\n')
        print('Numeric columns are')
        print(num_columns.columns)
        for nc in num_columns :
            ds[nc]=ds[nc].apply(lambda x : np.nan if str(type(x))=="<class 'str'>" else x)
    print('\n')
    print('Collecting columns values with null..')    
    columnWithNullValue=list()
    for column in columns :
        datatype=ds[column].dtype
        print('column '+column+'  data type '+str(datatype))
        if (ds[column].isnull().values.any==True):
            columnWithNullValue.append(column)   
    print('---------------------------------------------------------')
    
    if(len(columnWithNullValue)==0):
        print('columns check finish, ok.')
    else :
        print('some columns have null values\n')
        print(columnWithNullValue)   
    print('Replacing numeric null values with mean')
    replcementValues={}
    if(len(columnWithNullValue)>0) :
        for c in columnWithNullValue :
            if(c in num_columns) :
                meanvalue=ds[c].mean(skipna=True)
                replcementValues[c]=meanvalue
    ds.fillna(value=replcementValues, inplace=True)
    print('Ok, replacement done')
    print('Removing rows with null categorical values')
    ds.dropna(inplace=True)
    print('Ok,  Removing done')
    print('\n')

def datasetInfos() :
    if(os.path.exists(datasetPath)) :
        print('File size')
        print(os.stat(datasetPath).st_size)
    if(ds == None) :
        print('No data available yet !.')
        sys.exit()
    else :    
        print('Dataset shape rows (count x comluns count):')
        print(ds.shape)
        print()
        print('Dolumns names:')
        print(ds.columns)
        print()
        print('Numeric columns:')
        print(ds.select_dtypes(include='int64').columns)
        print()
        print('Statistics:')
        print(ds.describe())

#execute the main program

if __name__ == '__main__':
    main()
