# sort subjects by their performance in the first part of the experiment
# this script creates a variable that indicates whether they were better than random in the first 20 rounds and plots
# the effect of revealing/allowing an additional variable.

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

# figure out how many guesses they got correct in the first 20 roundsfirst20, on='participant.code').rename(columns={'player.correct_y':'first20_count'})
first20 = part1.groupby('participant.code').sum()['player.correct']
part1 = part1.merge(first20, on='participant.code').rename(columns={'player.correct_y':'first20_count', 'player.correct_x':'playe.correct'})

part1.loc[part1['first20_count']>10, 'better_random'] = 1
part1.loc[part1['first20_count']<=10, 'better_random'] = 0

all_rounds = all_rounds.merge(first20, on='participant.code').rename(columns={'player.correct_y':'first20_count', 'player.correct_x':'player.correct'})
all_rounds.loc[all_rounds['first20_count']>10, 'better_random'] = 1
all_rounds.loc[all_rounds['first20_count']<=10, 'better_random'] = 0

part2 = part2.merge(first20, on='participant.code').rename(columns={'player.correct_y':'first20_count', 'player.correct_x':'player.correct'})
part2.loc[part2['first20_count']>10, 'better_random'] = 1
part2.loc[part2['first20_count']<=10, 'better_random'] = 0

# plot the chance of guessing correctly by rounds (binned into 5) for the first 20 rounds
sns.lmplot(data=all_rounds[(all_rounds['round_number_modif']<=20) ], x="round_number_modif", y="player.correct", 
 x_bins=5, hue='better_random')
# save the plot
plt.savefig('computed_objects/figures/performance_part1.png')

# plot the two groups throughout the experiment
# plot the chance of guessing correctly by rounds (binned into 10 bins) by performance in part 1

sns.lmplot(data=all_rounds, x="round_number_modif", y="player.correct",  x_bins=10, hue='better_random')
plt.title('Learning by performance in part 1')
plt.xlabel('round number')
plt.ylabel('share correct')
plt.savefig('computed_objects/figures/p1_performance_throughout.png')

# Accuracy wrt number of variables that they were allowed to choose and by part1 performance
fig, axs = plt.subplots( figsize=(15, 5))
sns.pointplot(data=all_rounds[(all_rounds['round_number_modif']>20)], x='player.number_variables', y='player.correct', 
              hue='better_random', eestimator='mean', join=False )
axs.set_ylim(.35, .75)
axs.set_title('performance by number of available variables after 20 rounds')
axs.axhline(.5, 0, 1, color = 'grey')

fig.savefig('computed_objects/figures/p1_performace_effect_assigned.png')

# Accuracy wrt number of variables that they were allowed to choose
fig, axs = plt.subplots( figsize=(15, 5))
sns.pointplot(data=all_rounds[(all_rounds['round_number_modif']>20)], x='revealed_variables_count', y='player.correct', 
              hue='better_random', eestimator='mean', join=False )
axs.set_ylim(.35, .75)
axs.set_title('performance by number of variables revealed')
axs.axhline(.5, 0, 1, color = 'grey')
fig.savefig('computed_objects/figures/p1_performace_effect_revealed.png')