"""
Module Machine learning RandomForestClassifier
"""
# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
import sys
# Load pandas
import pandas as pd
# Load numpy
import numpy as np
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 500)

def main():
  print('Machine learning using RandomForestClassifier\n')
  print('================================================')
  npt=input('Enter your sample as array of shape (1,5) or press enter to rutn a test sample:')
  if (not npt ):
    return
  elif (npt=='exit'):
    return 
  npt=np.array(npt.split(','))
  if len(npt)>5:
    print('For instance we can only make prediction fro one student.')
    return
  npt=npt.reshape(1,5)
  data=(pd.DataFrame(npt))
  
  predict(data)
  featuresImportance()

  # Set random seed, so it start from 0
  np.random.seed(0)
  # 1) math_score machine learning
  target = ds[['math_score','reading_score','writing_score']]
  #split dataset 
  x_train, x_test, y_train, y_test= train_test_split(ds,target,test_size=0.2, random_state =0)
  # preparing features
  gender=x_train['gender'].unique()
  race_ethnicity=x_train['race_ethnicity'].unique()
  parental_level_of_education=x_train['parental_level_of_education'].unique()
  lunch=x_train['lunch'].unique()
  test_preparation_course=x_train['test_preparation_course'].unique()
  #transforming features values from string to numeric
  #ohe=OneHotEncoder(categories=[gender,race_ethnicity,parental_level_of_education,lunch,test_preparation_course])
  oe=OrdinalEncoder(categories=[gender,race_ethnicity,parental_level_of_education,lunch,test_preparation_course])
  global train_ds
  global test_ds
  train_ds = x_train[['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']]
  test_ds=x_test[['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']]
  
  #ohe.fit(cat_ds)
  oe.fit(train_ds)
  #OneHotEncoder()
  OrdinalEncoder()
  #features = ohe.transform(train_ds).toarray()
  features = oe.transform(train_ds)
  #trfm=ohe.transform([['male','group E','some high school','standard','none']]).toarray()
  """
  This is a sample to predict scores 
  trfm=oe.transform([['male','group E','some high school','standard','none'],\
                   ['female','group E','some high school','standard','none'],\
                   ['male','group C','some high school','standard','none'],\
                   ['female','group C','some high school','standard','none']])
  """

  clf=RandomForestClassifier(n_jobs=2, random_state=0)
  clf.fit(np.asarray(features),y_train)
  
def featuresImportance():
  features_importance=clf.feature_importances_
  fi_df=pd.DataFrame(features_importance.reshape(1,5),columns=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course'])

  print('features importance')
  
  print(fi_df)
  print()
  fi_df.plot(kind='bar', xlabel='Features', ylabel='Importance level' ,figsize=[10,10],)

def predict(ftrs=None):
   
   rows_count=10 
   if(ftrs is None):
     trfm=oe.transform(test_ds.head(rows_count))
   else:
     rows_count=len(ftrs.index)
     trfm=oe.transform(ftrs)

   pred=clf.predict(trfm)
   pred_df=pd.DataFrame(pred.reshape(rows_count,3),columns=['math_score','reading_score','writing_score'])
   print('prediction for ('+str(rows_count) +') students')
   print(pred_df)
   print('-------------------------------------------')

if __name__=="__main__":
  main()
  