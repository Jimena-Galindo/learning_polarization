# There are 4 random variables that together determine a state of the world. 
# This scripts simulates the accuracy of the models that the players could choose from.

import numpy as np
import scipy.stats as stats
import scipy as sp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# for 10k observations draw from each of the random variables
N = 10000
x1 = np.random.normal(loc=0, scale=1, size=N)
x2 = np.random.normal(loc=-10, scale=2, size=N)
x3 = np.random.normal(loc=5, scale=3, size=N)
x4 = np.random.normal(loc=-5, scale=4, size=N)

# there is a constant term that shits the hyperplane so that the expectation of the linear combination of the variables is 0
k = 50.5

# round each draw tho the nearest integer (in otree we use integers for the experiment)
x1=x1.round(decimals=0)
x2=x2.round(decimals=0)
x3=x3.round(decimals=0)
x4=x4.round(decimals=0)

# create a dataframe with the draws
df = pd.DataFrame()
df['x1']=x1
df['x2']=x2
df['x3']=x3
df['x4']=x4

# compute the state of the world
df['y']=11*df['x1']+6*df['x2']+4.5*df['x3']+2.4*df['x4']+k>=0

# plot the distribution of the draws by state
fig, axs = plt.subplots(2, 2)
sns.histplot(data=df, x='x1', hue='y', ax=axs[0, 0], stat='probability')
axs[0,0].set_xlim(-20, 20)
axs[0,0].set_ylim(0, .025)
sns.histplot(data=df, x='x2', hue='y', ax=axs[0, 1], stat='probability')
axs[0,1].set_xlim(-20, 20)
axs[0,1].set_ylim(0, .025)
sns.histplot(data=df, x='x3', hue='y', ax=axs[1, 0], stat='probability')
axs[1,0].set_xlim(-20, 20)
axs[1,0].set_ylim(0, .025)
sns.histplot(data=df, x='x4', hue='y', ax=axs[1, 1], stat='probability')
axs[1,1].set_xlim(-20, 20)
axs[1,1].set_ylim(0, .025)

# plot the probability of each state
sns.histplot(data=df, x='y', discrete=True, stat='probability')

# compute the accuracy of each model

########
# single variable models
########

df1=df[['x1', 'x2', 'y']].groupby(by=["x1", "y"]).count()/len(x1)
df1.reset_index(inplace=True)
df1.rename(columns={'x2':'px1y'}, inplace=True)
df1_aux = df1[['x1', 'px1y']].groupby(by='x1').sum()
df1_aux.reset_index(inplace=True)
df1_aux.rename(columns={'px1y':'px1'}, inplace=True)
df1.merge(df1_aux)
df1_true = df1.loc[df1['y']==True]
df1_true = df1_true.rename(columns={'px1y':'true_x1'})
df1_false = df1.loc[df1['y']==False].rename(columns={'px1y':'false_x1'})
df1_final=df1_true.merge(df1_false, on='x1' ,how='outer')
df1_final.fillna(0, inplace=True)
model_1 = np.maximum(df1_final['true_x1'], df1_final['false_x1']).sum()

df2=df[['x2', 'x3', 'y']].groupby(by=["x2", "y"]).count()/len(x2)
df2.reset_index(inplace=True)
df2.rename(columns={'x3':'px2y'}, inplace=True)
df2_aux = df2[['x2', 'px2y']].groupby(by='x2').sum()
df2_aux.reset_index(inplace=True)
df2_aux.rename(columns={'px2y':'px2'}, inplace=True)
df2.merge(df2_aux)
df2_true = df2.loc[df2['y']==True]
df2_true = df2_true.rename(columns={'px2y':'true_x2'})
df2_false = df2.loc[df2['y']==False].rename(columns={'px2y':'false_x2'})
df2_final=df2_true.merge(df2_false, on='x2' ,how='outer')
df2_final.fillna(0, inplace=True)
model_2 = np.maximum(df2_final['true_x2'], df2_final['false_x2']).sum()

df3=df[['x3', 'x2', 'y']].groupby(by=["x3", "y"]).count()/len(x3)
df3.reset_index(inplace=True)
df3.rename(columns={'x2':'px3y'}, inplace=True)
df3_aux = df3[['x3', 'px3y']].groupby(by='x3').sum()
df3_aux.reset_index(inplace=True)
df3_aux.rename(columns={'px3y':'px3'}, inplace=True)
df3.merge(df3_aux)
df3_true = df3.loc[df3['y']==True]
df3_true = df3_true.rename(columns={'px3y':'true_x3'})
df3_false = df3.loc[df3['y']==False].rename(columns={'px3y':'false_x3'})
df3_final=df3_true.merge(df3_false, on='x3' ,how='outer')
df3_final.fillna(0, inplace=True)
model_3 = np.maximum(df3_final['true_x3'], df3_final['false_x3']).sum()

