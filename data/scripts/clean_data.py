import pandas as pd
import numpy as np
import scipy as sp
from pathlib import Path

# load the data in long format for each part
part1 = pd.read_csv('data/raw/Part1_2023-06-05.csv')
part2 = pd.read_csv('data/raw/Part2_2023-06-05.csv')
part1_day2 = pd.read_csv('data/raw/Part1_2023-06-08_1.csv')
part2_day2 = pd.read_csv('data/raw/Part2_2023-06-08_1.csv')


# I had to reset the database after adding more rounds so there are two different cumulative data sets. The first has only the first 2 sessions
part1 = part1.merge(part1_day2, how='outer')
part2 = part2.merge(part2_day2, how='outer')
part1 = part1.loc[part1['session.is_demo']==0]
part2 = part2.loc[part2['session.is_demo']==0]

# Check the number of subjects
print('Number of subjects in part 1 is ' + str(len(part1['participant.code'].unique())))
print('Number of subjects in part 2 is ' + str(len(part2['participant.code'].unique())))

# Create a column in which the round number is consistent across all parts (part 2 starts from round 2 again)
part2.loc[:, 'round_number_modif'] = part2.loc[:, 'subsession.round_number']+20
part1.loc[:, 'round_number_modif'] = part1.loc[:, 'subsession.round_number']

# for part 1 create th ecolumn for 'player.number_variables' and set it to 5 since all subjects saw all 5 variables in those rounds
part1.loc[:, 'player.number_variables'] = 5
part1.loc[:, 'revealed_variables_count'] = 5

# for part 2 count the number of variables that subjects actually revealed in each round
part2.loc[:, 'revealed_variables_count'] = part2.loc[:, 'player.chose_x1']+ part2.loc[:, 'player.chose_x2']+part2.loc[:, 'player.chose_x3']+part2.loc[:, 'player.chose_x4']+part2.loc[:, 'player.chose_x5']

# Create a column that indicates the model chosen. It is a string of the indicators of having chosen each of the variables
# function that concatenates the indicators as strings into one string with 5 characters in it
def models(x1, x2, x3, x4, x5):
    return str(x1)+str(x2)+str(x3)+str(x4)+str(x5)

# applty the function to all rows of the data in part 2    
part2['model'] = part2.apply(lambda row : models(row['player.chose_x1'],
                                                 row['player.chose_x2'], 
                                                 row['player.chose_x3'], 
                                                 row['player.chose_x4'], 
                                                 row['player.chose_x5']), axis = 1)

# merge part 1 and part 2 into a single table
all_rounds=part1.merge(part2, how='outer')

# Create an indicator for each number of variables assigned
part2['indic_1'] = 0
part2['indic_2'] = 0
part2['indic_3'] = 0
part2['indic_4'] = 0
part2['indic_5'] = 0

part2.loc[part2['player.number_variables']==1, 'indic_1'] = 1
part2.loc[part2['player.number_variables']==2, 'indic_2'] = 1
part2.loc[part2['player.number_variables']==3, 'indic_3'] = 1
part2.loc[part2['player.number_variables']==4, 'indic_4'] = 1
part2.loc[part2['player.number_variables']==5, 'indic_5'] = 1

path_p1 = Path('data/clean/part1.csv')  
path_p1.parent.mkdir(parents=True, exist_ok=True)  
part1.to_csv(path_p1)

path_p2 = Path('data/clean/part2.csv')  
path_p2.parent.mkdir(parents=True, exist_ok=True)  
part2.to_csv(path_p2)

path_all = Path('data/clean/all.csv')  
path_all.parent.mkdir(parents=True, exist_ok=True)  
all_rounds.to_csv(path_all)
