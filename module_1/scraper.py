# 4/20/2024
# This scraper crawls espn fight stats website to count up how many times a specified fighter has been taken down in the UFC


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox() #uncomment to debug with auutomated browser open


def findFighter(name: str):
    # use search bar to find fighters page url; %20 = " "
    fighterName = name.replace(" ", "%20").lower()
    url = f'https://www.espn.com/search/_/q/{fighterName}'
    driver.get(url)
    # wait for browser to load content
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/section[1]/div/ul/div'))
    )
    fighterUrl = element.find_element(By.TAG_NAME, "a").get_attribute("href")
    return fighterUrl


def numberOfTimesTakendown(name: str):
    # expand list of fighters fought
    fighterUrl = findFighter(name)
    fighterHistoryUrl = fighterUrl.replace('fighter', 'fighter/history')
    driver.get(fighterHistoryUrl)

    # wait for browser to load content
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/section/div/div/div/div/div[2]/table'))
    )

    table = table.find_element(By.TAG_NAME, 'tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    timesTakenDown = 0
    opponentUrls = []

    # crawl through each opponents stats, tally how many times they've taken down specified fighter
    print('counting...')
    for rowIndex in range(len(rows)):
        opponent = driver.find_element(
            By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/section/div/div/div/div/div[2]/table/tbody/tr[{rowIndex+1}]/td[2]/a')
        opponentUrl = opponent.get_attribute("href")

        event = driver.find_element(
            By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/section/div/div/div/div/div[2]/table/tbody/tr[{rowIndex+1}]/td[7]/*')
        # only consider oppenents fought in the UFC
        if "UFC" in event.text:
            opponentUrls.append(opponentUrl)

    for opponentUrl in opponentUrls:
        print(f'{opponentUrls.index(opponentUrl)+1}/{len(opponentUrls)}')
        # navigate to opponents stats
        statsUrl = opponentUrl.replace('fighter', 'fighter/stats')
        driver.get(statsUrl)
        try:  # check if opponent has stats up
            table = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/div[1]/section/div/div[3]/div[2]/div/div[2]/table'))
            )
        except Exception as e:
            print("opponent's ufc stats not availble.")
            continue

        table = table.find_element(By.TAG_NAME, 'tbody')
        opponentRows = table.find_elements(By.TAG_NAME, 'tr')
        for opponentRowIndex in range(len(opponentRows)):
            opponentsOpponent = driver.find_element(
                By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/div[1]/section/div/div[3]/div[2]/div/div[2]/table/tbody/tr[{opponentRowIndex+1}]/td[2]/a')
            # only tally specified fighter's fight
            if (opponentsOpponent.get_attribute('href') == fighterUrl):
                takedownAmmount = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/div[1]/section/div/div[3]/div[2]/div/div[2]/table/tbody/tr[{opponentRowIndex+1}]/td[13]')
                # clean any non integers in string
                numOnly = re.findall(r'\d+', takedownAmmount.text)
                numOnly = ''.join(numOnly)
                if numOnly:
                    timesTakenDown += int(numOnly)
    return timesTakenDown


print(numberOfTimesTakendown("khabib nurmagomedov"))
driver.quit()