df4=df[['x4', 'x2', 'y']].groupby(by=["x4", "y"]).count()/len(x4)
df4.reset_index(inplace=True)
df4.rename(columns={'x2':'px4y'}, inplace=True)
df4_aux = df4[['x4', 'px4y']].groupby(by='x4').sum()
df4_aux.reset_index(inplace=True)
df4_aux.rename(columns={'px4y':'px4'}, inplace=True)
df4.merge(df4_aux)
df4_true = df4.loc[df4['y']==True]
df4_true = df4_true.rename(columns={'px4y':'true_x4'})
df4_false = df4.loc[df4['y']==False].rename(columns={'px4y':'false_x4'})
df4_final=df4_true.merge(df4_false, on='x4' ,how='outer')
df4_final.fillna(0, inplace=True)
model_4 = np.maximum(df4_final['true_x4'], df4_final['false_x4']).sum()

########
# two variable models
########

df12=df[['x1', 'x2', 'x3', 'y']].groupby(by=["x1", "x2", "y"]).count()/len(x1)
df12.reset_index(inplace=True)
df12.rename(columns={'x3':'px1x2y'}, inplace=True)
df12_aux = df12[['x1', 'x2', 'px1x2y']].groupby(by=['x1', 'x2']).sum()
df12_aux.reset_index(inplace=True)
df12_aux.rename(columns={'px1x2y':'px1x2'}, inplace=True)
df12.merge(df12_aux)
df12_true = df12.loc[df12['y']==True]
df12_true = df12_true.rename(columns={'px1x2y':'true_x1x2'})
df12_false = df12.loc[df12['y']==False].rename(columns={'px1x2y':'false_x1x2'})
df12_final=df12_true.merge(df12_false, on=['x1', 'x2'] ,how='outer')
df12_final.fillna(0, inplace=True)
model_12 = np.maximum(df12_final['true_x1x2'], df12_final['false_x1x2']).sum()

df13=df[['x1', 'x3', 'x4', 'y']].groupby(by=["x1", "x3", "y"]).count()/len(x1)
df13.reset_index(inplace=True)
df13.rename(columns={'x4':'px1x3y'}, inplace=True)
df13_aux = df13[['x1', 'x3', 'px1x3y']].groupby(by=['x1', 'x3']).sum()
df13_aux.reset_index(inplace=True)
df13_aux.rename(columns={'px1x3y':'px1x3'}, inplace=True)
df13.merge(df13_aux)
df13_true = df13.loc[df13['y']==True]
df13_true = df13_true.rename(columns={'px1x3y':'true_x1x3'})
df13_false = df13.loc[df13['y']==False].rename(columns={'px1x3y':'false_x1x3'})
df13_final=df13_true.merge(df13_false, on=['x1', 'x3'] ,how='outer')
df13_final.fillna(0, inplace=True)
model_13 = np.maximum(df13_final['true_x1x3'], df13_final['false_x1x3']).sum()

df14=df[['x1', 'x4', 'x3', 'y']].groupby(by=["x1", "x4", "y"]).count()/len(x1)
df14.reset_index(inplace=True)
df14.rename(columns={'x3':'px1x4y'}, inplace=True)
df14_aux = df14[['x1', 'x4', 'px1x4y']].groupby(by=['x1', 'x4']).sum()
df14_aux.reset_index(inplace=True)
df14_aux.rename(columns={'px1x4y':'px1x4'}, inplace=True)
df14.merge(df14_aux)
df14_true = df14.loc[df14['y']==True]
df14_true = df14_true.rename(columns={'px1x4y':'true_x1x4'})
df14_false = df14.loc[df14['y']==False].rename(columns={'px1x4y':'false_x1x4'})
df14_final=df14_true.merge(df14_false, on=['x1', 'x4'] ,how='outer')
df14_final.fillna(0, inplace=True)
model_14 = np.maximum(df14_final['true_x1x4'], df14_final['false_x1x4']).sum()

