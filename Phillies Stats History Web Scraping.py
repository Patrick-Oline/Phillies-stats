#!/usr/bin/env python
# coding: utf-8

# In[1]:
### Stats for batting scaped from baseball-reference.com ###

import requests
import pandas as pd
from bs4 import BeautifulSoup, Comment


# In[2]:

bat_stats_url = "https://www.baseball-reference.com/teams/PHI/batteam.shtml"

data_b = requests.get(bat_stats_url)

soup = BeautifulSoup(data_b.text)

bat_stats_table = soup.select('table.stats_table')[0]

bat_year_stats = pd.read_html(data_b.text, match = 'Year-by-Year Team Batting')

bat_year_stats[0]

bat = bat_year_stats[0]

bat.shape


# In[3]:

### Scraping batting table 2

soup = BeautifulSoup(requests.get('https://www.baseball-reference.com/teams/PHI/batteam.shtml').text)

bat_per_game = pd.read_html([x.extract() for x in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="yby_team_bat_per_game"' in x][0])[0]

bat_per_game

### Stats for pitching scaped from baseball-reference.com ###

pitch_stats_url = "https://www.baseball-reference.com/teams/PHI/pitchteam.shtml"

data_p = requests.get(pitch_stats_url)

soup = BeautifulSoup(data_p.text)

pitch_stats_table = soup.select('table.stats_table')[0]

pitch_year_stats = pd.read_html(data_p.text, match = 'Year-by-Year Team Pitching')

pitch = pitch_year_stats[0]

pitch


# In[4]:

pitch.rename(columns = {'H' : 'H_A', 'R' : 'R_A', 'HR':'HR_A', 'BB':'BB_A', 'SO':'Ks'}, inplace = True)


# In[5]:

### Scraping pitching table 2

soup = BeautifulSoup(requests.get('https://www.baseball-reference.com/teams/PHI/pitchteam.shtml').text)

pitch_per_game = pd.read_html([x.extract() for x in soup.find_all(string=lambda text: isinstance(text, Comment)) if 'id="yby_team_pitch_per_game"' in x][0])[0]

pitch_per_game


# In[6]:

pitch_per_game.rename(columns = {'H' : 'H_A', 'R' : 'R_A', 'HR':'HR_A', 'BB':'BB_A', 'SO':'Ks'}, inplace = True)


pitch_per_game


# In[7]:

### Combinding two tables

pitch.columns.values.tolist()

bat.columns.values.tolist()

team_data = bat.merge(pitch[['Year','RA/G','ERA','CG','tSho','SV','IP',
                              'H_A','R_A','ER','HR_A','BB_A','Ks','WHIP','SO9','HR9','PAge']],on='Year')

team_data.shape

team_data.columns = [c.upper() for c in team_data.columns]

team_data = team_data.drop(labels=0, axis=0)

team_data = team_data.drop(columns="LG")

team_data


# In[8]:


team_name = bat_stats_url.split("/")[-2]

team_name

team_data.insert(0, 'TEAM', team_name)


team_data


# In[9]:

### Combined 2 per game tables

team_per_game = bat_per_game.merge(pitch_per_game[['Year','RA/G','ERA','CG','tSho','SV','IP',
                              'H_A','R_A','ER','HR_A','BB_A','Ks','WHIP','SO9','HR9','PAge']],on='Year')


team_per_game.columns = [c.upper() for c in team_per_game.columns]

team_per_game = team_per_game.drop(labels=0, axis=0)

team_per_game = team_per_game.drop(columns="LG")

team_per_game.insert(0, 'TEAM', team_name)

team_per_game


# In[10]:

phillies_stats = team_data

per_game_phillies = team_per_game


# In[11]:

phillies_stats.to_csv("phillies_stats.csv")

per_game_phillies.to_csv('per_game_phillies')