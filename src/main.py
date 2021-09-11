import learning_times as lt
import user_class as us
import matplotlib.pyplot as plt
import numpy as np

def main():
    #Please edit the data location in learning_times and user_classes
    
    save_image = True # set True to save images to file
    print('Plotting graphs...')
    materials_per_skill = lt.general_analysis(save_image) #getting a kpi and plotting images
    
    #getting percentage_time_deviation
    avg_percent_deviation, language_df, type_df = lt.percent_time_deviation()
    
    #plotting the percent deviation by language and type dataframes
    language_df.plot.bar(x = 'language', y = 'percent_deviation', rot = 0)
    if save_image: plt.savefig('Deviation_by_language.png', dpi = 100)
    type_df.plot.bar(x = 'type', y = 'percent_deviation', rot = 0)
    if save_image: plt.savefig('Deviation_by_type.png', dpi = 100)
    
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
    if save_image: fig.savefig('People_metric.png', dpi = 100)
    
    # Writing KPIs to a file
    with open('KPI.txt', 'w') as f:
        f.write('Percent time deviations is: '+ str(avg_percent_deviation))
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
    
    #creating a json file for user_list
    us.create_json()
    
if __name__ == "__main__":
    main()
else:
    print('Please run the code from main')