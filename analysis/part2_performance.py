# this script sorts subjects by their performance in the first 20 rounds of part 2 (rounds 20 to 40 in the aggregate)
# and plots the effect of revealing/allowing an additional variable.

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from pathlib import Path
import statsmodels.api as sm
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer

# load the data in long format for each part
part1 = pd.read_csv('data/clean/part1.csv')
all_rounds = pd.read_csv('data/clean/all.csv')
part2 = pd.read_csv('data/clean/part2.csv')

# count the number of guesses they got right in the first 20 rounds of part 2
guesses2040 = part2[(part2['subsession.round_number']<=20)].groupby('participant.code').sum()['player.correct']
# add the count column to the all_rounds table
all_rounds = all_rounds.merge(guesses2040, on='participant.code').rename(columns={'player.correct_y':'2040_count', 'player.correct_x':'player.correct'})
# create an indicator for whether they were better than random in the first 20 rounds of part 2
all_rounds.loc[all_rounds['2040_count']>10, 'better_random_2040'] = 1
all_rounds.loc[all_rounds['2040_count']<=10, 'better_random_2040'] = 0
# plot the performance across all rounds by performance in the first 20 rounds of part 2
sns.lmplot(data=all_rounds[all_rounds['round_number_modif']<=60], x="round_number_modif", y="player.correct", x_bins=10, hue='better_random_2040')
plt.savefig('computed_objects/figures/p2_correct_rounds.png')

# add the indicator to the part2 table
part2 = part2.merge(guesses2040, on='participant.code').rename(columns={'player.correct_y':'2040_count', 'player.correct_x':'player.correct'})
part2.loc[part2['2040_count']>10, 'better_random_2040'] = 1
part2.loc[part2['2040_count']<=10, 'better_random_2040'] = 0

# Accuracy wrt number of variables that they chose to reveal and by performance in part2
fig, axs = plt.subplots()
axs = sns.pointplot(data=part2, x='revealed_variables_count', y='player.correct', hue='better_random_2040', eestimator='mean', join=False)
axs.set_ylim(.35, .75)

axs.axhline(.5, 0, 1, color = 'grey')
axs.set_xlabel('number of revealed variables')
axs.set_ylabel('share of correct guesses')

fig.savefig('computed_objects/figures/p2_performance_effect_revealed.png')

# Accuracy wrt number of variables that they were allowed to choose and by performance in part2
fig, axs = plt.subplots()
axs = sns.pointplot(data=part2[part2['subsession.round_number']>0], x='player.number_variables', y='player.correct', 
                    hue='better_random_2040', eestimator='mean', join=False)
plt.ylim(.35, .75)

plt.axhline(.5, 0, 1, color = 'grey')
axs.set_xlabel('number of allowed variables')
axs.set_ylabel('share of correct guesses')


fig.savefig('computed_objects/figures/p2_performance_effect_allowed.png')

# count the number of subjects in each of the groups
better_random_count = len(all_rounds.loc[all_rounds['better_random_2040']==1, 'participant.code'].unique())
N = len(all_rounds['participant.code'].unique())

share_better_random = better_random_count/N

print('the number of subjects who do better than random in rounds 20 - 40 is ' + str(better_random_count))

print('the number of subjects who do random or worse in rounds 20 - 40  is ' + str(N - better_random_count))

print('the share of subjects who do better than random in rounds 20 - 40 is ' + str(share_better_random))


# Accuracy wrt choosen model conditional on the number of variables they were allowed to choose by group in part 2 for 
# one variable models and two variable models
fig, axs = plt.subplots(2, 1, figsize=(10, 7))
sns.pointplot(data=part2[(part2['player.number_variables']==1) & (part2['subsession.round_number']>20)], x='model', y='player.correct', 
              hue='better_random_2040', eestimator='mean', join=False, ax=axs[0])
axs[0].set_ylim(0, 1)
axs[0].set_title('performance by models with 1 variable chosen (after 40 rounds)')
axs[0].axhline(.5, 0, 1, color = 'grey')

sns.pointplot(data=part2[(part2['player.number_variables']==2) & (part2['subsession.round_number']>20)], x='model', y='player.correct', 
              hue='better_random_2040', eestimator='mean', join=False, ax=axs[1])
axs[1].set_ylim(0, 1)
axs[1].set_title('performance by models with 1 variable chosen (after 40 rounds)')
axs[1].axhline(.5, 0, 1, color = 'grey')

fig.savefig('computed_objects/figures/p2_performance_by_model.png')


# aggregate with treatment assignment only (no random effects) for the better than random group
y=part2.loc[part2['better_random_2040']==1,'player.correct']
part2['round'] = part2['subsession.round_number']

mod = smf.ols(formula='y ~ indic_1 + indic_2+ indic_3 + indic_4 + indic_5  - 1', data=part2[part2['better_random_2040']==1])

res_assigned = mod.fit(cov_type='HC3')

print(res_assigned.summary())

stargazer = Stargazer([res_assigned], )

stargazer.render_latex()

# For the regression using assignment to treatment directly for the better than random group
# test that 1 variable makes the guesses better than random, and whether adding an extra variable is helpful or not  
hypotheses = 'indic_1-.5 = 0, indic_2 - indic_1 = 0, indic_3 - indic_2 = 0, indic_4 - indic_3 = 0, indic_5 - indic_4 = 0'
t_test = res_assigned.t_test(hypotheses)
print(t_test)

fig, axs = plt.subplots(2, 1, figsize=(25, 15))
sns.pointplot(data=part2[(part2['player.number_variables']==2) ], x='model', y='player.correct',
              eestimator='mean', join=False, ax=axs[0])
axs[0].set_ylim(0, 1.05)
axs[0].set_title('performance by 2-variable model chosen')
axs[0].axhline(.5, 0, 1, color = 'grey')

sns.histplot(data=part2[(part2['player.number_variables']==2) ], x='model', stat='probability',
              discrete=True, ax=axs[1], hue='better_random_2040', multiple='stack')

axs[1].set_title('model choices')

sns.lineplot(data=part2[(part2['player.number_variables']==2) ], x='model', y='accuracy', ax=axs[0], 
              color='black')

fig.savefig('computed_objects/figures/p2_perfotmance_model_choices_2var.png')