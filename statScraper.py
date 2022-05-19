from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

website = 'https://www.baseball-reference.com/'
path = './chromedriver'
driver = webdriver.Chrome(path)
driver.get(website)

#gets a teams stats as csv table
def getTeamStats(team):
    #from main page go to team page
    team_select = Select(driver.find_element(By.ID,'team_page_team_choice'))
    year_select = Select(driver.find_element(By.ID,'team_page_page_choice'))
    team_select.select_by_value("/teams/" + team.upper())
    year_select.select_by_value("/2022.shtml")

    go_btn = driver.find_element_by_xpath('//div[@id="teams"]/form/div[3]/div/input')
    #driver.find_element_by_id('go_button_907')
    driver.execute_script("arguments[0].click();", go_btn)

    #inside team page pull data from table

    rows = 28 #may bring errors find way to determine # of rows in table
    data_labels = []
    for col in range(1,rows):
        label = driver.find_element(By.XPATH,'//div[@id="div_team_batting"]/table[@id="team_batting"]/thead/tr/th[' + str(col) + "]")
        data_labels.append(label.get_dom_attribute("data-stat"))
    #print(data_labels) #table headers

    data = {}
    cols = 28
    for row in range(5):
        row_data = driver.find_element(By.XPATH,'//div[@id="div_team_batting"]/table[@id="team_batting"]/tbody/tr[@data-row=' + str(col) + "]")
        data_entry = []
        for entry in range(1,cols):
            col_data = row_data.find_element(By.XPATH,'.//td[' + str(entry) + "]")
            data_titles = col_data.get_dom_attribute("data-stat")
            if data_titles == 'player':
                name = col_data.text
            data_entry.append((data_titles, col_data.text))
        data[name] = data_entry
        print(data)
        #for entry in row_data.find_element_by_xpath('.//td'):
        #    print(entry.get_dom_attribute("data-stat"))

    driver.quit()

getTeamStats('tex')