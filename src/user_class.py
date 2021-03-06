import pandas as pd
import json

class User:
    def __init__(self, user_id, data: pd.DataFrame):
        self.user_id = user_id
        self.data = (data.loc[data['user_id'] == user_id]).drop(columns='user_id')
        self.total_skills = self.data['skill_id'].count()
        self.mastered_skills = self.data['is_mastered'][self.data['is_mastered']==True].count()
        self.list_of_skills = pd.Series(self.data.is_mastered.values, index=self.data.skill_id).to_dict()
        self.mastery_level = 'Beginner'
        if self.total_skills != 0:
            self.mastery_percent = self.mastered_skills/self.total_skills
            if (self.mastery_percent > 0.8):
                self.mastery_level = 'Expert'
            elif (self.mastery_percent< 0.8 and self.mastery_percent > 0.4):
                self.mastery_level = 'Intermediate'
                
        
    def describe(self):
        print("The user id is: " + self.user_id)
        print('Number of total skills: ', self.total_skills)
        print("Number of skills mastered ", self.mastered_skills)
        print('Skill level: ', self.mastery_level)


global data_location
def load_data():
    return (pd.read_csv(data_location + "/material_progress.csv"),
            pd.read_csv(data_location + "/material.csv"),
            pd.read_csv(data_location + "/user_skill.csv"))

def create_json():
    _, _, user_skills = load_data()
    user_id_list = list(user_skills['user_id'].unique())
    user_list_dict = {'user_list': []}
    print('Creating json list of user data')
    
    for user_id in user_id_list:
        user = User(user_id, user_skills)
        data = {
            'user_id': user.user_id,
            'skill_list': user.list_of_skills
            }
        user_list_dict['user_list'].append(data)
    
    with open('../output_data/user_list.json', 'w') as fp:
        json.dump(user_list_dict, fp)
        print('user_list.json created!')
        
if __name__ == '__main__':
    data_location =     data_location = "../data" #Edit location here
    _, _, df_user_data = load_data()
    user_instance = User(df_user_data.iloc[0,0], df_user_data)
    user_instance.describe()
    create_json()
else:
    print('user_class.py loaded')