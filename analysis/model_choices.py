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

# load the data in long format for each part
part1 = pd.read_csv('data/clean/part1.csv')
all_rounds = pd.read_csv('data/clean/all.csv')
part2 = pd.read_csv('data/clean/part2.csv')

# plot the histogram of model choices and the share of correct guesses
fig, axs = plt.subplots(2, 1, figsize=(25, 15))
sns.pointplot(data=part2, x='model', y='player.correct', 
              eestimator='mean', join=False, ax=axs[0], label='accuracy')
axs[0].set_ylim(0, 1.05)
axs[0].set_title('performance by 2-variable model chosen')
axs[0].axhline(.5, 0, 1, color = 'grey')

sns.histplot(data=part2, x='model', stat='probability',
              discrete=True, ax=axs[1], palette='Blues_r')


sns.lineplot(data=part2, x='model', y='accuracy', ax=axs[0], 
               markers='+', color='gray', label='informativeness')


axs[1].set_title('model choices')


fig.savefig('computed_objects/figures/model_choices_all.png')

# plot the histogram of model choices and the share of correct guesses when they have two variables available
fig, axs = plt.subplots(2, 1, figsize=(25, 15))
sns.pointplot(data=part2[(part2['player.number_variables']==2) ], x='model', y='player.correct',
              eestimator='mean', join=False, ax=axs[0])
axs[0].set_ylim(0, 1.05)
axs[0].set_title('performance by 2-variable model chosen')
axs[0].axhline(.5, 0, 1, color = 'grey')

sns.histplot(data=part2[(part2['player.number_variables']==2) ], x='model', stat='probability',
              discrete=True, ax=axs[1], multiple='stack')

axs[1].set_title('model choices')

sns.lineplot(data=part2[(part2['player.number_variables']==2) ], x='model', y='accuracy', ax=axs[0], 
              color='black')

fig.savefig('computed_objects/figures/model_choices_2vars.png')

# plot the accuracy of the chosen models over time to see if they choose better models over time
sns.lmplot(data=part2[part2['subsession.round_number']<41], x='subsession.round_number', y='accuracy', x_bins=10, hue='player.number_variables')
plt.xlabel('rounds in Part 2')
plt.ylabel('Accuracy of chosen model')

plt.axhline(.69, 0, 1, color = 'grey', linestyle='--', alpha = .5)
plt.axhline(.78, 0, 1, color = 'grey', linestyle='--', alpha = .5)
plt.axhline(1, 0, 1, color = 'grey', linestyle='--', alpha = .5)
plt.axhline(.85, 0, 1, color = 'grey', linestyle='--', alpha = .5)


plt.savefig('computed_objects/figures/acuracy_rounds.png')
