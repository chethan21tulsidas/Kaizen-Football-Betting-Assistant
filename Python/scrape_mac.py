#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 17:38:17 2022

@author: chethantulsidas
"""


import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from os import path, makedirs



countries = {1: "England", 2: "Spain", 3: "Germany", 4: "Italy", 5: "France"}

leagues = {1: {1: "Premier League", 2: "Championship", 3: "League One", 4: "League Two"}, 
           2: {1: "LaLiga", 2: "LaLiga2"}, 
           3: {1: "Bundesliga", 2: "2. Bundesliga", 3: "3. Liga"}, 
           4: {1: "Serie A", 2: "Serie B"}, 
           5: {1: "Ligue 1", 2: "Ligue 2", 3: "National"}}


example = "https://www.betexplorer.com/soccer/england/premier-league-2021-2022/results/"

baseurl = "https://www.betexplorer.com/soccer/"

pd.set_option('display.max_columns', None)

file = "global"

def checkdata(country, datapath= "data/"):
    country = country.lower()
    filename = datapath + country + ".csv"
    #print("\n" + filename)
    flag=-1
    if not path.isfile(filename):
        return flag, filename
    else:
        data = pd.read_csv(filename, index_col=0, parse_dates=True)
        min = data["season"].min()
        return min, filename
    
    
def get_data(country_choice, filename, choice="y"):
    country = countries[country_choice]
    if choice == "y" or choice == "Y":
        data = pd.DataFrame()
        start_season = int(input("Pick a start season (yyyy) : "))
        #print("")
        for i, league in leagues[country_choice].items():
            for s in range(start_season, current_season):
                #print(league, s)
                comp_data = scrapeseason(country, league, s)
                data = data.append(comp_data)
                print(data.shape)
                #print(comp_data.shape)
                #data = data.append(comp_data)
                #print(data.shape)
                #print("Get Competition Data")
        data.sort_values(['date', 'homeTeam'], ascending=[False, True], inplace=True)
        data.reset_index(inplace=True, drop=True)
        #print("")
        #print(data.sample())
        data.to_csv(filename, index = False)
        data = pd.read_csv(filename)
    else:
        data = pd.read_csv(filename)
    print("")
    print("Records size : {0}".format(data.shape))
    return data
    #print(data.sample())




def scrapeseason(country, comp, season):
        # output what the function is attempting to do.
    print("\nScraping : ", country, comp, str(season) + "-" + str(season + 1))
    
    country = country.lower()
    comp = comp.lower()

    baseurl = "https://www.betexplorer.com/soccer/"
    scrapeaddress = (baseurl + country + "/" + comp.replace(" ", "-").replace(".", "") + "-"
                     + str(season) + "-" + str(season + 1) + "/results/")
    print("URL : ", scrapeaddress)
    #print("")

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
        
        #print("{0} {1} - {2} {3} | {4}".format(home_team, home_goals, away_goals, away_team, date.date()))
        
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
    #print(df.shape)
    return df

