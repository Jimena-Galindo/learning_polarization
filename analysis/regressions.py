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
from linearmodels.panel import RandomEffects
import linearmodels

# load the data in long format for each part
part1 = pd.read_csv('data/clean/part1.csv')
all_rounds = pd.read_csv('data/clean/all.csv')
part2 = pd.read_csv('data/clean/part2.csv')

# aggregate regression with treatment assignment only (no random effects)
y=part2['player.correct']
part2['round'] = part2['subsession.round_number']

mod = smf.ols(formula='y ~ indic_1 + indic_2+ indic_3 + indic_4 + indic_5  - 1', data=part2)

res_assigned = mod.fit(cov_type='HC3')

stargazer = Stargazer([res_assigned], )

with open('computed_objects/tables/regression_assigned.txt', 'w') as f:
    f.write(stargazer.render_latex())



# For the regression using assignment to treatment directly,
# test that 1 variable makes the guesses better than random, and whether adding an extra variable is helpful or not  
hypotheses = 'indic_1-.5 = 0, indic_2 - indic_1 = 0, indic_3 - indic_2 = 0, indic_4 - indic_3 = 0, indic_5 - indic_4 = 0'
t_test_assigned = res_assigned.t_test(hypotheses)

with open('computed_objects/tables/ttest_assigned.txt', 'w') as f:
    f.write(str(t_test_assigned.summary()))

# Regression with the chosen number of variables (aggregate regression, all subjects and all rounds pooled)

y=part2['player.correct']

mod = smf.ols(formula='y ~ C(revealed_variables_count)-1', data=part2)

res_revealed = mod.fit(cov_type='HC3')


stargazer = Stargazer([res_revealed], )

with open('computed_objects/tables/regression_revealed.txt', 'w') as f:
    f.write(stargazer.render_latex())


hypotheses = 'C(revealed_variables_count)[0] - .5 = 0, C(revealed_variables_count)[1] - C(revealed_variables_count)[0] = 0, C(revealed_variables_count)[2] - C(revealed_variables_count)[1] = 0, C(revealed_variables_count)[3] - C(revealed_variables_count)[2] = 0, C(revealed_variables_count)[4] - C(revealed_variables_count)[3] = 0, C(revealed_variables_count)[5] - C(revealed_variables_count)[4] = 0'
t_test_revealed = res_revealed.t_test(hypotheses)


with open('computed_objects/tables/ttest_revealed.txt', 'w') as f:
    f.write(str(t_test_revealed.summary()))


