from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

def getTeamStats(team):
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
