
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    data_location = "/media/NV/Edyoucated_Data_Science/data" #Edit location here
    return (pd.read_csv(data_location + "/material_progress.csv"),
            pd.read_csv(data_location + "/material.csv"),
            pd.read_csv(data_location + "/user_skill.csv"))


# finds the watchtime with the time_factor 
# as a factor for upper bound of the watchtime
def  watchtime_finder(time_factor):
    df_material_progress, df_material, _ = load_data()
    df_material_progress['watch_duration'] = (
        pd.to_datetime(df_material_progress['finished_at'])-
        pd.to_datetime(df_material_progress['started_at'])) / np.timedelta64(1,'m')
    new_df = pd.merge(df_material_progress, df_material, on = 'material_id')
    #Here I got the times which were in several days for a single material. 
    #So, to filter such errors I created an upper bound which is five times
    #the estimated time of a material
    new_df['watch_duration'] = np.where((new_df['watch_duration'] <= time_factor
                                        * new_df['duration_minutes']), 
                                        new_df['watch_duration'], np.nan)
    return new_df


#returns percentage time deviation, by language and by type
def percent_time_deviation(time_factor = 5):
    _, df_material, _ = load_data()
    df_material_progress = watchtime_finder(time_factor)
    df_time_diff_by_material = df_material_progress.groupby(
        'material_id',as_index=False)['watch_duration'].mean()
    new_df = pd.merge(df_time_diff_by_material, df_material, on = 'material_id')
    
    #deviation method
    new_df['percent_deviation'] = ((new_df['watch_duration'] 
                                    - new_df['duration_minutes'])
                                   /new_df['duration_minutes']).abs()
    
    df_by_language = new_df.groupby(
        'language', as_index=False)['percent_deviation'].mean()
    df_by_type = new_df.groupby(
        'type', as_index=False)['percent_deviation'].mean()
    return (np.nanmean(new_df['percent_deviation'].to_numpy()), 
            df_by_language, df_by_type)
 

#returns a percentage of users who passed the analysis and a list of failed users    
def watch_analysis( watch_percent = 0.5, material_percent = 0.5, time_factor = 5):
    _, df_material, df_user_skill = load_data()
    df_material_progress = watchtime_finder(time_factor)
    #new_df = pd.merge(df_material_progress, df_material, on = 'material_id')
    new_df = df_material_progress
    new_df['is_watched'] = (new_df['watch_duration'] 
                            >= watch_percent * new_df['duration_minutes'])
    new_df_by_users = new_df.groupby('user_id', as_index=False)['is_watched'].mean()
    passed_users = (new_df_by_users[new_df_by_users['is_watched'] 
                                    >= material_percent])['user_id'].to_list()
    failed_users = (new_df_by_users[new_df_by_users['is_watched'] 
                                    < material_percent])['user_id'].to_list()
    total_users = new_df_by_users['user_id'].count()
    if total_users != 0:
        return len(passed_users)/total_users, passed_users, failed_users
    else:
        return 0, passed_users, failed_users

