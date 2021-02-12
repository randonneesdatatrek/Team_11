"""
Module graphics
"""
from matplotlib import pyplot as plt
import seaborn as sns
import sys

#plt.rcParams["figure.figsize"] = [16, 16]
%config InlineBackend.figure_format = 'retina'
sns.set_theme(style="whitegrid")

def main():
  #ask user which graph or print pass
    print('Graphic module')
    graph=input('Please make a choice:\n' \
              +'Enter 1 for categorical variables\n' \
              +'Enter 2 for categorical variables\n' \
              +'Enter 3 for categorical variables\n' \
              +'Enter 4 for categorical variables\n' \
              +'Enter 5 for categorical variables\n' \
              +'Enter 6 for categorical variables\n' )
  
    if (not graph):
        return

    else:
        if (graph=='1'):
            showCategoricalvariables()
        elif (graph=='2') :
            showExtremScores()
        elif (graph=='3') :
            meanGraph()
        elif (graph=='4') :
            boxGraphs()
        elif (graph=='5') :      
            barMeanPerformanceGraph()


def showCategoricalvariables():
    # 1) Categorical variables distribution
    #Gender 
    genders= ds.gender.value_counts(ascending=True).to_dict()
    races= ds.race_ethnicity.value_counts(ascending=True).to_dict()
    
    fig, ax=  plt.subplots(nrows=1,ncols=2, figsize=[12,6])
        
    ax[0].pie(x=genders.values(),data=genders, labels=['']* len(genders.keys()),colors=['blue','hotpink'], autopct='%1.1f%%')
    ax[0].axis('equal')
    ax[0].set_title('Gender')
    ax[0].legend(genders.keys())
    
    #Race/Ethnicity
    ax[1].pie(x=races.values(),data=races, labels=['']* len(races.keys()), autopct='%1.1f%%')
    ax[1].axis('equal')
    ax[1].set_title('Races/Ethnicity')
    ax[1].legend(races.keys())
    
    fig.patch.set_facecolor('white')
    fig.suptitle('Categorical variables distribution',fontsize=16)
    fig.subplots_adjust(top=0.88)
    fig.tight_layout()
    plt.show()
    print('------------------------------------------------------------------------')
    
def showExtremScores():
    fig, ax=  plt.subplots(nrows=3,ncols=2, sharey=False, figsize=[16,16])
    fig.suptitle('Extrem scores grouped by races and divided by gender', fontsize=16)
    # math score
    #------------------------------------------------------------------------------------
    math_less_20=ds.loc[ds['math_score']<=20].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size()
    math_df_20=pd.DataFrame({'counts':math_less_20}).reset_index()
    sns.barplot(ax=ax[0,0],palette=['hotpink','blue'], data=math_df_20, x='race_ethnicity', y='counts',hue='gender')
    ax[0,0].set_title('Under 20 math score')
    
    math_greater_80=ds.loc[ds['math_score']>=80].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size()
    math_df_80=pd.DataFrame({'counts':math_greater_80}).reset_index()
    sns.barplot(ax=ax[0,1],palette=['hotpink','blue'], data=math_df_80, x='race_ethnicity', y='counts',hue='gender')
    ax[0,1].set_title('Above 80 math score')
    
    #--------------------------------------------------------------------------------
    # reding score
    
    read_less_20=ds.loc[ds['reading_score']<=20].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size()
    read_df_20=pd.DataFrame({'counts':read_less_20}).reset_index()
    sns.barplot(ax=ax[1,0],palette=['hotpink','blue'], data=read_df_20, x='race_ethnicity', y='counts',hue='gender')
    ax[1,0].set_title('Under 20 reding score')
    
    read_greater_80=ds.loc[ds['reading_score']>=80].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size()
    read_df_80=pd.DataFrame({'counts':read_greater_80}).reset_index()
    sns.barplot(ax=ax[1,1],palette=['hotpink','blue'], data=read_df_80, x='race_ethnicity', y='counts',hue='gender')
    ax[1,1].set_title('Above 80 reding score')
    
    #--------------------------------------------------------------------------------
    # writing score
    
    write_less_20=ds.loc[ds['writing_score']<=20].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size()
    write_df_20=pd.DataFrame({'counts':write_less_20}).reset_index()
    sns.barplot(ax=ax[2,0],palette=['hotpink','blue'], data=write_df_20, x='race_ethnicity', y='counts',hue='gender')
    ax[2,0].set_title('Under 20 writing score')
    
    write_greater_80=ds.loc[ds['writing_score']>=80].reindex(columns=['gender','race_ethnicity'])\
              .groupby(by=['race_ethnicity','gender']).size()
    write_df_80=pd.DataFrame({'counts':write_greater_80}).reset_index()
    sns.barplot(ax=ax[2,1],palette=['hotpink','blue'], data=write_df_80, x='race_ethnicity', y='counts',hue='gender')
    ax[2,1].set_title('Above 80 writing score')
    
    plt.show()

