#!/usr/bin/env python
# coding: utf-8

# ## Exploring and Preparing Data

# ### Objectives
# 
# Perform exploratory Data Analysis and Feature Engineering using `Pandas` and `Matplotlib`
# 
# *   Exploratory Data Analysis
# *   Preparing Data  Feature Engineering

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[8]:


import requests


# In[80]:


path = "/Users/QXJ/Desktop/IBM/SpaceX/dataset_part_2.csv"
df = pd.read_csv(path, index_col = False)
df.head()


# First, let's try to see how the `FlightNumber` (indicating the continuous launch attempts.) and `Payload` variables would affect the launch outcome.

# In[233]:


sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect =2)
plt.xlabel("Flight Number",fontsize=12)
plt.ylabel("Pay load Mass (kg)",fontsize=12)
plt.xticks(np.arange(-1,120,10))
plt.show


# We see that different launch sites have different success rates.  <code>CCAFS LC-40</code>, has a success rate of 60 %, while  <code>KSC LC-39A</code> and <code>VAFB SLC 4E</code> has a success rate of 77%.

# Next, let's drill down to each site visualize its detailed launch records.

# #### 1. Visualize the relationship between Flight Number and Launch Site

# In[168]:


# Options are: “strip”, “swarm”, “box”, “violin”, “boxen”, “point”, “bar”, or “count”
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, kind = 'strip', aspect=2, alpha = 0.7)
plt.title('Flight Number vs. Launch Site', fontsize = 15)
plt.xlabel("Flight Number",fontsize=10)
plt.ylabel("Launch Site",fontsize=10)
plt.show()


# *-> KSC LC 39A has the highest sucessful rate, vice verce CCAFS SLC 40 has the lowest*

# #### 2. Visualize the relationship between Payload and Launch Site

# In[169]:


sns.catplot(x='LaunchSite',y='PayloadMass', hue = 'Class', data=df,aspect =2, alpha = 0.6)
plt.title('Payload vs. Launch Site', fontsize = 15)
plt.xlabel('Launch Site')
plt.ylabel('PayloadMass')
plt.show


# *-> VAFB SLC 4E has no payload obove 10000 kg*

# #### 4. Visualize the relationship between success rate of each orbit type

# In[97]:


df2 = df.groupby(['Orbit'])['Class'].mean().reset_index()
df2.head(30)


# In[136]:


sns.catplot(x = 'Orbit', y='Class', data=df2, kind='bar',palette = 'rocket', hue = 'Class', height =4, aspect =3, legend = None )
plt.title('Successful rate of different Orbits',fontsize = 20 )
plt.ylabel('Successful rate')
plt.show


# #### 4. Visualize the relationship between FlightNumber and Orbit type

# In[165]:


sns.catplot(y='Orbit', x='FlightNumber', data=df,hue='Class',aspect =2)
plt.title('Flight Number vs. Orbits', fontsize = 15)
plt.show


# *->In the LEO orbit the Success appears related to the number of flights; on the other hand, there seems to be no relationship between flight number when in GTO orbit.*

# #### 5. Visualize the relationship between Payload and Orbit type

# In[176]:


sns.catplot(x='PayloadMass',y='Orbit',data=df, hue='Class',aspect=2,alpha=0.7)
plt.show


# *->With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.However for GTO we cannot distinguish this well as both positive landing rate and negative landing(unsuccessful mission) are both there here.*

# #### 6. Visualize the launch success yearly trend

# In[180]:


# A function to Extract years from the date 
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()


# In[191]:


df3=df.groupby(['Date'])['Class'].mean().reset_index()
df3.head()


# In[206]:


plt.figure(figsize=(12,4))
sns.lineplot(x='Date',y='Class',data=df3, color ='red')
plt.xlabel('Year',fontsize=12)
plt.ylabel('Successful rate', fontsize=12)
plt.title('Launch success by year',fontsize=16)
plt.show


# *->The sucess rate since 2013 kept increasing till 2020*

# #### 7. Create dummy variables to categorical columns

# In[210]:


features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()


# In[221]:


features_one_hot = pd.get_dummies(features,columns = ['Orbit','LaunchSite','Serial','LandingPad'])
features_one_hot.head()


# In[222]:


df_f.dtypes


# #### 8. Cast all numeric columns to `float64`

# In[227]:


features_one_hot.astype('float').dtypes


# In[234]:


features_one_hot.to_csv('/Users/QXJ/Desktop/IBM/SpaceX/dataset_part_3.csv', index=False)