#reports the graph of the current data and returns average materials required per skill
def general_analysis(save_image = False):
    df_material_progress, df_material, user_skills = load_data()
    
    #df_material_progress
    by_user = df_material_progress.groupby(
        'user_id', as_index=False)['material_id'].count()
    by_material = df_material_progress.groupby(
        'material_id', as_index=False)['user_id'].count()
    avg_materials_per_user = by_user['material_id'].mean()
    avg_users_per_material = by_material['user_id'].mean()
    
    #df_material
    by_type = df_material.groupby('type', as_index=False)['material_id'].count()
    by_type = by_type.rename(columns = {
        'type' : 'Number_of_types', 'material_id': 'type_count'})
    by_language = df_material.groupby('language', as_index=False).count()
    by_language = by_language.rename(columns = {
        'language': 'Number_of_languages', 'material_id': 'language_count'})
    short = df_material['material_id'][(df_material['duration_minutes']<4)].nunique()
    medium = df_material['material_id'][
        (df_material['duration_minutes']>=4) &
        (df_material['duration_minutes']<=10)].nunique()
    long = df_material['material_id'][(df_material['duration_minutes']>10)].nunique()
    
        #user_skills
    df_by_user_id = user_skills.groupby('user_id', as_index=False)['is_mastered'].sum()
    df_by_skill_id = user_skills.groupby('skill_id', as_index=False)['is_mastered'].sum()
    avg_skills_by_per_user = df_by_user_id['is_mastered'].mean()
    avg_users_per_skill = df_by_skill_id['is_mastered'].mean()
    
    
    #prints
    plt.figure(figsize=(8, 4))
    by_type.plot.bar(x = 'Number_of_types', y = 'type_count', rot = 0)
    if save_image: plt.savefig('../plots/Number_of_types.png', dpi = 100)
    
    plt.figure(figsize=(5, 5))
    by_language.plot.bar(x = 'Number_of_languages', y = 'language_count', rot = 0)
    if save_image: plt.savefig('../plots/Number_of_languages.png', dpi = 100)
    
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_axes([0.15,0.15,0.75,0.75])
    ax.bar(['Short', 'Medium', 'Long'], [short, medium, long], 0.8)
    ax.set_title('Material_duration')
    plt.show()
    if save_image: fig.savefig('../plots/Material_duration.png', dpi = 100)
    
    plt.figure(figsize=(5, 5))
    plt.bar(['Average no. of materials \n consumed by per user',
             'Average no. of skills \n mastered by per user'],
            [avg_materials_per_user, avg_skills_by_per_user])
    if save_image: plt.savefig('../plots/Per_user_index.png', dpi = 100)
    
    plt.figure(figsize=(5, 5))
    plt.bar(['Average no. of users \n consuming a material',
             'Average no. of users \n mastering a skill'],
            [avg_users_per_material, avg_users_per_skill])
    if save_image: plt.savefig('../plots/Average_user_index.png', dpi = 100)
    
    if (avg_skills_by_per_user != 0):
        return avg_materials_per_user/avg_skills_by_per_user
    else:
        return 0
    
    
    
#returns a list of user_ids of possible cheaters
def cheating_list():
    _, _, failed_users = watch_analysis(0.1, 0.1, 5)
    _, _, user_skills = load_data()
    filtered_users = user_skills[user_skills['user_id'].isin(failed_users)]
    mean_mastery_df = filtered_users.groupby('user_id', as_index=False)['is_mastered'].mean()
    cheat_users = mean_mastery_df['user_id'][mean_mastery_df['is_mastered'] >= 0.7].tolist() 
    return cheat_users
 

# I tried using for loop but it was slow so I did it with another way   
'''
def watchtime_finder(time_factor):
    df_material_progress, df_material, _ = load_data()
    time_diff_ls = []
    for material_id, start_time, finish_time in df_material_progress[
            ['material_id','started_at','finished_at']].to_numpy():
        estimated_time_minutes = df_material[
            'duration_minutes'].loc[df_material['material_id'] == material_id].values
        estimate_times_seconds = estimated_time_minutes * 60
        time_diff = 0
        try:
            st = datetime.fromisoformat(str(start_time))
            ft = datetime.fromisoformat(str(finish_time))
            time_diff = (ft - st).total_seconds()
        except:
            time_diff = 0
            pass
        if(time_diff < time_factor * estimate_times_seconds and time_diff > 0):
            time_diff_ls.append(time_diff / 60)
        else:
            time_diff_ls.append(0)
    df_material_progress['watch_duration'] = time_diff_ls
    return df_material_progress
'''

if __name__ == '__main__':
    print('Percent time deviations are:\n', percent_time_deviation())
    percent_passed, passed_users, _ = watch_analysis(0.7, 0.7, 5)
    print(
'''Percentage of users who have more than 
70% of watch duration and completed 70% of their materials '''
        , percent_passed*100)
    print('No. of passsed users ', len(passed_users))
    print('Average required materials per skill:', general_analysis())
    print('No. of users who could be potentially cheating', len(cheating_list()))
else:
    print('learning_times.py loaded')
























