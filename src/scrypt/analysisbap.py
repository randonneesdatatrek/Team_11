"""
Module analys perfoms statistical Analysis
"""
import sys

import pandas as pd

ds = None


def main():
    check_data_balancing('gender')
    check_data_balancing('race_ethnicity')
    analysis()
    
def check_data_balancing(cat_column=None) :
    print('Data balancing check for column '+cat_column)
    print()
    if cat_column  is None :
        print('None categorical column')
        pass
    
    unique_count = ds[cat_column].nunique()
    ds_size = ds[cat_column].size
    grouped_ds=ds.groupby(by=cat_column)
    normal_count=ds_size/unique_count
    print('Normal count for column '+cat_column+' = '+str(normal_count))
    real_count=grouped_ds.size()
    print('values count in each category '+cat_column)
    print(real_count.to_string())
    is_balanced=True
    
    for count in real_count :
        ratio = count / normal_count
        if (count / normal_count) > 1.1 :
            is_balanced=False
            break
           
    if is_balanced:
         print('Sample for category '+cat_column+' is balanced')
    else:
         print('Sample for category '+cat_column+' is not balanced, ' \
               +'because some group contain more than 90% of the total values of culumn '+cat_column)
    print('---------------------------------------------------')
    
def analysis():
    print('Data analysis')
    if ds is None:
        print('Dataset no available')
        return
    else:
       
        print('Find min / max values')
        print()
        print('Student''s gender who get <= 20% math score')
        ds_less_20=ds[ds['math_score']<=20][['gender','race_ethnicity']] \
              .groupby(by=['race_ethnicity','gender']).size()
        print(pd.DataFrame({'count':ds_less_20}).reset_index())
        print()
        print('Student''s gender who get >=80% math score')
        ds_greater_80=ds[ds['math_score']>=80][['gender','race_ethnicity']]\
              .groupby(by=['race_ethnicity','gender']).size()
        print(pd.DataFrame({'count':ds_greater_80}).reset_index())
        print()
                
        print('Dataset discription:')
        print(ds.describe())
        print()    
        print('Calculating means for each feature...')
        print()
        print('Mean by gender')
        print(ds.groupby(ds['gender']).mean())
        print()
        print('Mean by race/ethnicity')
        print(ds.groupby(ds['race_ethnicity']).mean())
        print()
        print('Mean by parental level of eductaion')
        print(ds.groupby(ds['parental_level_of_education']).mean())
        print()
        print('Mean by lunch')
        print(ds.groupby(ds['lunch']).mean())
        print()
        print('Mean by test preparation course')
        print(ds.groupby(ds['test_preparation_course']).mean())
        print('--------------------------------------------------')

if __name__ == '__main__':
    main()

           