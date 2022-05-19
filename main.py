from matplotlib.font_manager import json_dump
import statScraper as ss
import json

teams_east = ['nyy','tbr','tor','bal','bos','nym','phi','atl','mia','wsn']
teams_central = ['min','chw','cle','kcr','det','mil','stl','pit','chc','cin']
teams_west = ['hou','laa','sea','tex','oak','lad','sdp','sfg','ari','col']
stats_east = {}
stats_central = {}
stats_west = {}

for team in teams_east:
    stats_east[team] = ss.getTeamStats(team)

for team in teams_central:
    stats_central[team] = ss.getTeamStats(team)

for team in teams_west:
    stats_west[team] = ss.getTeamStats(team)

with open('baseball_data.txt', 'w') as convert_file:
    convert_file.write(json.dumps(stats_east | stats_central | stats_west))