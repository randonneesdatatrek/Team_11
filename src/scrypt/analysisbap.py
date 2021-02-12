"""
Module analys perfoms statistical Analysis
"""
import sys
from scipy.stats import mannwhitneyu
import pandas as pd

"""
check if the data balanced:
In this dataset we have two columns gender and race/ethnicity that are
categorical variable, they should have the same number of values for each category (eg. 500 men and 500 women)
"""
def checkDataBalancing(cat_column=None) :
    if(cat_column==None) :
        print('None categorical column')
        pass
    unique_count = ds[cat_column].nunique()
    ds_size = ds[cat_column].size
    grouped_ds=ds.groupby(by=cat_column)
    normal_count=ds_size/unique_count
    real_count=grouped_ds.size()
    print('values count in each category '+cat_column)
    print(real_count.to_string())
    isBalanced=True
    
    for count in real_count :
        if((count / normal_count) >= 1.1):
            print(count / normal_count)
            isBalanced=False
            break
            
    if(isBalanced==True):
         print('Sample for category '+cat_column+' is balanced')
    else:
         print('Sample for category '+cat_column+' is not balanced,' \
               +'because some '+ cat_column +' contains more than 90% of the total values '+cat_column)
    print()
    
def analysis():
    if(ds is None):
        print('Dataset no available')
        sys.exit()
    else:
       
        # find max min values
        print('Student''s gender who get <= 20% math score')
        print(ds.loc[ds['math_score']<=20].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size())
        print('Student''s gender who get >=80% math score')
        print(ds.loc[ds['math_score']>=80].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size())
        print()
        #mean by gender
        print('analysing dataset please wait...')
        print('-----------------------------------------------------')
        print(ds.describe())
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
        
"""
Running tests for each categorical variable:
We try to find out if there is a correlation between a given category of students
and any of the performances, so we have to filter out a category and compare them 
against each another.
"""

def runtest(dist1,dist2):
    alpha=0.05
    stat,pv= mannwhitneyu(dist1,dist2,alternative='two-sided')
    if(pv<alpha):
        return True
    else:
        return False
    
def runAllTests():
    principal_columns=['math_score','reading_score','writing_score']
    males=ds[ds['gender']=='male'][principal_columns]
    females=ds[ds['gender']=='female'][principal_columns]   
    
    print('---------Gender statitcs test:----------')
    math_test=runtest(males['math_score'],females['math_score'])
    writing_test=runtest(males['reading_score'],females['reading_score'])
    redaing_test=runtest(males['writing_score'],females['writing_score'])
        
    print('Male are '+('good than 'if(math_test)else 'equal with'  )+'females in math ')
    print('Females are '+('good than 'if(writing_test)else 'equal with '  )+'males in writing ')
    print('Females are '+('good than 'if(redaing_test)else 'equal with '  )+'males in reading ')
    print()
    print('---------race_ethnicity statitcs test---------')
    print()
    group_a=ds[ds['race_ethnicity']=='group A'][principal_columns]
    group_b=ds[ds['race_ethnicity']=='group B'][principal_columns]
    group_c=ds[ds['race_ethnicity']=='group C'][principal_columns]
    group_d=ds[ds['race_ethnicity']=='group D'][principal_columns]
    group_e=ds[ds['race_ethnicity']=='group E'][principal_columns]
    
    math_test=runtest(group_e['math_score'],group_d['math_score'])
    writing_test=runtest(group_e['reading_score'],group_d['reading_score'])
    redaing_test=runtest(group_e['writing_score'],group_d['writing_score'])
    
    print('Group E vs group D:')
    
    print('group E is '+('good than 'if(math_test)else 'similar with'  )+'group D in math ')
    print('group E is '+('good than 'if(writing_test)else 'equal with '  )+'group D in writing ')
    print('group E is '+('good than 'if(redaing_test)else 'equal with '  )+'group D in reading ') 
    print()
    print('Group D vs group C:')
    math_test=runtest(group_d['math_score'],group_c['math_score'])
    writing_test=runtest(group_d['reading_score'],group_c['reading_score'])
    redaing_test=runtest(group_d['writing_score'],group_c['writing_score'])
    
    print('group D is '+('good than 'if(math_test)else 'similar with'  )+'group C in math ')
    print('group D is '+('good than 'if(writing_test)else 'similar with '  )+'group C in writing ')
    print('group D is '+('good than 'if(redaing_test)else 'similar with '  )+'group C in reading ')
    print()
    print('---------Parental level of education---------')
    print()
    bachelor_degree=ds[ds['parental_level_of_education']=='bachelor''s degree'][principal_columns]
    master_degree=ds[ds['parental_level_of_education']=='master''s degree'][principal_columns]
    ass_degree=ds[ds['parental_level_of_education']=='associate''s degree'][principal_columns]
    somme_college=ds[ds['parental_level_of_education']=='some college'][principal_columns]
    high_school=ds[ds['parental_level_of_education']=='high school'][principal_columns]
    somme_high_school=ds[ds['parental_level_of_education']=='some high school'][principal_columns]
    
    print('bachelor degree vs master degree:')
    math_test=runtest(bachelor_degree['math_score'],master_degree['math_score'])
    writing_test=runtest(bachelor_degree['reading_score'],master_degree['reading_score'])
    redaing_test=runtest(bachelor_degree['writing_score'],master_degree['writing_score'])
    print('master degree is '+('good than 'if(math_test)else 'similar with'  )+'bachelor degree in math ')
    print('master degree is '+('good than 'if(writing_test)else 'similar with '  )+'bachelor degree in writing ')
    print('master degree is '+('good than 'if(redaing_test)else 'similar with '  )+'bachelor degree in reading ')
    print()
    
    print('associate degree vs some college:')
    math_test=runtest(ass_degree['math_score'],somme_college['math_score'])
    writing_test=runtest(ass_degree['reading_score'],somme_college['reading_score'])
    redaing_test=runtest(ass_degree['writing_score'],somme_college['writing_score'])
    print('associate degree is '+('good than 'if(math_test)else 'similar with'  )+'some college in math ')
    print('associate degree is '+('good than 'if(writing_test)else 'similar with '  )+'some college in writing ')
    print('associate degree is '+('good than 'if(redaing_test)else 'similar with '  )+'some college in reading ')
    print()
    
    print('some high school vs high school:')
    math_test=runtest(high_school['math_score'],somme_high_school['math_score'])
    writing_test=runtest(high_school['reading_score'],somme_high_school['reading_score'])
    redaing_test=runtest(high_school['writing_score'],somme_high_school['writing_score'])
    print('some high school is '+('good than 'if(math_test)else 'similar with '  )+'high school in math ')
    print('some high school is '+('good than 'if(writing_test)else 'similar with '  )+'high school in writing ')
    print('some high school is '+('good than 'if(redaing_test)else 'similar with '  )+'high school in reading ')
    print()
           