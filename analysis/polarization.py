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
from linearmodels.panel import RandomEffects
import linearmodels

# load the data in long format for each part
part1 = pd.read_csv('data/clean/part1.csv')
all_rounds = pd.read_csv('data/clean/all.csv')
part2 = pd.read_csv('data/clean/part2.csv', dtype={'model': str})
pairs = pd.read_csv('data/clean/pairs.csv')

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

stargazer = Stargazer([res_predicted], )

with open('computed_objects/tables/regression_predicted_polariz.txt', 'w') as f:
    f.write(stargazer.render_latex())

hypotheses = 'round_number_modif-round_number_modif:predicted_polarization=0'
t_test = res_predicted.t_test(hypotheses)

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

sns.lmplot(data=pairs[pairs['round_number_modif']<61], x='round_number_modif', y='polarized', x_bins=5, hue='predicted_polarization')
plt.title('polarization across all rounds')
plt.axhline(.5, 0, 1, color = 'grey')

plt.savefig('computed_objects/figures/polarization_rounds_predicted.png')  

pairs[(pairs['round_number_modif']>40)].groupby('predicted_polarization')['polarized'].mean()

sp.stats.ttest_ind(pairs[(pairs['predicted_polarization']==1)& (pairs['round_number_modif']>40)]['polarized'], pairs[(pairs['predicted_polarization']==0)& (pairs['round_number_modif']>40)]['polarized'])

# Regression intercept and indicator variable of predicted polarization 
# if beta1 is significant then there is more polarization when predicted by the theory

y=pairs['polarized']

mod = smf.ols(formula='y ~1+ C(predicted_polarization)', data=pairs)

res_polariz = mod.fit(cov_type='HC3')


stargazer = Stargazer([res_polariz], )

with open('computed_objects/tables/predicted_polarization_ttest.txt', 'w') as f:
    f.write(stargazer.render_latex())
