
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

# which are their single variable models and do they change over time?
# count the number of times each model was chosen by rounds. grouping rounds into 20 round bins
fig, axs = plt.subplots(1, 3, figsize=(20, 5))
fig.suptitle('Single-Variable Models')

sns.histplot(data=part2[part2['subsession.round_number']<=20], x='single_variable', discrete=True, stat='probability', ax=axs[0])
axs[0].set_title('rounds 21 to 40')
axs[0].set_ylim(0. ,.6)

sns.histplot(data=part2[(part2['subsession.round_number']>20) & (part2['subsession.round_number']<=40)], x='single_variable', discrete=True, stat='probability', ax=axs[1])
axs[1].set_title('rounds 41 to 60')
axs[1].set_ylim(0. ,.6)

sns.histplot(data=part2[(part2['subsession.round_number']>40)], x='single_variable', discrete=True, stat='probability', ax=axs[2])
axs[2].set_title('rounds 61 and over')
axs[2].set_ylim(0. ,.6)

plt.savefig('computed_objects/figures/single_variable_time.png')

# bar plot with the frequency with which each variable was chosen. the first bar is the average of chose_x1 across all rounds
# bar2 is the average of chose_x2 across all rounds and so on
fig, ax = plt.subplots(figsize=(10, 5))
averages = part2[['player.chose_x1', 'player.chose_x2', 'player.chose_x3', 'player.chose_x4', 'player.chose_x5']].mean()
sns.barplot(x=averages.index, y=averages.values, ax=ax)
# label the axes
plt.xlabel('variable')
plt.ylabel('share of times chosen')
# label the columns
plt.xticks([0, 1, 2, 3, 4], ['x1', 'x2', 'x3', 'x4', 'x5'])
# save the plot
plt.savefig('computed_objects/figures/variable_choices_average.png')

# same plot but group by 20 rounds
fig, axs = plt.subplots(1, 3, figsize=(20, 5)) 
fig.suptitle('Variable Choices by Round')
averages_1 = part2[part2['subsession.round_number']<=20][['player.chose_x1', 'player.chose_x2', 'player.chose_x3', 'player.chose_x4', 'player.chose_x5']].mean()
sns.barplot(x=averages_1.index, y=averages_1.values, ax=axs[0])
axs[0].set_title('rounds 21 to 40')
axs[0].set_ylim(0. ,.8)
axs[0].set_xlabel('variable')
axs[0].set_ylabel('share of times chosen')
axs[0].set_xticks([0, 1, 2, 3, 4], ['x1', 'x2', 'x3', 'x4', 'x5'])

averages_2 = part2[(part2['subsession.round_number']>20) & (part2['subsession.round_number']<=40)][['player.chose_x1', 'player.chose_x2', 'player.chose_x3', 'player.chose_x4', 'player.chose_x5']].mean()
sns.barplot(x=averages_2.index, y=averages_2.values, ax=axs[1])
axs[1].set_title('rounds 41 to 60')
axs[1].set_ylim(0. ,.8)
axs[1].set_xlabel('variable')
axs[1].set_xticks([0, 1, 2, 3, 4], ['x1', 'x2', 'x3', 'x4', 'x5'])

averages_3 = part2[(part2['subsession.round_number']>40)][['player.chose_x1', 'player.chose_x2', 'player.chose_x3', 'player.chose_x4', 'player.chose_x5']].mean()
sns.barplot(x=averages_3.index, y=averages_3.values, ax=axs[2])
axs[2].set_title('rounds 61 and over')
axs[2].set_ylim(0. ,.8)
axs[2].set_xlabel('variable')
axs[2].set_xticks([0, 1, 2, 3, 4], ['x1', 'x2', 'x3', 'x4', 'x5'])

fig.show()

plt.savefig('computed_objects/figures/variable_choices_time.png')