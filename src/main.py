import learning_times as lt
import user_class as us
import matplotlib.pyplot as plt
import numpy as np

def main():
    #Please edit the data location in learning_times and user_classes
    lt.data_location = '../data'
    us.data_location = '../data'
    save_image = True # set True to save images to file
    if save_image: print('Saving graphs...')
    print('Plotting graphs...')
    materials_per_skill = lt.general_analysis(save_image) #getting a kpi and plotting images
    
    #getting percentage_time_deviation
    avg_percent_deviation, language_df, type_df = lt.percent_time_deviation()
    language_df['percent_deviation'] = language_df['percent_deviation']*100
    type_df['percent_deviation'] = type_df['percent_deviation']*100
    
    #plotting the percent deviation by language and type dataframes
    #plotting the percent deviation by language and type dataframes
    _, axes = plt.subplots(nrows=1,ncols=2,figsize=(15,7))
    language_df.plot.bar(x = 'language', y = 'percent_deviation', ax = axes[0], rot = 0)
    type_df.plot.bar(x = 'type', y = 'percent_deviation', ax = axes[1], rot = 0)
    if save_image: plt.savefig('../plots/Deviation_by_type_and_languages.png', dpi = 100)
    
    #Watch_time analysis
    pass_list = []
    percent_list = []
    for i in np.linspace(0,1,11):
        percent_passed, _, _ = lt.watch_analysis(i, i, 5)
        pass_list.append(percent_passed*100)
        percent_list.append(str(int(i*100)))
    
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_axes([0.15,0.15,0.75,0.75])
    ax.bar(percent_list, pass_list, 0.8)
    ax.set_title('People watching specific percent of material duration')
    ax.set_ylabel('Percentage of people')
    ax.set_xlabel('Percentage of watch duration and material content')
    plt.show()
    if save_image: fig.savefig('../plots/People_metric.png', dpi = 100)
    
    # Writing KPIs to a file
    with open('../output_data/KPIs.txt', 'w') as f:
        f.write('Percent time deviations is: '+ str(avg_percent_deviation*100))
        f.write('\n' + str(language_df) +'\n')
        f.write('\n' + str(type_df)+ '\n')
        percent_passed, passed_users, _ = lt.watch_analysis(0.7, 0.7, 5)
        f.write(
'''\nPercentage of users who have more than 
70% of watch duration and completed 70% of their materials: '''
        + str(percent_passed*100))
        f.write('\nNo. of passsed users: '+ str(len(passed_users)))
        f.write('\nAverage required materials per skill: ' + str(materials_per_skill))
        f.write('\nNo. of users who could be potentially cheating: ' + str(len(lt.cheating_list())))
        print('Written to KPI.txt')
        
    with open('../output_data/cheat_list.txt', 'w') as fp:
        for i in lt.cheating_list():
            fp.write(str(i)+'\n')
        print('Written to cheat_list.txt')
        
    
    #creating a json file for user_list
    us.create_json()
    
if __name__ == "__main__":
    main()
else:
    print('Please run the code from main')