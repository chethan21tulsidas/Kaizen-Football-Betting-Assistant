#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 22:16:37 2022

@author: chethantulsidas
"""



import argparse
import datetime
import matplotlib.pyplot as plt
import os

from os import path, makedirs

import numpy as np
import pandas as pd
import requests


from bs4 import BeautifulSoup as bs
from scipy.stats import poisson,skellam

pd.set_option('display.max_columns', None)

def scrapeseason(country, comp, season):
        # output what the function is attempting to do.
    print("Scraping : ", country, comp, str(season) + "-" + str(season + 1))
    
    country = country.lower()
    comp = comp.lower()

    baseurl = "https://www.betexplorer.com/soccer/"
    scrapeaddress = (baseurl + country + "/" + comp.replace(" ", "-").replace(".", "") + "-"
                     + str(season) + "-" + str(season + 1) + "/results/")
    print("URL : ", scrapeaddress)
    print("")

    # scrape the page and create beautifulsoup object
    content = requests.get(scrapeaddress).text
    page = bs(content, "html.parser")
    

    #for table in page.find_all('table'):
    #   print(table.get("class"))

    # find the main data table within the page source
    maintable = page.find("table", "table-main")

    # seperate the data table into rows
    games = maintable.find_all("tr")

    # create an empty pandas dataframe to store our data
    df = pd.DataFrame(columns=["date", "homeTeam", "homeScore", "awayScore", "awayTeam"])

    idx = 0
    today = datetime.date.today()
    
    
    #game = games[1]
    #print(game.prettify())
    
    #print(game.get_text(" ").split())
    #print(game.find("td", "h-text-left").text)
    #print(game.find("td", "h-text-center").text)
    #print(game.find("td", "h-text-right").text)
    #print("")
    
    #teams = game.find("td", "h-text-left").text
    #score = game.find("td", "h-text-center").text
    #date = game.find("td", "h-text-right").text

    for game in games:
        text = game.get_text(" ")
        if "Round" in text.split():
            #print("\nRound Skipped\n")
            continue
        #print(text)
        try:
            teams = game.find("td", "h-text-left").text
            score = game.find("td", "h-text-center").text
            date = game.find("td", "h-text-right").text
        except:
            continue
        
        if "CAN." in score:
            continue
        
        if " AWA." in score:
            score = score.replace(" AWA.", "")
            
        
        if date[-1] == ".":
            date = date + "2022"
            
        date = date.replace(".", "/")
        
        format_str = '%d/%m/%Y'
        date = datetime.datetime.strptime(date, format_str)
        #print(type(date.date()))
        #print(date.date())
        
        
        #print("Teams : {0} | Score : {1} | Date : {2}".format(teams, score, date))
        teams = teams.split(" - ")
        score = score.split(":")
        #print(teams)
        #print(score)
        
        home_team = teams[0]
        away_team = teams[1]
        
        home_goals = score[0]
        away_goals = score[1]
        
        print("{0} {1} - {2} {3} | {4}".format(home_team, home_goals, away_goals, away_team, date.date()))
        
        df.loc[idx] = {"date": date,
                       "homeTeam": home_team,
                       "homeScore": int(home_goals),
                       "awayScore": int(away_goals),
                       "awayTeam": away_team}
         # update our index
        idx += 1

    # sort our dataframe by date
    df.sort_values(['date', 'homeTeam'], ascending=[True, True], inplace=True)
    df.reset_index(inplace=True, drop=True)
    # add a column containing the season, it'll come in handy later.
    df["season"] = season
    df["country"] = country
    df["league"] = comp
    return df


country = "France"
league = "Ligue 1"
season = 2011

data = scrapeseason(country, league, season)

print(data.shape)

print(data.sample())