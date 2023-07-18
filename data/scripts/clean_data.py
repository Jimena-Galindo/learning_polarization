import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import scipy as sp
from pathlib import Path
import random

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

# for data in part 2 create a column that indicates the variable that they chose to reveal when they could only reveal one variable
part2.loc[(part2['player.number_variables']==1) & (part2['player.chose_x1']==1), 'single_variable'] = 1
part2.loc[(part2['player.number_variables']==1) & (part2['player.chose_x2']==1), 'single_variable'] = 2
part2.loc[(part2['player.number_variables']==1) & (part2['player.chose_x3']==1), 'single_variable'] = 3
part2.loc[(part2['player.number_variables']==1) & (part2['player.chose_x4']==1), 'single_variable'] = 4
part2.loc[(part2['player.number_variables']==1) & (part2['player.chose_x5']==1), 'single_variable'] = 5

###############
# create a dataframe with all the pairs that played together
###############

# There was an issue in the code when pairs moved on to the second part of the experiment. 
# Not all pairs got the same observations. 
# It had to do with how long some players were waiting for their partners to catch up. 
# So I will filter out all pairs for which this happened.

# get a data table with the pairs and compute wether they are polarized or not. 
# split into player 1 table and player 2 table. 
# Rename the columns to indicate which player it is and merge them to add columns to each group
player1 = all_rounds.loc[all_rounds['player.id_in_group']==1, ['participant.code', 'player.guess', 'player.correct',
                                                               'player.chose_x1', 'player.chose_x2', 'player.chose_x3',
                                                               'player.chose_x4', 'player.chose_x5', 'revealed_variables_count',
                                                               'round_number_modif', 'player.number_variables',
                                                               'group.id_in_subsession', 
                                                               'player.x1', 'player.x2', 'player.x3', 
                                                               'player.x4', 'player.x5', 'player.y', 'session.code']]

player1.rename(columns={'participant.code':'p1_code', 'player.guess':'p1_guess', 'player.correct':'p1_correct', 
                        'player.chose_x1':'p1_chose_x1', 'player.chose_x2':'p1_chose_x2', 'player.chose_x3':'p1_chose_x3', 'player.chose_x4':'p1__chose_x4',
                       'player.chose_x5':'p1_chose_x5', 'player.number_variables':'p1_number_variables', 'revealed_variables_count':'p1_revealed', 
                       'player.x1':'p1_x1', 'player.x2':'p1_x2', 'player.x3':'p1_x3', 'player.x4':'p1_x4', 'player.x5':'p1_x5', 'player.y':'p1_y'}, inplace=True)

player2 = all_rounds.loc[all_rounds['player.id_in_group']==2, ['participant.code', 'player.guess', 'player.correct',
                                                               'player.chose_x1', 'player.chose_x2', 'player.chose_x3',
                                                               'player.chose_x4', 'player.chose_x5', 'revealed_variables_count',
                                                               'round_number_modif', 'player.number_variables',
                                                               'group.id_in_subsession', 
                                                               'player.x1', 'player.x2', 'player.x3', 
                                                               'player.x4', 'player.x5', 'player.y', 'session.code']]


player2.rename(columns={'participant.code':'p2_code', 'player.guess':'p2_guess', 'player.correct':'p2_correct', 
                        'player.chose_x1':'p2_chose_x1', 'player.chose_x2':'p2_chose_x2', 'player.chose_x3':'p2_chose_x3', 'player.chose_x4':'p2_chose_x4',
                       'player.chose_x5':'p2_chose_x5', 'player.number_variables':'p2_number_variables', 'revealed_variables_count':'p2_revealed',
                       'player.x1':'p2_x1', 'player.x2':'p2_x2', 'player.x3':'p2_x3', 'player.x4':'p2_x4', 'player.x5':'p2_x5', 'player.y':'p2_y'}, inplace=True)

# merge the two tables
pairs = player1.merge(player2, on=['group.id_in_subsession', 'round_number_modif', 'session.code'])

# keep only the pairs that got the same observations
pairs[(pairs['p2_x1']==pairs['p1_x1'])&(pairs['p2_x2']==pairs['p1_x2'])&(pairs['p2_x3']==pairs['p1_x3'])&(pairs['p2_x4']==pairs['p1_x4'])]

# create a column that indicates whether the pair is polarized or not
pairs.loc[pairs['p1_guess']!=pairs['p2_guess'], 'polarized']=1
pairs.loc[pairs['p1_guess']==pairs['p2_guess'], 'polarized']=0

# count the number of guesses they got right in the first 20 rounds of part 2
guesses2040 = part2[(part2['subsession.round_number']<=20)].groupby('participant.code').sum()['player.correct']
# add the count column to the all_rounds table
all_rounds = all_rounds.merge(guesses2040, on='participant.code').rename(columns={'player.correct_y':'2040_count', 'player.correct_x':'player.correct'})
# create an indicator for whether they were better than random in the first 20 rounds of part 2
all_rounds.loc[all_rounds['2040_count']>10, 'better_random_2040'] = 1
all_rounds.loc[all_rounds['2040_count']<=10, 'better_random_2040'] = 0

# add the indicator to the part2 table
part2 = part2.merge(guesses2040, on='participant.code').rename(columns={'player.correct_y':'2040_count', 'player.correct_x':'player.correct'})
part2.loc[part2['2040_count']>10, 'better_random_2040'] = 1
part2.loc[part2['2040_count']<=10, 'better_random_2040'] = 0