df23=df[['x2', 'x3', 'x4', 'y']].groupby(by=["x2", "x3", "y"]).count()/len(x2)
df23.reset_index(inplace=True)
df23.rename(columns={'x4':'px2x3y'}, inplace=True)
df23_aux = df23[['x2', 'x3', 'px2x3y']].groupby(by=['x2', 'x3']).sum()
df23_aux.reset_index(inplace=True)
df23_aux.rename(columns={'px2x3y':'px2x3'}, inplace=True)
df23.merge(df23_aux)
df23_true = df23.loc[df23['y']==True]
df23_true = df23_true.rename(columns={'px2x3y':'true_x2x3'})
df23_false = df23.loc[df23['y']==False].rename(columns={'px2x3y':'false_x2x3'})
df23_final=df23_true.merge(df23_false, on=['x2', 'x3'] ,how='outer')
df23_final.fillna(0, inplace=True)
model_23 = np.maximum(df23_final['true_x2x3'], df23_final['false_x2x3']).sum()

df24=df[['x2', 'x4', 'x3', 'y']].groupby(by=["x2", "x4", "y"]).count()/len(x2)
df24.reset_index(inplace=True)
df24.rename(columns={'x3':'px2x4y'}, inplace=True)
df24_aux = df24[['x2', 'x4', 'px2x4y']].groupby(by=['x2', 'x4']).sum()
df24_aux.reset_index(inplace=True)
df24_aux.rename(columns={'px2x4y':'px2x4'}, inplace=True)
df24.merge(df24_aux)
df24_true = df24.loc[df24['y']==True]
df24_true = df24_true.rename(columns={'px2x4y':'true_x2x4'})
df24_false = df24.loc[df24['y']==False].rename(columns={'px2x4y':'false_x2x4'})
df24_final=df24_true.merge(df24_false, on=['x2', 'x4'] ,how='outer')
df24_final.fillna(0, inplace=True)
model_24 = np.maximum(df24_final['true_x2x4'], df24_final['false_x2x4']).sum()

df34=df[['x3', 'x4', 'x2', 'y']].groupby(by=["x3", "x4", "y"]).count()/len(x3)
df34.reset_index(inplace=True)
df34.rename(columns={'x2':'px3x4y'}, inplace=True)
df34_aux = df34[['x3', 'x4', 'px3x4y']].groupby(by=['x3', 'x4']).sum()
df34_aux.reset_index(inplace=True)
df34_aux.rename(columns={'px3x4y':'px3x4'}, inplace=True)
df34.merge(df34_aux)
df34_true = df34.loc[df34['y']==True]
df34_true = df34_true.rename(columns={'px3x4y':'true_x3x4'})
df34_false = df34.loc[df34['y']==False].rename(columns={'px3x4y':'false_x3x4'})
df34_final=df34_true.merge(df34_false, on=['x3', 'x4'] ,how='outer')
df34_final.fillna(0, inplace=True)
model_34 = np.maximum(df34_final['true_x3x4'], df34_final['false_x3x4']).sum()

########
# three variable models
########

df123=df[['x1', 'x2', 'x3', 'x4','y']].groupby(by=["x1", "x2", "x3" ,"y"]).count()/len(x1)
df123.reset_index(inplace=True)
df123.rename(columns={'x4':'px1x2x3y'}, inplace=True)
df123_aux = df123[['x1', 'x2', 'x3', 'px1x2x3y']].groupby(by=['x1', 'x2', 'x3']).sum()
df123_aux.reset_index(inplace=True)
df123_aux.rename(columns={'px1x2x3y':'px1x2x3'}, inplace=True)
df123.merge(df123_aux)
df123_true = df123.loc[df123['y']==True]
df123_true = df123_true.rename(columns={'px1x2x3y':'true_x1x2x3'})
df123_false = df123.loc[df123['y']==False].rename(columns={'px1x2x3y':'false_x1x2x3'})
df123_final=df123_true.merge(df123_false, on=['x1', 'x2', 'x3'] ,how='outer')
df123_final.fillna(0, inplace=True)
model_123 = np.maximum(df123_final['true_x1x2x3'], df123_final['false_x1x2x3']).sum()

