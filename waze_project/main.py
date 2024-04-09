""" Project for the end of Get Started With Python glass on coursera from Google. """

import pandas as pd
import numpy as np

#Build a dataframe for the churn dataset
#Examine data type of each column
#Gather descriptive statistics

def load_data(csv_file: str, print_it: bool = False):
    dataframe = pd.read_csv(csv_file, index_col=0)
    if print_it:
        print(dataframe.head(10))
    return dataframe

def find_nulls(df: pd.DataFrame, print_it: bool = False):
        nulls = df[df.isna().any(axis=1)]
        #null_df = df[df['label'].isnull()] #class recommended way to find nulls
        if(print_it):
            print('*** NULLS ***')
            print(nulls.head(10))
            print(nulls.info())

            print('*** STATS ***')
            print(df.describe(include='all'))
            print(nulls.describe(include='all'))
        return nulls


def format_numbers(df: pd.DataFrame):
    df = df.applymap(lambda x: "{:,}".format(x if isinstance(x, (int,float))else x))
    return df

def percent_device(df: pd.DataFrame):
    stats = df.groupby(['device']).agg({'sessions': ['count'], 'total_sessions': ['sum', 'mean'],'activity_days': ['sum', 'mean']})
    stats['percent_device'] = stats['sessions']['count'] / stats['sessions']['count'].sum()
    return stats

def compare(df: pd.DataFrame, nulls: pd.DataFrame, print_all: bool = False, print_stats: bool = True):
    pd.set_option('display.float_format','{:.2f}'.format)

    allstats = percent_device(df)
    temp_df = format_numbers(allstats)
    if print_stats:
        print('*** STATS ***')
        print('DATATFRAME')
        print(allstats)
    if print_all:
        print(df.describe(include='all'))
        print(temp_df)
            
    null_stats = percent_device(nulls)
    temp_null = format_numbers(null_stats)
    if print_stats:
        print('NULLS')
        print(nulls)
    if print_all:
        print(nulls.describe(include='all'))
        print(temp_null)

def nulls_stats(df: pd.DataFrame, print_it: bool = False):
    null_stats = df.groupby(['device']).agg({'sessions': ['count']}).rename(columns={'sessions': 'null_count'})
    null_stats['percent_device'] = null_stats['null_count']['count'] / null_stats['null_count']['count'].sum()
    if print_it:
        print(null_stats.median())
        print(null_stats)
    #alt 
    df['device'].value_counts()
    df['device'].value_counts(normalize=True)

    median_stats = df.groupby(['device'])[['sessions', 'drives', 'n_days_after_onboarding','total_sessions', 'total_navigations_fav1',
                                                    'total_navigations_fav2', 'driven_km_drives','duration_minutes_drives', 'activity_days']].median()
    median_stats['km_per_drive'] = median_stats['driven_km_drives'] / median_stats['drives']
    median_stats['km_per_driving_day'] = median_stats['driven_km_drives'] / median_stats['activity_days']
    print(median_stats['km_per_drive'])
    print(median_stats['km_per_driving_day'])

def nonnulls_stats(df: pd.DataFrame, nulls: pd.DataFrame, print_all: bool = False, print_stats: bool = True):
    merged = df.merge(nulls, indicator='df_merge_info', how='outer') #df_merge_info is a new column that shows where the data came from
    nonnull_only = merged[merged['df_merge_info'] == 'left_only']
    if print_all:
        print('*** MERGED ***')
        print(nonnull_only.info())
    nonnull_stats = df.groupby(['device']).agg({'sessions': ['count']}).rename(columns={'sessions': 'nonnull_count'})
    nonnull_stats['percent_device'] = nonnull_stats['nonnull_count']['count'] / nonnull_stats['nonnull_count']['count'].sum()
    if print_stats:
        print(nonnull_stats)
    

    #df['km_per_drive'] = df['driven_km_drives'] / df['drives']
    #median_drive = df.groupby('label').median(numeric_only=True)[['km_per_drive']]  #cass recommended   
    median_stats = nonnull_only.groupby(['label'])[['sessions', 'drives', 'n_days_after_onboarding','total_sessions', 'total_navigations_fav1',
                                                    'total_navigations_fav2', 'driven_km_drives','duration_minutes_drives', 'activity_days']].median()
    median_stats['km_per_drive'] = median_stats['driven_km_drives'] / median_stats['drives']
    median_stats['km_per_driving_day'] = median_stats['driven_km_drives'] / median_stats['activity_days']
    if print_stats:
        print(median_stats['km_per_drive'])
        print(median_stats['km_per_driving_day'])
   
def main():
    print("*** BEGIN ***")
    dataframe = load_data('waze_project\\waze_dataset.csv', False)
    nulls = find_nulls(dataframe, False)

    compare(dataframe, nulls, False, False)
    
    nulls_stats(nulls, False)
    nonnulls_stats(dataframe, nulls, False)


if __name__ == '__main__':
    main()