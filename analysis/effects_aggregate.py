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

# import the clean data
part2 = pd.read_csv('data/clean/part2.csv')

# plot the average accuracy by number of variables revealed
fig, axs = plt.subplots()
axs = sns.pointplot(data=part2[part2['subsession.round_number']>0], x='revealed_variables_count', y='player.correct', eestimator='mean', join=False)
plt.ylim(.35, .75)
plt.title('Performance by number of revealed variables')
plt.axhline(.5, 0, 1, color = 'grey')
axs.set_xlabel('number of revealed variables')
axs.set_ylabel('share of correct guesses')
fig.show()

fig.savefig('computed_objects/figures/revealed_variables_pooled.png')

# plot the average accuracy by number of variables assigned 
fig, axs = plt.subplots()
sns.pointplot(data=part2[part2['subsession.round_number']>0], x='player.number_variables', y='player.correct', eestimator='mean', join=False, ax=axs)
plt.ylim(.35, .75)
plt.title('Performance by number of available variables')
plt.axhline(.5, 0, 1, color = 'grey')
axs.set_xlabel('number of available variables')
axs.set_ylabel('share of correct guesses')

fig.show()

fig.savefig('computed_objects/figures/assigned_variables.png')

# plot the accuracy by number of variables assigned, binned by rounds

# Accuracy wrt number of variables that they were allowed to choose over rounds
fig, axs = plt.subplots(1, 3, figsize=(25, 5))
fig.suptitle('performance by number of available variables')

sns.pointplot(data=part2[(part2['subsession.round_number']>0) & (part2['subsession.round_number']<21)], 
              x='player.number_variables', y='player.correct', eestimator='mean', join=False, ax=axs[0])
axs[0].set_ylim(.35, .75)
axs[0].axhline(.5, 0, 1, color = 'grey')
axs[0].set_title('rounds 20 to 40')
axs[0].set_xlabel('number variables')
axs[0].set_ylabel('share correct guesses')

sns.pointplot(data=part2[(part2['subsession.round_number']>20) & (part2['subsession.round_number']<41)], 
              x='player.number_variables', y='player.correct', eestimator='mean', join=False, ax=axs[1])
axs[1].set_ylim(.35, .75)
axs[1].axhline(.5, 0, 1, color = 'grey')
axs[1].set_title('rounds 40 to 60')
axs[1].set_xlabel('number variables')
axs[1].set_ylabel('')

sns.pointplot(data=part2[(part2['subsession.round_number']>40)], 
              x='player.number_variables', y='player.correct', eestimator='mean', join=False, ax=axs[2])
axs[2].set_ylim(.35, .75)
axs[2].axhline(.5, 0, 1, color = 'grey')
axs[2].set_title('rounds over 60')
axs[2].set_xlabel('number variables')
axs[2].set_ylabel('')

fig.savefig('computed_objects/figures/assigned_variables_time.png')

# average number of variables revealed in each treatment
fig, axs = plt.subplots()
sns.pointplot(data=part2, x='player.number_variables', y='revealed_variables_count', eestimator='mean', join=False, ax=axs)
axs.plot([0, 5], [1, 6], color='gray')
axs.set_xlim(-0.5,4.5)
axs.set_ylim(.5, 5)

axs.set_xlabel('available variables')
axs.set_ylabel('revealed variables')

axs.set_title('Number of chosen variables by number of available variables')

fig.savefig('computed_objects/figures/revealed_available.png')