from leagueDashboardProject.apps.dataQueries import leagueParser as lp
from re import search
import mwclient
from datetime import date 
current_year = date.today().year

""" This will pull the default page
        it  will consist of the following:
            1. Standing per region
            2. Historical Standing per region 
"""
def layoutStandingsPage(): 
    search_dictionary = lp.searches()
    default_dic = {}
    default_tournament = ['LCS','LCK','LPL','LEC']
    default_regions = ['North America','Korea','China','Europe']
    for tournament_keys in default_regions:
        default_dic[tournament_keys] = []
    for keys in search_dictionary['Regions'].keys():
        if keys in ['North America','Europe', 'China','Korea']:
            for tournament in search_dictionary['Regions'][keys]:
                for i in default_tournament:
                    if search(i, tournament):
                        default_dic[keys].append(tournament)
    default_standings = {}
    for keys in default_dic.keys():
       default_standings[keys] = lp.defaultStandings(default_dic[keys][0]) 
    return default_standings

def layoutHistoricalPage(dict = layoutStandingsPage()):
    default_historical = {}
    for keys in dict.keys():
        default_historical[keys] = lp.defaultHistoricalStanding(dict[keys]['Event'][0])
    columns = ['Barons','Dragons','Gold','RiftHeralds','Kills']
    return default_historical, columns


def statsLayoutPage(dict = layoutStandingsPage()):
    default_stats = {}
    print(dict)
    for keys in dict.keys():
        default_stats[keys] = lp.statsDataFrames(dict[keys]['Event'][0])
    return default_stats


def searches():
    regionSearchDic = lp.searches()['Regions']
    playoffsSearchDic = lp.searches()['PlayOffs']
    return regionSearchDic, playoffsSearchDic

layoutStandingsPage()