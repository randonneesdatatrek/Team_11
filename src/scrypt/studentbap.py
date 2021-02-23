""" 
Studentbap Main Module as command line interface
"""
import pandas as pd
import sys
import os.path
import numpy as np
import analysisbap
import graphicbap
import mlbap
import testbap

pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 500)


actions = ['analys','graph','test','ml']
action = None
ds = None
dataset_path='data/StudentsPerformance.csv'
env=get_ipython().__class__.__name__
"""
In order to run script from terminal we create this main method in each module
"""
def main() :
    
    print('=====================================')
    for i in range(6) :
        if i==3 :
            print('|            StudentBAP             |')
            print('|    Student Background Analysis    |')
            print('|    Coppy right Kamel Haoua 2021   |')
            print('|                                   |')
    print('=====================================')
    print('Initializing dataset...')
    print()
    load_dataset()
    cleanup_dataset(num_columns = ds[['math score','reading score','writing score']].columns)
    datasetInfos()
    action = get_user_action()
    if ((action == None) or (len(action) == 0)):
        print('Sorry i can\'t understand your action,! see you next time.')
        exit()
    elif action == 'exit':
        return
    else:
        execute_action(action)
"""
Load dataset from path (data/StudentsPerformance.csv)
if file path not exists it stops the execution of script
"""        
def load_dataset():
    global ds
    if (os.path.exists(dataset_path)):
        ds = pd.read_csv(dataset_path)
        print('Reading dataset ok')
    else:
        print('file '+dataset_path+' doesn\'t exits. Please check file system and try agin later.' )    
        return

#display help how to use scripts
def show_help():
    print('usage :\n'+ \
    'action \n'+ \
    '\n'+ \
    'Where action is one of the following:\n'+ \
    'analys: perfom all statistical analysis.\n'+ \
    'graph: display graphics and plots\n'+ \
    'test: run statistical tests\n'+ \
    'ml: make a prediction and show features importance classification\n'+ \
    'exit: stop script\n')
    
#Prompts user for action he wants to perfom and return user std input text
def get_user_action():
    print('Type help or any action.?')
    print()
    maxtry=3;
    while(maxtry>0):
        action = input("action: ")
        if ((action is None) or len(action) == 0 ):
            print ('No action specified!. type help or shoose one action: \n'+', '.join(actions))
            print()
        elif ((action in actions) or (action == 'exit')) :
            return action;
        elif action == 'help' :
            show_help() 
        else:
            print('Unknown action. "'+action+'"\n'+'type help or choose one action: \n'+', '.join(actions))
            print()
        if maxtry == 0 :
            return None;
        else:
            maxtry-=1;
                
#Execute initiation methods and execute one action                
def execute_action(act=None):
    
    if(act=='exit') :
        print('stoping script... good bye.')
        return  
    else :  
        print('executing action: '+str(act)+'\nPlease wait this action may take a while... ')
        if env == 'TerminalInteractiveShell' : # execution from terminal we call secripts main method
            if act=='analys' :
                analysbap.main()
            elif act=='graph' :
                graphicbap.main() 
            elif act=='test' :
                testbap.main() 
            elif act=='ml' :
                mlbap.main()
            else:
                print('Unknown action: ('+str(act)+')')    
        else : # execution from notebook we call methods in this notebook
            if act=='analys' :
                check_data_balancing('gender')
                check_data_balancing('race_ethnicity')
                analysis()
            elif act=='graph' :
                selectGraph() 
            elif act=='test' :
                run_all_tests()
            elif act=='ml' :
                init_ml()
                start_ml()
            else:
                print('Unknown action: ('+str(act)+')')
            

# verify dataset

"""
 if there is a missing or wrong values we have to process each column depending on its data type
 if data type is not numeric we remove the row from dataset, if is nemuric we replace
 non conform values with NaN and replace NaN values with the mean of that column
"""
def cleanup_dataset(num_columns=None) :
    print('Process missing and or wrong values..')
    print('--------------------------------------------------------')
    
    #some column names contain white-space and back slash character, 
    #so we have to replace it with underscore character(_).

    print('Correcting columns names..')
    ds.columns=ds.columns.str.replace(' ','_')
    ds.columns=ds.columns.str.replace('\/','_')
    columns= ds.columns

    print(columns)
    print('Replacing  wrong values with null..')
    if(num_columns is None):
        num_columns=ds.select_dtypes(include='int64')
        print()
                
        for nc in num_columns :
            ds[nc]=ds[nc].apply(lambda x : np.nan if str(type(x))=="<class 'str'>" else x)
    print('\n')
    print('Collecting columns having a null values..')  

    column_with_null_value=list()
    
    for column in columns :
        datatype=ds[column].dtype
        print('column '+column+'  data type '+str(datatype))
        if (ds[column].isnull().values.any==True):
            column_with_null_value.append(column)   
    print('---------------------------------------------------------')
    
    if len(column_with_null_value)==0:
        print('columns check finish, ok.')
    else :
        print('some columns have null values\n')
        print(column_with_null_value)   
    print('Replacing numeric null values with mean')
    replcement_values={}
    if(len(column_with_null_value)>0) :
        for c in column_with_null_value :
            if(c in num_columns) :
                meanvalue=ds[c].mean(skipna=True)
                replcementValues[c]=meanvalue
    ds.fillna(value=replcement_values, inplace=True)
    print('Ok, replacement done')
    print('Removing rows with null categorical values')
    ds.dropna(inplace=True)
    print('Ok,  Removing done')
    print('\n')

"""
Dataset discritption
"""
def datasetInfos() :
    if(os.path.exists(dataset_path)) :
        print('File size: ')
        print(os.stat(dataset_path).st_size)
    if ds is None :
        print('No data available yet !.')
        exit()
    else :    
        print('Dataset shape rows (count x comluns count):')
        print(ds.shape)
        print()
        print('Columns names:')
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

