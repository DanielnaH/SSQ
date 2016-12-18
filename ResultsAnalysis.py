# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:13:36 2016

@author: Daniel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb,perm
from math import sqrt
import numpy as np
#%%
names=['date','one','two','three','four','five','six','blue']
results=pd.read_csv('F:/Documents/PythonWork/AnalysisofSSQ/hun.txt',
                    names=names,header=None,sep=',')

#%%
#nomalize results read from hun.txt
def nom_results(df):
  
  df['one']=df['one'].str.slice(2,4)
  df['date']=df['date'].str.slice(-11,-1)
  df['blue']=df['blue'].str.slice(0,2)
  index=pd.to_datetime(df['date'])
  df.index=index
  df=df.drop('date',axis=1)
  return df.astype(int)
  
  
def get_reddum(df,index):

  df_dum=pd.DataFrame(np.zeros([len(df),33]),index=index)
  for col in range(6):
    for idx in range(len(df)):
      df_dum.ix[idx,df.ix[idx,col]-1]=1
  dum_names=[]
  for bid in range(1,34):
    dum_names.append('red_%d' % bid)
  df_dum.columns=dum_names
  return df_dum

#get the top10 appearance red ball id for each red ball id    
def get_top10(df,red_id,df_num):
  red=df.groupby(red_id).sum().T
  red.columns=['No','Yes']
  red=pd.merge(red,df_num,left_index=True,right_index=True)
  red['weight_num']=red['Yes']*red['prop']
  top10_index=red.sort_values(by='weight_num',ascending=False)[:10].index
  top10=list(top10_index)
  return top10

#write the dictionary into a txt document
def dict_txt(dict_write):
  f=open('top10_each_red.txt','w')
  for i in dict_write:
    writestr=str(i)[4:]+'\t'+str(dict_write[i])+'\n'
    f.write(writestr)
  f.close()
  
def dist_euclid(row_1,row_2):
  return sqrt(sum(pow(row_1-row_2,2)))

def dist_chessboard(row_1,row_2):
  return max(abs(row_1-row_2))
  
def dist_Man(row_1,row_2):
  return sum(abs(row_1-row_2))
  
def sim_dist(red_results,index):
  dist=[]
  for i in range(len(red_results)):
    dist_tmp=[dist_euclid(red_results.ix[index],red_results.ix[i]),
              dist_chessboard(red_results.ix[index],red_results.ix[i]),
              dist_Man(red_results.ix[index],red_results.ix[i])]
    dist.append(dist_tmp)
  return dist
#%%

#def get_redamt_a(df_dum,red_id):
#  red=df_dum[df_dum[red_id]==1].drop(red_id,axis=1)
#  red_A=red.resample('Q',kind='period').sum()
#  return red_A
#%%
results=nom_results(results)
red_dum=get_reddum(results,results.index)
red_num=pd.DataFrame(red_dum.sum(),columns=['counts'])
red_num['prop']=red_num['counts']/2020
#%%
dist_0=pd.DataFrame(sim_dist(results,0))
#%%
red_dum['week']=red_dum.index.strftime('%w')
red_Sun=red_dum[red_dum['week']=='0'].drop('week',axis=1)
red_Tue=red_dum[red_dum['week']=='2'].drop('week',axis=1)
red_Thu=red_dum[red_dum['week']=='4'].drop('week',axis=1)
#%%
dict_top10={}
for col in red_Tue.columns:
  dict_top10[col]=get_top10(red_Tue,col,red_num)
dict_txt(dict_top10)
#%%
#fig,ax_blue=plt.subplots(1,1)
#ax_blue.bar(results['blue'].value_counts().sort_index().index,
#            results['blue'].value_counts().sort_index(),0.4)
#%%
#fig,ax_red=plt.subplots(1,1)
#ax_red.bar(range(1,34),red_dum.sum(),0.35)
#%%
#fig_dist,ax_0=plt.subplots(1,1)
#ax_0.plot(dist_0)
#%%
fig_pie,ax_pie=plt.subplots(1,1)
arr=[2020,comb(33,6)-2020]
ax_pie.pie(arr,explode=(0.05,0),colors=['gold','lightcoral'],
           labels=['Combinations drew','All combinations'],
           radius=0.5,shadow=False,startangle=69)
ax_pie.axis('equal')
#%%
#p=pd.Period('5/1/2003',freq='W-Wed')
#(comb(33,6)-1)/3
#p+369189