df124=df[['x1', 'x2', 'x4', 'x3','y']].groupby(by=["x1", "x2", "x4" ,"y"]).count()/len(x1)
df124.reset_index(inplace=True)
df124.rename(columns={'x3':'px1x2x4y'}, inplace=True)
df124_aux = df124[['x1', 'x2', 'x4', 'px1x2x4y']].groupby(by=['x1', 'x2', 'x4']).sum()
df124_aux.reset_index(inplace=True)
df124_aux.rename(columns={'px1x2x4y':'px1x2x4'}, inplace=True)
df124.merge(df124_aux)
df124_true = df124.loc[df124['y']==True]
df124_true = df124_true.rename(columns={'px1x2x4y':'true_x1x2x4'})
df124_false = df124.loc[df124['y']==False].rename(columns={'px1x2x4y':'false_x1x2x4'})
df124_final=df124_true.merge(df124_false, on=['x1', 'x2', 'x4'] ,how='outer')
df124_final.fillna(0, inplace=True)
model_124 = np.maximum(df124_final['true_x1x2x4'], df124_final['false_x1x2x4']).sum()

df134=df[['x1', 'x3', 'x4', 'x2','y']].groupby(by=["x1", "x3", "x4" ,"y"]).count()/len(x1)
df134.reset_index(inplace=True)
df134.rename(columns={'x2':'px1x3x4y'}, inplace=True)
df134_aux = df134[['x1', 'x3', 'x4', 'px1x3x4y']].groupby(by=['x1', 'x3', 'x4']).sum()
df134_aux.reset_index(inplace=True)
df134_aux.rename(columns={'px1x3x4y':'px1x3x4'}, inplace=True)
df134.merge(df134_aux)
df134_true = df134.loc[df134['y']==True]
df134_true = df134_true.rename(columns={'px1x3x4y':'true_x1x3x4'})
df134_false = df134.loc[df134['y']==False].rename(columns={'px1x3x4y':'false_x1x3x4'})
df134_final=df134_true.merge(df134_false, on=['x1', 'x3', 'x4'] ,how='outer')
df134_final.fillna(0, inplace=True)
model_134 = np.maximum(df134_final['true_x1x3x4'], df134_final['false_x1x3x4']).sum()

df234=df[['x2', 'x3', 'x4', 'x1','y']].groupby(by=["x2", "x3", "x4" ,"y"]).count()/len(x2)
df234.reset_index(inplace=True)
df234.rename(columns={'x1':'px2x3x4y'}, inplace=True)
df234_aux = df234[['x2', 'x3', 'x4', 'px2x3x4y']].groupby(by=['x2', 'x3', 'x4']).sum()
df234_aux.reset_index(inplace=True)
df234_aux.rename(columns={'px2x3x4y':'px2x3x4'}, inplace=True)
df234.merge(df234_aux)
df234_true = df234.loc[df234['y']==True]
df234_true = df234_true.rename(columns={'px2x3x4y':'true_x2x3x4'})
df234_false = df234.loc[df234['y']==False].rename(columns={'px2x3x4y':'false_x2x3x4'})
df234_final=df234_true.merge(df234_false, on=['x2', 'x3', 'x4'] ,how='outer')
df234_final.fillna(0, inplace=True)
model_234 = np.maximum(df234_final['true_x2x3x4'], df234_final['false_x2x3x4']).sum()

# Add a fifth variable that is not informative. The accuracy of each model should not change when we add this variable.
model_5 = 0.5
model_15 = model_1
model_25 = model_2
model_35 = model_3
model_45 = model_4

model_125 = model_12
model_135 = model_13
model_145 = model_14
model_235 = model_23
model_245 = model_24
model_345 = model_34

model_1235 = model_123
model_1245 = model_124
model_2345 = model_234
model_1345 = model_134

model_1234 = 1
model_12345 = 1

# a dictionary with the accuracy of each model
model_accuracy = {'00000':.5, '10000':model_1, '01000':model_2, '00100':model_3, '00010':model_4, '00001':model_5, 
 '11000':model_12, '10100':model_13, '10010':model_14, '10001':model_15, '01100':model_23, '01010':model_24, '01001':model_25, '00110':model_34, '00101':model_35, '00011':model_45,
 '11100':model_123, '11010':model_124, '11001':model_125, '10110':model_134, '10101':model_135, '10011':model_145, '01110':model_234, '01101':model_235, '01011':model_245, '00111':model_345,
 '11110':model_1234, '11101':model_1235, '11011':model_1245, '10111':model_1345, '01111':model_2345, '11111':model_12345}

# create a dataframe with the accuracy of each model
model_accuracy = pd.DataFrame.from_dict(model_accuracy, orient='index')
model_accuracy.rename(columns={0:'accuracy'}, inplace=True)
model_accuracy.reset_index(inplace=True)

# save the dataframe as a csv file
model_accuracy.to_csv("computed_objects/tables/model_accuracy.csv")