import re
import mwclient
import pandas as pd 
import numpy as np
import datetime as dt
from datetime import date, timedelta, datetime
from leagueDashboardProject import tidydata as td
import sys

date = datetime.date(datetime.now())
site  = mwclient.Site('lol.gamepedia.com', path = '/')
    
def searches():
    response = site.api('cargoquery',
                        limit = 'max',
                        tables = 'Tournaments = TN',
                        fields = "TN.Name, TN.Region, TN.Year, TN.IsOfficial, TN.IsQualifier, TN.IsPlayoffs, TN.Split, TN.SplitNumber, TN.DateStart",
                        where = 'TN.Year = "2020" AND TN.IsOfficial = 1 AND TN.DateStart <= "{} 00:00:00"'.format(str(date)),
                        order_by = 'TN.DateStart DESC')

    search_dictionary = {'Regions':{}, 'Qualifiers':[],'PlayOffs':[]}

    for dictionary in response['cargoquery']:
        if dictionary['title']['Region'] in search_dictionary['Regions']:
            pass
        else:
            search_dictionary['Regions'][dictionary['title']['Region']] = [] 
        
        if dictionary['title']['Region'] in list(search_dictionary['Regions'].keys()):
            search_dictionary['Regions'][dictionary['title']['Region']].append(dictionary['title']['Name'])
        if dictionary['title']['IsQualifier'] == "1":
                search_dictionary['Qualifiers'].append(dictionary['title']['Name'])
        
        if dictionary['title']['IsPlayoffs'] == "1":
                search_dictionary['PlayOffs'].append(dictionary['title']['Name'])
    return search_dictionary 

def defaultStandings(tournament = None):
    try: 
        defaultStanding = site.api('cargoquery',
                                        limit = 'max',
                                        tables = 'TournamentResults = TNR',
                                        fields = "TNR.Event,TNR.Place_Number,TNR.Team,TNR.UniqueLine",
                                        where = 'TNR.Event="{}"'.format(tournament)

                                    )
        standings = {}
        teams = 0 
        headers_standings = ['Event', 'Team', 'Place','UniqueLine']
        for team in defaultStanding['cargoquery']:
            standings[teams] = []
            standings[teams].append(team['title']['Event'])
            standings[teams].append(team['title']['Team'])
            standings[teams].append(team['title']['Place Number'])
            standings[teams].append(team['title']['UniqueLine'])
            teams += 1
        standings_df = pd.DataFrame.from_dict(standings, orient = 'index', columns = headers_standings)
        return standings_df
    except TypeError:
        print('Please Select the Tournament Standing you Would like to View')
        pass
    
def defaultHistoricalStanding(tournament = None):
    """
        Makes Historical Standing of regions
        Try the table ScoreboardGame
    """
    try:            
        defaultHistoricalStanding = site.api('cargoquery',
                                                limit = 'max',
                                                tables = 'ScoreboardGame = SG',
                                                fields = 'SG.Tournament, SG.Team1, SG.Team2, SG.WinTeam, SG.LossTeam,SG.Team1Score, SG.Team2Score, SG.Winner,SG.UniqueGame, SG.ScoreboardID_Wiki, SG.Gamename, SG.DateTime_UTC, SG.Team1Gold, SG.Team2Gold, SG.Team1Kills, SG.Team2Kills, SG.Team1RiftHeralds, SG.Team2RiftHeralds, SG.Team1Dragons, SG.Team2Dragons, SG.Team1Barons, SG.Team2Barons, SG.Team1Towers, SG.Team2Towers, SG.Team1Inhibitors, SG.Team2Inhibitors',
                                                where = 'SG.Tournament="{}"'.format(tournament)
                                                )        
    except TypeError:
        print >> sys.stderr, 'Tournament Could not be found'
        print >> sys.stderr, 'Please Pick another Tournament'
        sys.exit(1)
    games = []
    for order_dic in defaultHistoricalStanding['cargoquery']:
        for rows in order_dic:
            row_dict = {}
            for keys in order_dic['title'].keys():
                row_dict.update({keys : order_dic['title'][keys]})
            games.append(row_dict)
    games_df = pd.DataFrame(games)
    games_df = pd.melt(games_df, id_vars = games_df.columns.difference(['Team1','Team2']),
                 value_vars=['Team1','Team2'], var_name = 'Side', value_name = "Team")
    id_vars = list(games_df.columns.values) 
    games_df = td.superMelt(games_df,id_vars, [['Team1Barons','Team2Barons'],['Team1Dragons','Team2Dragons'],['Team1Gold','Team2Gold'],
                                        ['Team1Inhibitors','Team2Inhibitors'],['Team1Kills','Team2Kills'],['Team1RiftHeralds','Team2RiftHeralds'],
                                        ['Team1Score','Team2Score'],['Team1Towers','Team2Towers']],
                                        ['SideBarons','SideDragons','SideGold','SideInhibitors','SideKills','SideRiftHeralds','SideScore','SideTowers'],
                                       ['Barons','Dragons','Gold','Inhibitors','Kills','RiftHeralds','Score','Towers'])
    games_df['Side'] = games_df['Side'].map({'Team1':'Blue', 'Team2':'Red'})
    games_df['Winner'] = np.where(games_df['Winner']=='1', 'Blue', 'Red')
    games_df['Won'] = np.where(games_df['Side']==games_df['Winner'], '1', '0')
    games_df['TeamAgaints'] = np.where(games_df['WinTeam']==games_df['Team'], games_df['LossTeam'], games_df['WinTeam'])
    del games_df['WinTeam']
    del games_df['UniqueGame']
    del games_df['LossTeam']
    del games_df['DateTime UTC__precision']
    games_df = games_df.sort_values(by=['DateTime UTC'])
    games_df = games_df.reset_index()
    del games_df['index']
    for convert_columns in list(games_df.columns):
        if convert_columns in ['Barons','Dragons','Gold','RiftHeralds','Kills']:
            games_df[convert_columns] = pd.to_numeric(games_df[convert_columns])    
    return games_df

def statsDataFrames(tournament = None):
    try:
        statsQuery = site.api('cargoquery',
                                limit = 'max',
                                tables = 'PicksAndBansS7 = PB, MatchScheduleGame = MSG, ScoreboardGame = SG',
                                fields = '',
                                where = 'SG.Tournament="{}"'.format(tournament),
                                join_on = 'PB.GameID_Wiki = MSG.GameID_Wiki, MSG.ScoreboardID_Wiki = SG.ScoreboardID_wiki'
                                )

    except TypeError:
        print('Please Select a Tournament to look for')