def meanGraph():
    fig, ax = plt.subplots(nrows=3,ncols=2, sharey=False, figsize=[20,16])
    ax[-1, -1].axis('off')
    fig.suptitle('Means grouped by categorical variables', fontsize=16)
        
    by_gender= ds.groupby(ds['gender']).mean().reset_index()
    by_gender=by_gender.melt('gender',var_name='means',value_name='score_means')
    sns.barplot(ax=ax[0,0], data=by_gender, x='gender', y='score_means',hue='means')
    ax[0,0].set_title('mean by gender')
        
    by_race= ds.groupby(ds['race_ethnicity']).mean().reset_index()
    by_race=by_race.melt('race_ethnicity',var_name='means',value_name='score_means')
    sns.barplot(ax=ax[0,1], data=by_race, x='race_ethnicity', y='score_means',hue='means')
    ax[0,1].set_title('mean by race_ethnicity')
        
    by_ple=ds.groupby(ds['parental_level_of_education']).mean().reset_index()
    by_ple=by_ple.melt('parental_level_of_education',var_name='means',value_name='score_means')
    sns.barplot(ax=ax[1,0], data=by_ple, x='parental_level_of_education', y='score_means',hue='means')
    ax[1,0].set_title('mean by parental_level_of_education')    
       
    by_lunch=ds.groupby(ds['lunch']).mean().reset_index()
    by_lunch=by_lunch.melt('lunch',var_name='means',value_name='score_means')
    sns.barplot(ax=ax[1,1], data=by_lunch, x='lunch', y='score_means',hue='means')
    ax[1,1].set_title('Mean by lunch type')    
       
    by_tpc=ds.groupby(ds['test_preparation_course']).mean().reset_index()
    by_tpc=by_tpc.melt('test_preparation_course',var_name='means',value_name='score_means')
    sns.barplot(ax=ax[2,0], data=by_tpc, x='test_preparation_course', y='score_means',hue='means')
    ax[2,0].set_title('Mean by test_preparation_course') 
    
    plt.show()
    
def boxGraphs():
    fig, ax = plt.subplots(nrows=5, ncols=3, figsize=[30,20])
    fig.suptitle('Grouped by scores', fontsize=16)
        
    sns.boxplot(ax=ax[0,0],y='gender',x='math_score', data=ds, palette=['hotpink','blue'])
    sns.boxplot(ax=ax[0,1],y='gender',x='reading_score', data=ds, palette=['hotpink','blue'])
    sns.boxplot(ax=ax[0,2],y='gender',x='writing_score', data=ds, palette=['hotpink','blue'])
    
    sns.boxplot(ax=ax[1,0],y='race_ethnicity',x='math_score', data=ds)
    sns.boxplot(ax=ax[1,1],y='race_ethnicity',x='reading_score', data=ds)
    sns.boxplot(ax=ax[1,2],y='race_ethnicity',x='writing_score', data=ds)
    
    sns.boxplot(ax=ax[2,0],y='parental_level_of_education',x='math_score', data=ds)
    sns.boxplot(ax=ax[2,1],y='parental_level_of_education',x='reading_score', data=ds)
    sns.boxplot(ax=ax[2,2],y='parental_level_of_education',x='writing_score', data=ds)
    
    sns.boxplot(ax=ax[3,0],y='lunch',x='math_score', data=ds)
    sns.boxplot(ax=ax[3,1],y='lunch',x='reading_score', data=ds)
    sns.boxplot(ax=ax[3,2],y='lunch',x='writing_score', data=ds)
    
    sns.boxplot(ax=ax[4,0],y='test_preparation_course',x='math_score', data=ds)
    sns.boxplot(ax=ax[4,1],y='test_preparation_course',x='reading_score', data=ds)
    sns.boxplot(ax=ax[4,2],y='test_preparation_course',x='writing_score', data=ds)
    
    plt.show() 
    
