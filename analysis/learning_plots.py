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



# read the clean data
part1 = pd.read_csv('data/clean/part1.csv')
part2 = pd.read_csv('data/clean/part2.csv')
all_rounds = pd.read_csv('data/clean/all.csv')

# plot the regression line of correct guesses by round in part 1 and bin the data into 5 bins with equal number of observations
sns.lmplot(data=all_rounds[all_rounds['round_number_modif']<21], x="subsession.round_number", y="player.correct", 
            x_bins=5, aspect=1.5, height=5)
# add a line at .5 that indicates the random guess level 
plt.axhline(.5, 0, 1, color = 'grey')
plt.tight_layout()
plt.xlabel('round number')
plt.ylabel('share correct guesses')

# save the plot as learning_part1
plt.savefig('computed_objects/figures/learning_part1.png')

# similar plot but using all_rounds and binning the data into 10 bins
# plot the guesses in all rounds with standard errors and by number of variables that they were allowed to reveal
# truncate the data at round 60 since there are only few observations after that
sns.lmplot(data=all_rounds[(all_rounds['player.number_variables']>3) & (all_rounds['round_number_modif']<61)], x="round_number_modif", y="player.correct", 
            x_bins=10, aspect=1.5, height=5)
plt.tight_layout()
plt.xlabel('round number')
plt.ylabel('share correct')
plt.axhline(.5, 0, 1, color = 'grey')


plt.savefig('computed_objects/figures/learning_all.png')