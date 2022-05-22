from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import json

def getTeamBatting(team):
    website = 'https://www.baseball-reference.com/'
    path = './chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(website)
    team_select = Select(driver.find_element(By.ID,'team_page_team_choice'))
    year_select = Select(driver.find_element(By.ID,'team_page_page_choice'))
    team_select.select_by_value("/teams/" + team.upper())
    year_select.select_by_value("/2022.shtml")

    go_btn = driver.find_element(By.XPATH, '//div[@id="teams"]/form/div[3]/div/input')
    driver.execute_script("arguments[0].click();", go_btn)

    data = {}
    rows = driver.find_elements(By.XPATH, '//div[@id="div_team_batting"]/table[@id="team_batting"]/tbody/tr')
    for row in range(len(rows)):
        cols = rows[row].find_elements(By.XPATH, './/td')
        current_player_data = []
        for col in range(len(cols)):
            data_label = cols[col].get_dom_attribute("data-stat")
            data_value = cols[col].text
            if data_label == "player":
                name = data_value
            current_player_data.append((data_label, data_value))
        data[name] = current_player_data
    driver.quit()
    return data

def getTeamPitching(team):
    website = 'https://www.baseball-reference.com/'
    path = './chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(website)
    team_select = Select(driver.find_element(By.ID,'team_page_team_choice'))
    year_select = Select(driver.find_element(By.ID,'team_page_page_choice'))
    team_select.select_by_value("/teams/" + team.upper())
    year_select.select_by_value("/2022.shtml")

    go_btn = driver.find_element(By.XPATH, '//div[@id="teams"]/form/div[3]/div/input')
    driver.execute_script("arguments[0].click();", go_btn)

    data = {}
    rows = driver.find_elements(By.XPATH, '//div[@id="all_team_pitching"]//table[@id="team_pitching"]/tbody/tr')   
    for row in range(len(rows)):
        cols = rows[row].find_elements(By.XPATH, './/td')
        current_player_data = []
        for col in range(len(cols)):
            data_label = cols[col].get_dom_attribute("data-stat")
            data_value = cols[col].text
            if data_label == "player":
                name = data_value
            current_player_data.append((data_label, data_value))
        data[name] = current_player_data
    driver.quit()
    return data

def getTeamRecords():
    website = 'https://www.baseball-reference.com/'
    path = './chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(website)
    data_table_AL = driver.find_element(By.XPATH, '//table[@id="standings_AL"]/tbody')
    data_table_NL = driver.find_element(By.XPATH,'//table[@id="standings_NL"]/tbody')

    data = {}
    rows = data_table_AL.find_elements(By.XPATH, './/tr') + data_table_NL.find_elements(By.XPATH, './/tr')
    for row in range(len(rows)):
        team = "Team not found"
        team_col = rows[row].find_element(By.XPATH, './/th')
        if team_col.get_dom_attribute("data-stat") == "team_ID":
            team = team_col.text
        else:
            continue
        cols = rows[row].find_elements(By.XPATH, './/td')
        current_data = []
        for col in range(len(cols)):
            data_label = cols[col].get_dom_attribute("data-stat")
            data_value = cols[col].text
            current_data.append((data_label,data_value))
        data[team] = current_data
    driver.quit()
    return data

def getSchedule():
    website = 'https://www.baseball-reference.com/leagues/MLB-schedule.shtml'
    path = './chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(website)

    records = {}

    all_matchups = driver.find_element(By.XPATH, '//div[@class="section_content"]')
    daily_matchups = all_matchups.find_elements(By.XPATH, './/div')
    for entry in range(1):#range(len(daily_matchups)):
        #code works for range up to "today"
        #find way to update games from previously selected date up to today (last day in dataset? to today)
        date = daily_matchups[entry].find_element(By.XPATH,'.//h3').text
        games = daily_matchups[entry].find_elements(By.XPATH, './/p[@class="game"]')

        results = []
        for game in range(len(games)):
            result = games[game].text
            result = result.strip('  Boxscore').split(' @ ')

            away = result[0]
            home = result[1]

            awaylist = away.split(' (')
            away_team = awaylist[0]
            away_score = awaylist[1].replace(')', '')
            homelist = home.split(' (')
            home_team = homelist[0]
            home_score = homelist[1].replace(')', '')
            
            result = {'Away': {away_team: away_score, 'Home': {home_team: home_score}}}
            results.append(result)
        records[date] = results

    with open('baseball_schedule.txt', 'w') as file:
        file.write(json.dumps(records, indent=4, sort_keys=True))

    driver.quit()


teams_east = ['nyy','tbr','tor','bal','bos','nym','phi','atl','mia','wsn']
teams_central = ['min','chw','cle','kcr','det','mil','stl','pit','chc','cin']
teams_west = ['hou','laa','sea','tex','oak','lad','sdp','sfg','ari','col']

all_teams = teams_central + teams_west + teams_east

#Slow implementation speed up with following improvements
# 1) get batting data and pitching data from single website visit
# 2) instead of closing page between team searches go to previous webpage (homepage)
# 3) Possibly reduce amount of data / webelements received only get absolute necessary data
def updateAllData():
    total_stats = {}

    team_records = getTeamRecords()

    for team in all_teams:
        team = team.upper()
        record = dict(team_records[team])
        total_stats = {}
        batting = {}
        pitching = {}

        for player, data in getTeamBatting(team).items():
            batting[player] = dict(data)

        for player, data in getTeamPitching(team).items():
            pitching[player] = dict(data)
        
        total_stats[team] = {'Record': record, 'Team_Batting': batting, 'Team_Pitching': pitching}

    with open('baseball_data.txt', 'w') as convert_file:
        convert_file.write(json.dumps(total_stats, indent=4, sort_keys=True))

def updateData(team):
    team = team.upper()
    pitching = {}
    batting = {}
    records = getTeamRecords()
    with open('baseball_data.txt', 'r') as file:
        data = json.load(file)

    for player, data in getTeamBatting(team).items():
            batting[player] = dict(data)

    for player, data in getTeamPitching(team).items():
        pitching[player] = dict(data)

    updatedData = {}
    updatedData[team] = {'Record': dict(records[team]), 'Team_Batting': batting, 'Team_Pitching': pitching}
    
    data[team] = updatedData[team]
    with open('baseball_data.txt', 'w') as testfile:
        testfile.write(json.dumps(updatedData, indent=4, sort_keys=True))


getSchedule()