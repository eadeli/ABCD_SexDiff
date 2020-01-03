#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pygrowup import Calculator
from pygrowup import helpers

calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                       include_cdc=True, logger_name='pygrowup',
                       log_level='INFO')


# In[2]:


import numpy as np 
import pandas as pd
from functools import reduce

all_subs     = np.array([])

for i in range(5):
    all_subs = np.concatenate((all_subs, np.genfromtxt('./5cv/subid_' + str(i+1) + '.txt', dtype='str')))
    
all_bmiinfo = pd.read_csv('./abcd_ant01.csv')
all_bmiinfo = all_bmiinfo[all_bmiinfo.subjectkey.isin(all_subs)]

all_bmiinfo = all_bmiinfo.sort_values('interview_ageyyy', ascending=True)
all_bmiinfo = all_bmiinfo.drop_duplicates(subset='subjectkey', keep='first')

dfb = all_bmiinfo[all_bmiinfo['sex']=='M'].dropna(axis=0, subset=['anthroheightcalc', 'anthroweightcalc', 'interview_ageyyy'])
dfb['bmi_z'] = dfb.apply(lambda x: calculator.bmifa((float(x['anthroweightcalc']) * 703) / (float(x['anthroheightcalc'])**2), float(x['interview_ageyyy']), 'M'), axis = 1)

dfg = all_bmiinfo[all_bmiinfo['sex']=='F'].dropna(axis=0, subset=['anthroheightcalc', 'anthroweightcalc', 'interview_ageyyy'])
dfg.drop(6246, axis=0, inplace=True)
dfg['bmi_z'] = dfg.apply(lambda x: calculator.bmifa((float(x['anthroweightcalc']) * 703) / (float(x['anthroheightcalc'])**2), float(x['interview_ageyyy']), 'F'), axis = 1)


# In[3]:


from scipy import stats

print ('%f +- %f' % (np.mean(np.array(dfb['bmi_z'], dtype=np.float64)), np.std(np.array(dfb['bmi_z'], dtype=np.float64))))
print ('%f +- %f' % (np.mean(np.array(dfg['bmi_z'])), np.std(np.array(dfg['bmi_z']))))
[sss, p] = stats.ttest_ind(np.array(dfb['bmi_z'], dtype=np.float64), np.array(dfg['bmi_z'], dtype=np.float64), equal_var = False)

print ('%2.20f' % p)