def barMeanPerformanceGraph():
    fig, ax = plt.subplots(nrows=5, ncols=4, figsize=[40,40])
    plt.xticks(rotation=45)
    fig.suptitle('Mean and perfomances of three exams', fontsize=28)
    
    # Mean
    mean_perormance=ds.eval('(math_score + reading_score + writing_score)/3').rename('mean_perormance')
    sns.barplot(ax=ax[0,0], data=ds,y=mean_perormance , x='gender',palette=['hotpink','blue']).set_title('Mean for all scores', fontsize=18)
    sns.barplot(ax=ax[1,0], data=ds,y=mean_perormance , x='race_ethnicity')
    ple=sns.barplot(ax=ax[2,0], data=ds,y=mean_perormance , x='parental_level_of_education')
    ple.set_xticklabels(ple.get_xticklabels(),rotation=30)
    
    sns.barplot(ax=ax[3,0], data=ds,y=mean_perormance , x='lunch')
    sns.barplot(ax=ax[4,0], data=ds,y=mean_perormance , x='test_preparation_course')
   
    # Math score
    sns.barplot(ax=ax[0,1], data=ds,y='math_score' , x='gender',palette=['hotpink','blue']).set_title('Math score', fontsize=18)
    sns.barplot(ax=ax[1,1], data=ds,y='math_score' , x='race_ethnicity')
    sns.barplot(ax=ax[2,1], data=ds,y='math_score' , x='parental_level_of_education').set_xticklabels(ple.get_xticklabels(),rotation=30)
    sns.barplot(ax=ax[3,1], data=ds,y='math_score' , x='lunch')
    sns.barplot(ax=ax[4,1], data=ds,y='math_score' , x='test_preparation_course')
    
    # Reading score
    sns.barplot(ax=ax[0,2], data=ds,y='reading_score' , x='gender',palette=['hotpink','blue']).set_title('Reading score', fontsize=18)
    sns.barplot(ax=ax[1,2], data=ds,y='reading_score' , x='race_ethnicity')
    sns.barplot(ax=ax[2,2], data=ds,y='reading_score' , x='parental_level_of_education').set_xticklabels(ple.get_xticklabels(),rotation=30)
    sns.barplot(ax=ax[3,2], data=ds,y='reading_score' , x='lunch')
    sns.barplot(ax=ax[4,2], data=ds,y='reading_score' , x='test_preparation_course')
    
    # Writing scores
    sns.barplot(ax=ax[0,3], data=ds,y='writing_score' , x='gender',palette=['hotpink','blue']).set_title('Writing scores', fontsize=18)
    sns.barplot(ax=ax[1,3], data=ds,y='writing_score' , x='race_ethnicity')
    sns.barplot(ax=ax[2,3], data=ds,y='writing_score' , x='parental_level_of_education').set_xticklabels(ple.get_xticklabels(),rotation=30)
    sns.barplot(ax=ax[3,3], data=ds,y='writing_score' , x='lunch')
    sns.barplot(ax=ax[4,3], data=ds,y='writing_score' , x='test_preparation_course')
    
if __name__=="__main__":
    main()  
