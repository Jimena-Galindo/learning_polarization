# import libraries
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from pathlib import Path
import statsmodels.api as sm
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer
import random

# load the data in long format for each part
part1 = pd.read_csv('data/clean/part1.csv')
all_rounds = pd.read_csv('data/clean/all.csv')
part2 = pd.read_csv('data/clean/part2.csv')
pairs = pd.read_csv('data/clean/pairs.csv')

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

# plot the polarization over time for pairs that were predicted to be polarizrd and pairs that were not
sns.lmplot(data=pairs, x='round_number_modif', y='polarized', 
           x_bins=7, hue='predicted_polarization')

plt.savefig('computed_objects/figures/polarization_rounds_predicted.png')

# Regression with the chosen number of variables (aggregate regression, all subjects and all rounds pooled) 
# to check if the intercepts or the slopes of the two groups are different
# dependent variable: observed polarization
y=pairs['polarized']
# regress on whether it was predicted or not, the round number and the interaction between the two. 
# If the interaction is significant, it means that the slope of the two groups is different
# If the prediction is significant, it means there is more polarization in the predicted pairs
mod = smf.ols(formula='y ~ predicted_polarization+round_number_modif+round_number_modif*predicted_polarization ', data=pairs)

res_predicted = mod.fit(cov_type='HC3')

print(res_predicted.summary())

stargazer = Stargazer([res_predicted], )

with open('computed_objects/tables/regression_predicted_polariz.txt', 'w') as f:
    f.write(stargazer.render_latex())

hypotheses = 'round_number_modif+round_number_modif:predicted_polarization=0'
t_test = res_predicted.t_test(hypotheses)
print(t_test)

with open('computed_objects/tables/ttest_predicted_polariz.txt', 'w') as f:
    f.write(str(t_test.summary()))

# plot the average polarization when predicted and not predicted after 20 rounds of part 2
fig, axs = plt.subplots(figsize=(5, 3))
sns.pointplot(data=pairs[pairs['round_number_modif']>40], x='predicted_polarization', y='polarized', eestimator='mean' , join=False, ax=axs)
axs.set_ylim(.2, .6)
axs.set_xticks([0, 1], ['not predicted', 'predicted'])
axs.set_xlabel('')
axs.set_ylabel('share polarized')
axs.axhline(.5, 0, 1, color = 'grey')
axs.set_title('Polarization after 40 rounds')
fig.savefig('computed_objects/figures/polarization.png')  
