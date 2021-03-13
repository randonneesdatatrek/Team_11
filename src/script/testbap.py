"""
Running tests for each categorical variable:
We try to find out if there is a correlation between a given category of students
and any of the performances, so we have to filter out a category and compare them 
against each another.
"""
from scipy.stats import mannwhitneyu
import scipy.stats as stats
import pandas as pd

ds = None


def main():
    run_all_tests()
    
def run_2ways_test(dist1,dist2):
    alpha = 0.05
    stat,pv = mannwhitneyu(dist1,dist2,alternative='two-sided')
    return pv < alpha
    
def run_all_tests():
    principal_columns=['math_score','reading_score','writing_score']
    
    males=ds[ds['gender']=='male'][principal_columns]
    females=ds[ds['gender']=='female'][principal_columns]   
    
    group_a=ds[ds['race_ethnicity']=='group A'][principal_columns]
    group_b=ds[ds['race_ethnicity']=='group B'][principal_columns]
    group_c=ds[ds['race_ethnicity']=='group C'][principal_columns]
    group_d=ds[ds['race_ethnicity']=='group D'][principal_columns]
    group_e=ds[ds['race_ethnicity']=='group E'][principal_columns]
    
    bachelor_degree=ds[ds['parental_level_of_education']=='bachelor''s degree'][principal_columns]
    master_degree=ds[ds['parental_level_of_education']=='master''s degree'][principal_columns]
    ass_degree=ds[ds['parental_level_of_education']=='associate''s degree'][principal_columns]
    somme_college=ds[ds['parental_level_of_education']=='some college'][principal_columns]
    high_school=ds[ds['parental_level_of_education']=='high school'][principal_columns]
    somme_high_school=ds[ds['parental_level_of_education']=='some high school'][principal_columns]
    
    
    
    print('---------Running  two-ways test:----------')
    print()
    print('---------Gender test:----------')
    print()
    math_test=run_2ways_test(males['math_score'],females['math_score'])
    writing_test=run_2ways_test(males['reading_score'],females['reading_score'])
    redaing_test=run_2ways_test(males['writing_score'],females['writing_score'])
    
    print('Male are '+('good than 'if math_test else 'equal with'  )+'females in math ')
    print('Females are '+('good than 'if writing_test else 'equal with '  )+'males in writing ')
    print('Females are '+('good than 'if redaing_test else 'equal with '  )+'males in reading ')
        
    print()
    print('---------Race/Ethnicity ---------')
    print()
    math_test=run_2ways_test(group_e['math_score'],group_d['math_score'])
    writing_test=run_2ways_test(group_e['reading_score'],group_d['reading_score'])
    redaing_test=run_2ways_test(group_e['writing_score'],group_d['writing_score'])
    
    print('Group E vs group D:')
    
    print('group E is '+('good than 'if math_test else 'similar with'  )+'group D in math ')
    print('group E is '+('good than 'if writing_test else 'similar with '  )+'group D in writing ')
    print('group E is '+('good than 'if redaing_test else 'similar with '  )+'group D in reading ') 
    print()
    print('Group D vs group C:')
    math_test=run_2ways_test(group_d['math_score'],group_c['math_score'])
    writing_test=run_2ways_test(group_d['reading_score'],group_c['reading_score'])
    redaing_test=run_2ways_test(group_d['writing_score'],group_c['writing_score'])
    
    print('group D is '+('good than 'if math_test else 'similar with'  )+'group C in math ')
    print('group D is '+('good than 'if writing_test else 'similar with '  )+'group C in writing ')
    print('group D is '+('good than 'if redaing_test else 'similar with '  )+'group C in reading ')
    print()
    print('---------Parental level of education test ---------')
    print()
   
    print('bachelor degree vs master degree:')
    math_test=run_2ways_test(bachelor_degree['math_score'],master_degree['math_score'])
    writing_test=run_2ways_test(bachelor_degree['reading_score'],master_degree['reading_score'])
    redaing_test=run_2ways_test(bachelor_degree['writing_score'],master_degree['writing_score'])
    print('master degree is '+('good than 'if math_test else 'similar with'  )+'bachelor degree in math ')
    print('master degree is '+('good than 'if writing_test else 'similar with '  )+'bachelor degree in writing ')
    print('master degree is '+('good than 'if redaing_test else 'similar with '  )+'bachelor degree in reading ')
    print()
    
    print('associate degree vs some college:')
    math_test=run_2ways_test(ass_degree['math_score'],somme_college['math_score'])
    writing_test=run_2ways_test(ass_degree['reading_score'],somme_college['reading_score'])
    redaing_test=run_2ways_test(ass_degree['writing_score'],somme_college['writing_score'])
    print('associate degree is '+('good than 'if math_test else 'similar with'  )+'some college in math ')
    print('associate degree is '+('good than 'if writing_test else 'similar with '  )+'some college in writing ')
    print('associate degree is '+('good than 'if redaing_test else 'similar with '  )+'some college in reading ')
    print()
    
    print('some high school vs high school:')
    math_test=run_2ways_test(high_school['math_score'],somme_high_school['math_score'])
    writing_test=run_2ways_test(high_school['reading_score'],somme_high_school['reading_score'])
    redaing_test=run_2ways_test(high_school['writing_score'],somme_high_school['writing_score'])
    print('some high school is '+('good than 'if math_test else 'similar with '  )+'high school in math ')
    print('some high school is '+('good than 'if writing_test else 'similar with '  )+'high school in writing ')
    print('some high school is '+('good than 'if redaing_test else 'similar with '  )+'high school in reading ')
    print()
    
    print()
    print('---------Running  one-ways ANOVA test (black box test):----------')
    print()
    print('---------race_ethnicity test---------')
    print()
    
    f,p =stats.f_oneway(group_a, group_b, group_c, group_d ,group_e)
    dic={'scores':principal_columns, 'F values':f, 'P values':p, 'it\'s ok':f>p}
    print(pd.DataFrame(dic))
    print()
    
if __name__ == '__main__':
    main()