# add a column that indicates the group in each session
all_rounds.loc[: , 'group_id'] = all_rounds['session.code'] + all_rounds['group.id_in_subsession'].astype(str)
part1.loc[: , 'group_id'] = part1['session.code'] + part1['group.id_in_subsession'].astype(str)
part2.loc[: , 'group_id'] = part2['session.code'] + part2['group.id_in_subsession'].astype(str)

######
# predict polarization
######

# set the parameters of the function that determines the state of the world
#coefficients
a1 = 11
a2 = 6
a3 = 4.5
a4 = 2.4
k = 50.5

# means
m1 = 0
m2 = -10
m3 = 5
m4 = -5

# define a function that predicts the state of the world conditional on the model chosen by the subject. 
# The model chosen is the revealed variables (1) and the non-revealed variables (0) concatenated in a string.

def predict(model, x1, x2, x3, x4):
    # model is a string with 5 characters that indicates if each variable is revealed (1) or not (0)
    # x1, x2, x3, x4 are the realized values of the variables
    if   model == '10000' or model == '10001':
        y_latent = a1*x1+a2*m2+a3*m3+a4*m4+k
        
    elif model == '01000' or model == '01001':
        y_latent = a1*m1+a2*x2+a3*m3+a4*m4+k
        
    elif model == '00100' or model == '00101':
        y_latent = a1*m1+a2*m2+a3*x3+a4*m4+k
    
    elif model == '00010' or model == '00011':
        y_latent = a1*m1+a2*m2+a3*m3+a4*x4+k
        
    elif model == '11000' or model == '11001':
        y_latent = a1*x1+a2*x2+a3*m3+a4*m4+k
        
    elif model == '10100' or model == '10101':
        y_latent = a1*x1+a2*m2+a3*x3+a4*m4+k
    
    elif model == '10010' or model == '10011':
        y_latent = a1*x1+a2*m2+a3*m3+a4*x4+k
    
    elif model == '01100' or model == '01101':
        y_latent = a1*m1+a2*x2+a3*x3+a4*m4+k
        
    elif model == '01010' or model == '01011':
        y_latent = a1*m1+a2*x2+a3*m3+a4*x4+k
        
    elif model == '00110' or model == '00111':
        y_latent = a1*m1+a2*m2+a3*m3+a4*x4+k
        
    elif model == '11100' or model == '11101':
        y_latent = a1*x1+a2*x2+a3*x3+a4*m4+k
        
    elif model == '11010' or model == '11011':
        y_latent = a1*x1+a2*x2+a3*m3+a4*x4+k
    
    elif model == '10110' or model == '10111':
        y_latent = a1*x1+a2*m2+a3*x3+a4*x4+k
        
    elif model == '01110' or model == '01111':
        y_latent = a1*m1+a2*x2+a3*x3+a4*x4+k
        
    elif model == '11110' or model == '11111':
        y_latent = a1*x1+a2*x2+a3*x3+a4*x4+k
        
    else:
        y_latent = random.randint(-1, 1)
        
    if y_latent>= 0:
        predict = 1
    else:
        predict = 0
    
    return predict

# create a column with the prediction of the state of the world for each round by applying the function predict
part2['prediction'] = part2.apply(lambda row : predict(row['model'],
                                                     row['player.x1'],
                                                     row['player.x2'], 
                                                     row['player.x3'], 
                                                     row['player.x4'], ), axis = 1)

# separate the predictions of player 1 from player 2
player2 = part2.loc[part2['player.id_in_group']==2, ['group.id_in_subsession', 'participant.code', 'round_number_modif', 'prediction']]
player1 = part2.loc[part2['player.id_in_group']==1, ['group.id_in_subsession', 'participant.code', 'round_number_modif', 'prediction']]

# rename the codes for merging into a pairs table
player2.rename(columns={'prediction':'p2_prediction', 'participant.code':'p2_code'}, inplace=True)
player1.rename(columns={'prediction':'p1_prediction', 'participant.code':'p1_code'}, inplace=True)

# add the predictions to the pairs table
pairs = pairs.merge(player1, on=['p1_code', 'round_number_modif', 'group.id_in_subsession']).merge(player2, on=['p2_code', 'round_number_modif', 'group.id_in_subsession'])

# determine if the pair is predicted to be polarized or not in the new column 'predicted_polarization'
pairs.loc[pairs['p1_prediction']!=pairs['p2_prediction'], 'predicted_polarization'] = 1
pairs.loc[pairs['p1_prediction']==pairs['p2_prediction'], 'predicted_polarization'] = 0


# Save all the data in clean format

path_p1 = Path('data/clean/part1.csv')  
path_p1.parent.mkdir(parents=True, exist_ok=True)  
part1.to_csv(path_p1)

path_p2 = Path('data/clean/part2.csv')  
path_p2.parent.mkdir(parents=True, exist_ok=True)  
part2.to_csv(path_p2)

path_all = Path('data/clean/all.csv')  
path_all.parent.mkdir(parents=True, exist_ok=True)  
all_rounds.to_csv(path_all)

path_pairs = Path('data/clean/pairs.csv')  
path_pairs.parent.mkdir(parents=True, exist_ok=True)  
pairs.to_csv(path_pairs)
