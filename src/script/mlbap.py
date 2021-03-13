"""
Module Machine learning RandomForestClassifier
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import svm
import sys
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 500)

ds = None

enhanced_ds=False

def main():
    npt=input('Enter 1 for normal dataset or 2 for enhanced dataset:')
    global enhanced_ds
    if npt != None and  npt=='2':
        enhanced_ds=True
    else :
        enhanced_ds=False
        
    init_ml()
    start_ml()

def init_ml() :
    # Set random seed, so it start from 0
    np.random.seed(0)
    
    global targets
    
    """
    if enhanced_ds, create columns to categorise the targets, that contain values form F to A 
    """
    if enhanced_ds:
        ds['math_cat'] = ds.math_score
        ds['math_cat']=ds.math_cat.apply(lambda x:'F' if x<=39.0 else 'E'if x<=49.0 else 'D' if x<=59.0  else 'C' if x<=69.0 \
        else 'B' if x<=79.0  else 'A')
        ds['reading_cat'] = ds.reading_score
        ds['reading_cat']=ds.reading_cat.apply(lambda x:'F' if x<=39.0 else 'E'if x<=49.0 else 'D' if x<=59.0  else 'C' if x<=69.0 \
        else 'B' if x<=79.0  else 'A')
        ds['writing_cat'] = ds.writing_score
        ds['writing_cat']=ds.writing_cat.apply(lambda x:'F' if x<=39.0 else 'E'if x<=49.0 else 'D' if x<=59.0  else 'C' if x<=69.0 \
        else 'B' if x<=79.0  else 'A')
        targets = ds[['math_cat','reading_cat','writing_cat']]
    else:
        targets = ds[['math_score','reading_score','writing_score']]
        
    #split dataset 
    global x_train, x_test, y_train, y_test
    x_train, x_test, y_train, y_test = train_test_split(ds, targets, test_size=0.2, random_state =0)
    
    # preparing features
    gender=x_train['gender'].unique()
    race_ethnicity=x_train['race_ethnicity'].unique()
    parental_level_of_education=x_train['parental_level_of_education'].unique()
    lunch=x_train['lunch'].unique()
    test_preparation_course=x_train['test_preparation_course'].unique()
    #transforming features values from string to numeric
    #ohe=OneHotEncoder(categories=[gender,race_ethnicity,parental_level_of_education,lunch,test_preparation_course])
    global oe
    oe=OrdinalEncoder(categories=[gender,race_ethnicity,parental_level_of_education,lunch,test_preparation_course])
    global train_ds
    global test_ds
    train_ds = x_train[['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']]
    test_ds = x_test[['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']]
    
    #ohe.fit(cat_ds)
    oe.fit(train_ds)
    #OneHotEncoder()
    OrdinalEncoder()
    #features = ohe.transform(train_ds).toarray()
    global features
    features = oe.transform(train_ds)
    #don't use this encoder because it generates more new columns, (see note in introduction)
    #trfm=ohe.transform([['male','group E','some high school','standard','none']]).toarray()
    
    # Training algorithms
    global clf_rf
    global clf_svc
    # initiate random forest algo.
    clf_rf=RandomForestClassifier(n_jobs=2, random_state=0)
    # initiate support vector machine algo. (it does not suport multi-class output)
    clf_svc = svm.SVC(kernel='linear', C=1, random_state=0)


def start_ml():
      
    print('================================================')
    
    task = input('Please type 1 for Prediction or 2 for features importance and hit enter key ↲')
    if task == '2': # task is features importance
        features_importance()
        return
    elif task == '1': # task is prediction
        npt = input('Enter your sample as array of shape (n row of 5 features) or press enter to run sample test data :')
        
        if npt == 'exit':
            return
        elif ((npt is None ) or (len(npt)==0)):# If no data, we use an x_test sample
            for t in targets.columns:
                predict(ftrs=None, target=t)
            return
        elif (len(npt.split(','))%5)!=0: # prediction for user's data
                print('Not valid input, expected input as follow.\n')
                print(', '.join(x_test.head(1)))
                return
        else :
            npt = np.array(npt.split(','))
            row_counts=len(npt)
            npt = npt.reshape(int(row_counts/5), 5)
                                
            data = (pd.DataFrame(npt))
            data = data.apply(lambda f : f.str.strip())
            print(data)
            try:
                for t in targets.columns:
                    predict(ftrs=data,target=t)
            except Exception as e:
                print(e)
                            
    else:# no task 
        print('Not valide choice.')      
        
def features_importance():
    print('-----------------------------------')
    clf_rf=RandomForestClassifier(n_jobs=2, random_state=0)
    clf_rf.fit(np.asarray(features), y_train)
    
    features_importance=clf_rf.feature_importances_
    fi_df=pd.DataFrame(features_importance.reshape(1,5), columns=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course'])

    print('Features importance classification using Random forest classifier')
    print
    print(fi_df)
    print()
    fi_df.plot(kind='bar', xlabel='Features', ylabel='Importance level' ,figsize=[10,10],)
    
    """
    Parameters:
    1) ftrs sample:
    female,group B,bachelor's degree,standard,none,
    male,group C,some college,standard,completed,
    female,group D,master's degree,standard,none
    
    2) target eg.: math_score,
    
    Returns:
    ND Array  of scores 
    """
def predict(ftrs = None, target=None):
            
    print()    
    clf_rf.fit(np.asarray(features), y_train[target])
    clf_svc.fit(np.asarray(features), y_train[target])
   
    global rows_count
    rows_count=200
    global trfm
    if((ftrs is None) or (len(ftrs)==0)):
        trfm=oe.transform(test_ds.head(rows_count))
    else:
        rows_count=len(ftrs.index)
        trfm=oe.transform(ftrs)
    global pred_rfc_df    
    pred_rfc_df=clf_rf.predict(trfm)
    #pred_df=pd.DataFrame(pred_df.reshape(rows_count,3),columns=['math_score','reading_score','writing_score'])
    print()
    print('Prediction for '+target +' using random forest classifier ')
    print(pred_rfc_df)
    
    print('Prediction for '+target +' students using svm support vector machine ')
    print()
    global pred_svm_df
    pred_svm_df=clf_svc.predict(trfm)
    print(pred_svm_df)
    print()
    
    if not enhanced_ds or type(ftrs) != None:
        return
    print('==================================================')
    
    choice = input('Enter 1 for confusion matrix, 2 for alogorithms pefromance score or press enter key to cancle')
    if choice == '1':
        confusion_matrix(target)
    elif choice == '2':
        alogo_pefromance_score(target)
    else:
        return
        
def confusion_matrix(target=None):
    if target is None:
        return
    print('Confusion matrix using random forest classifier for ')
    ct_rfc = pd.crosstab(y_test[target], pred_rfc_df, rownames=['Actual scores'], colnames=['Predicted scores'])
    print(ct_rfc)
    print()
    print('Confusion matrix using svm support vector machine')
    ct_svm = pd.crosstab(y_test[target], pred_svm_df, rownames=['Actual scores'], colnames=['Predicted scores'])
    print(ct_svm)
    
def alogo_pefromance_score(target=None):
    if target is None:
        return
    print('Algorithms perfomance:')
    
    rf_score = clf_rf.score(trfm, y_test[target].head(rows_count))
    svc_score = clf_svc.score(trfm,y_test[target].head(rows_count))
    print()
    print('Algorithms performance scores:')
    print()
    dic={'algorithm':['Random_Forest_Classifier','Support_Vector_Machine'], 'Score':[rf_score,svc_score]}
    print(pd.DataFrame(dic))
    print()
    
    
if __name__=="__main__":
    main()
  