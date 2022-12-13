#!/usr/bin/env python
# coding: utf-8

# ## Overview of the DataSet
# 
# SpaceX has gained worldwide attention for a series of historic milestones.
# 
# It is the only private company ever to return a spacecraft from low-earth orbit, which it first accomplished in December 2010.
# SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars wheras other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage.
# 
# Therefore if we can determine if the first stage will land, we can determine the cost of a launch.
# 
# This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.
# 
# This dataset includes a record for each payload carried during a SpaceX mission into outer space.

# In[1]:


get_ipython().system('pip3 install sqlalchemy')


# In[6]:


get_ipython().system('pip3 install ipython-sql')


# ### Connect to the database
# 
# Let us first load the SQL extension and establish a connection with the database

# In[71]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[72]:


import csv, sqlite3


# In[9]:


con = sqlite3.connect("my_data1.db")
cur = con.cursor()


# In[73]:


import numpy as np
import pandas as pd


# In[12]:


get_ipython().run_line_magic('sql', 'sqlite:///my_data1.db # sql connect to database')


# In[74]:


path = "/Users/QXJ/Desktop/IBM/SpaceX/Spacex.csv"
df = pd.read_csv(path, index_col = False)
df.head()


# In[75]:


# Reset index as columns 
df.reset_index(inplace=True)


# In[76]:


df.rename(columns = {'Landing _Outcome':'Landing_Outcome'}, inplace = True)


# In[77]:


df.columns


# In[78]:


df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")


# In[79]:


get_ipython().run_line_magic('sql', 'SELECT * FROM SPACEXTBL LIMIT 5;')


# In[80]:


get_ipython().run_line_magic('sql', 'SELECT DISTINCT Landing_Outcome from SPACEXTBL;')


# ### Write and execute SQL queries

# #### 1. Display the names of the unique launch sites  in the space mission

# In[81]:


get_ipython().run_line_magic('sql', 'SELECT DISTINCT Launch_Site FROM SPACEXTBL;')


# #### 2.Display 5 records where launch sites begin with the string 'CCA'

# In[88]:


get_ipython().run_line_magic('sql', "SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;")


# #### 3.Display the total payload mass carried by boosters launched by NASA (CRS)

# In[90]:


get_ipython().run_line_magic('sql', "SELECT SUM(PAYLOAD_MASS__KG_) AS total_payload FROM SPACEXTBL WHERE Customer LIKE 'NASA (CRS)';")


# #### 4.Display average payload mass carried by booster version F9 v1.1

# In[92]:


get_ipython().run_line_magic('sql', "SELECT avg(PAYLOAD_MASS__KG_) AS Avg_Payload FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1';")


# #### 5. List the date when the first succesful landing outcome in ground pad was acheived.

# In[102]:


get_ipython().run_line_magic('sql', "SELECT min(date) AS Early_Date from SPACEXTBL where Landing_Outcome LIKE 'Success (ground pad)'")


# #### 6. List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000

# In[99]:


get_ipython().run_line_magic('sql', "SELECT DISTINCT Customer, Landing_Outcome,PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome ='Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;")


# #### 7. List the total number of successful and failure mission outcomes

# In[103]:


get_ipython().run_line_magic('sql', 'SELECT Mission_Outcome, Count(*) AS Numbers FROM SPACEXTBL GROUP BY Mission_Outcome;')


# #### 8.List the names of the booster_versions which have carried the maximum payload mass. 

# In[98]:


get_ipython().run_line_magic('sql', 'SELECT Booster_Version, Max_Payload FROM (SELECT Booster_Version, MAX(PAYLOAD_MASS__KG_) AS Max_Payload FROM SPACEXTBL GROUP BY Booster_Version) AS Sub;')


# #### 9. List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
# 
# **Note: SQLLite does not support monthnames. So you need to use  substr(Date, 4, 2) as month to get the months and substr(Date,7,4)='2015' for year.**

# In[105]:


get_ipython().run_line_magic('sql', "SELECT SUBSTR(Date,4,2) AS Month, Booster_Version, Launch_site FROM SPACEXTBL WHERE Landing_Outcome LIKE 'Failure%drone%' AND SUBSTR(Date,7,4) = '2015'")


# #### 10. Rank the  count of  successful landing_outcomes between the date 04-06-2010 and 20-03-2017 in descending order.

# In[111]:


get_ipython().run_line_magic('sql', "SELECT Landing_Outcome, COUNT(*) AS Numbers FROM SPACEXTBL WHERE Landing_Outcome LIKE 'Success%' AND Date BETWEEN '04-06-2010' AND '20-03-2017' GROUP BY Landing_Outcome ORDER BY Numbers DESC;")


# In[ ]:




