#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 14:08:14 2022

@author: chethantulsidas
"""

import pandas as pd

def percent(x, y):
    return round((x/y)*100)

def avg(x,y):
    return round(x/y,2)

def leaguestats(data, league, season):
    
    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass
    
    print("\n\nStatistcs for {0} {1}/{2}".format(league, season, (season+1)%100))
    league = league.lower()
    homeWins = awayWins = draw = goals = homeGoals = awayGoals = over = under = 0
    data = data[(data["league"] == league) & (data["season"] == season)]
    #print(data.sample())
    #print("")
    matchnum = len(data.index)
    
    for i, record in data.iterrows():
        #print(record)
        #print(type(record))
        homeScore = int(record["homeScore"])
        awayScore = int(record["awayScore"])
        goals = goals + homeScore + awayScore
        homeGoals = homeGoals + homeScore
        awayGoals = awayGoals + awayScore
        if (homeScore + awayScore) > 2.5:
            over = over + 1
        elif (homeScore + awayScore) < 2.5:
            under = under + 1
        if homeScore > awayScore:
            homeWins = homeWins + 1
        elif awayScore > homeScore:
            awayWins = awayWins + 1
        elif homeScore == awayScore:
            draw = draw + 1
    
    print("\n--------------------------------------------")
    print(f"\n{'Matches played : ':<20}{matchnum:>5}")
    print(f"\n{'Home Wins : ':<20}{homeWins:>5}{percent(homeWins, matchnum):>5}{'%'}")
    print(f"{'Draws : ':<20}{draw:>5}{percent(draw, matchnum):>5}{'%'}")
    print(f"{'Away Wins : ':<20}{awayWins:>5}{percent(awayWins, matchnum):>5}{'%'}")
    print(f"\n{'Goals scored : ':<20}{goals:>5}{avg(goals, matchnum):>6}{' per match'}")
    print(f"{'Home Goals : ':<20}{homeGoals:>5}{avg(homeGoals, matchnum):>6}{' per match'}")
    print(f"{'Away Goals : ':<20}{awayGoals:>5}{avg(awayGoals, matchnum):>6}{' per match'}")
    print(f"\n{'Over 2.5 : ':<20}{over:>5}{percent(over, matchnum):>5}{'%'}")
    print(f"{'Under 2.5 : ':<20}{under:>5}{percent(under, matchnum):>5}{'%'}")
    print("\n--------------------------------------------")
    

    


def teamstats(data, league, season):
    print("\n\n")
    league = league.lower()
    teams = data[(data["league"] == league) & (data["season"] == season)]
    teams = list(teams["homeTeam"].unique())
    #print(type(teams))
    teams.sort()
    i = 0
    for team in teams:
        #print("{0}.{1}".format(i, team))
        i = i + 1
        print("{:<25}".format(str(i) + "." + team), end="")
        if (((i) % 4) == 0):
            print("\n")    
            
    print("")
    teams_choice = int(input("Pick a team : "))
    #print("\nYou have chosen", teams[teams_choice-1])
    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass
    
    team = teams[teams_choice-1]
    print("\n\nStatistics for {0} {1}/{2}".format(team, season, (season+1)%100))
    
    homeWins = awayWins = draw = goals = homeGoals = awayGoals = over = under = 0
    data_home = data[(data["league"] == league) & (data["season"] == season) & (data["homeTeam"] == team)]
    #print(data_home.sample())
    matchnum = len(data_home.index)
    for i, record in data_home.iterrows():
        #print(record)
        #print(type(record))
        homeScore = int(record["homeScore"])
        awayScore = int(record["awayScore"])
        goals = goals + homeScore + awayScore
        homeGoals = homeGoals + homeScore
        awayGoals = awayGoals + awayScore
        if (homeScore + awayScore) > 2.5:
            over = over + 1
        elif (homeScore + awayScore) < 2.5:
            under = under + 1
        if homeScore > awayScore:
            homeWins = homeWins + 1
        elif awayScore > homeScore:
            awayWins = awayWins + 1
        elif homeScore == awayScore:
            draw = draw + 1
    
    print("\n-------------------------------------------------")
    print(f"\n{'Home matches played : ':<25}{matchnum:>5}")
    print(f"\n{'Home Wins : ':<25}{homeWins:>5}{percent(homeWins, matchnum):>5}{'%'}")
    print(f"{'Draws : ':<25}{draw:>5}{percent(draw, matchnum):>5}{'%'}")
    print(f"{'Away Wins : ':<25}{awayWins:>5}{percent(awayWins, matchnum):>5}{'%'}")
    print(f"\n{'Goals scored : ':<25}{goals:>5}{avg(goals, matchnum):>6}{' per match'}")
    print(f"{'Home Goals : ':<25}{homeGoals:>5}{avg(homeGoals, matchnum):>6}{' per match'}")
    print(f"{'Away Goals : ':<25}{awayGoals:>5}{avg(awayGoals, matchnum):>6}{' per match'}")
    print(f"\n{'Over 2.5 : ':<25}{over:>5}{percent(over, matchnum):>5}{'%'}")
    print(f"{'Under 2.5 : ':<25}{under:>5}{percent(under, matchnum):>5}{'%'}")
    
    
    homeWins = awayWins = draw = goals = homeGoals = awayGoals = over = under = 0
    data_away = data[(data["league"] == league) & (data["season"] == season) & (data["awayTeam"] == team)]
    matchnum = len(data_home.index)
    for i, record in data_away.iterrows():
        #print(record)
        #print(type(record))
        homeScore = int(record["homeScore"])
        awayScore = int(record["awayScore"])
        goals = goals + homeScore + awayScore
        homeGoals = homeGoals + homeScore
        awayGoals = awayGoals + awayScore
        if (homeScore + awayScore) > 2.5:
            over = over + 1
        elif (homeScore + awayScore) < 2.5:
            under = under + 1
        if homeScore > awayScore:
            homeWins = homeWins + 1
        elif awayScore > homeScore:
            awayWins = awayWins + 1
        elif homeScore == awayScore:
            draw = draw + 1
    
    
    print("\n-------------------------------------------------")
    print(f"\n{'Away matches played : ':<25}{matchnum:>5}")
    print(f"\n{'Home Wins : ':<25}{homeWins:>5}{percent(homeWins, matchnum):>5}{'%'}")
    print(f"{'Draws : ':<25}{draw:>5}{percent(draw, matchnum):>5}{'%'}")
    print(f"{'Away Wins : ':<25}{awayWins:>5}{percent(awayWins, matchnum):>5}{'%'}")
    print(f"\n{'Goals scored : ':<25}{goals:>5}{avg(goals, matchnum):>6}{' per match'}")
    print(f"{'Home Goals : ':<25}{homeGoals:>5}{avg(homeGoals, matchnum):>6}{' per match'}")
    print(f"{'Away Goals : ':<25}{awayGoals:>5}{avg(awayGoals, matchnum):>6}{' per match'}")
    print(f"\n{'Over 2.5 : ':<25}{over:>5}{percent(over, matchnum):>5}{'%'}")
    print(f"{'Under 2.5 : ':<25}{under:>5}{percent(under, matchnum):>5}{'%'}")
    #print(data_away.sample())
    

    print("\n-------------------------------------------------")
    
    
filename = "data/england.csv"
data = pd.read_csv(filename)
league = "Premier League"
season = 2019

leaguestats(data, league, season)

#teamstats(data, league, season)