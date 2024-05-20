from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json


options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
url = 'https://en.wikipedia.org/wiki/List_of_current_UFC_fighters'
driver.get(url)



#table 1 (fly weight - welter weight)
table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[5]')))
table = table.find_element(By.TAG_NAME, 'tbody')
rankingHeaders = table.find_elements(By.TAG_NAME, 'th')
rankingRows = table.find_elements(By.TAG_NAME, 'tr')

#populate fighter dictionary
fighters = {}
for headerIndex in range(1, len(rankingHeaders)): #start at 2 to ignore edge column and pound for pound column
    fighters[rankingHeaders[headerIndex].text] = []
    for rowIndex in range(1, len(rankingRows)):
        rowData = rankingRows[rowIndex].find_elements(By.TAG_NAME, 'td')
        if headerIndex == 1 and rowIndex == 1: #ignore champion cell for Mens pound for pound column
            continue
        fighters[rankingHeaders[headerIndex].text].append(re.sub(r'\d+|\(.*?\)', '', rowData[headerIndex].text))#remove parenthesis and numbers

# #table 2 (middle weight - women's bantam weight)
table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[6]')))
table = table.find_element(By.TAG_NAME, 'tbody')
rankingHeaders = table.find_elements(By.TAG_NAME, 'th')
rankingRows = table.find_elements(By.TAG_NAME, 'tr')

#populate fighter dictionary
for headerIndex in range(1, len(rankingHeaders)): #start at 2 to ignore edge column and pound for pound column
    fighters[rankingHeaders[headerIndex].text] = []
    for rowIndex in range(1, len(rankingRows)):
        rowData = rankingRows[rowIndex].find_elements(By.TAG_NAME, 'td')
        if headerIndex == 4 and rowIndex == 1: #ignore champion cell for Womens pound for pound column
            continue
        fighters[rankingHeaders[headerIndex].text].append(re.sub(r'\d+|\(.*?\)', '', rowData[headerIndex].text))

#save data
with open('fighters.json', 'w') as file:
    json.dump(fighters, file, indent=4)
    