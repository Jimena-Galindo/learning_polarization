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
sns.lmplot(data=all_rounds[all_rounds['round_number_modif']<=60], x="round_number_modif", y="player.correct", 
 x_bins=10, hue='better_random_2040')
plt.savefig('computed_objects/figures/p2_correct_rounds.png')

# add the indicator to the part2 table
part2 = part2.merge(guesses2040, on='participant.code').rename(columns={'player.correct_y':'2040_count', 'player.correct_x':'player.correct'})
part2.loc[part2['2040_count']>10, 'better_random_2040'] = 1
part2.loc[part2['2040_count']<=10, 'better_random_2040'] = 0

# Accuracy wrt number of variables that they chose to reveal and by performance in part2
fig, axs = plt.subplots()
axs = sns.pointplot(data=part2[part2['subsession.round_number']>0], x='revealed_variables_count', y='player.correct', 
                    hue='better_random_2040', estimator='mean', join=False)
plt.ylim(.35, .75)

plt.axhline(.5, 0, 1, color = 'grey')
axs.set_xlabel('number of revealed variables')
axs.set_ylabel('share of correct guesses')

fig.show()
fig.savefig('computed_objects/figures/p2_performance_effect_revealed.png')

# Accuracy wrt number of variables that they were allowed to choose and by performance in part2
fig, axs = plt.subplots()
axs = sns.pointplot(data=part2[part2['subsession.round_number']>0], x='player.number_variables', y='player.correct', 
                    hue='better_random_2040', estimator='mean', join=False)
plt.ylim(.35, .75)

plt.axhline(.5, 0, 1, color = 'grey')
axs.set_xlabel('number of allowed variables')
axs.set_ylabel('share of correct guesses')
fig.show()

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
              hue='better_random_2040', estimator='mean', join=False, ax=axs[0])
axs[0].set_ylim(0, 1)
axs[0].set_title('performance by models with 1 variable chosen (after 40 rounds)')
axs[0].axhline(.5, 0, 1, color = 'grey')

sns.pointplot(data=part2[(part2['player.number_variables']==2) & (part2['subsession.round_number']>20)], x='model', y='player.correct', 
              hue='better_random_2040', estimator='mean', join=False, ax=axs[1])
axs[1].set_ylim(0, 1)
axs[1].set_title('performance by models with 1 variable chosen (after 40 rounds)')
axs[1].axhline(.5, 0, 1, color = 'grey')



