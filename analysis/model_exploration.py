
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
part2 = pd.read_csv('data/clean/part2.csv', dtype={'model': str})

# count the number of models that each subject uses in part 2 by number of available variables
model_counts = part2.groupby(['participant.code', 'model', 'player.number_variables'])['round_number_modif'].count()
model_counts = pd.DataFrame(model_counts)
model_counts.reset_index(inplace=True)
model_counts.rename(columns={'round_number_modif':'times_chosen'}, inplace=True)
count_models = model_counts.groupby(['participant.code','player.number_variables'])['model'].count()
count_models = pd.DataFrame(count_models)
count_models.reset_index(inplace=True)

counted_models = count_models.groupby(['player.number_variables', 'model']).count()
counted_models.reset_index(inplace=True)


count_models.rename(columns={'model':'number_models'}, inplace=True)
# plot the histogram of the number of models used by number of available variables
sns.histplot(data=count_models, x='player.number_variables', hue='number_models', multiple='dodge', discrete=True, palette='Blues_r')
plt.title('Number of models that were used at least once by a subject')
plt.savefig('computed_objects/figures/model_count.png') 


path_models = Path('data/clean/count_models.csv')  
path_models.parent.mkdir(parents=True, exist_ok=True)  
count_models.to_csv(path_models)


