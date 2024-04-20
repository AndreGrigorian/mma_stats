from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox()


# This scraper scrapes espn fighter stats website to count up how many times a specified fighter has been taken down in the UFC

def findFighter(name: str):
    fighterName = name.replace(" ", "%20").lower()
    url = f'https://www.espn.com/search/_/q/{fighterName}'
    driver.get(url)
    time.sleep(3)  # wait for browser to load content

    element = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/section[1]/div/ul/div')
    fighterUrl = element.find_element(By.TAG_NAME, "a").get_attribute("href")
    return fighterUrl


def numberOfTimesTakendown(name: str):
    # expand list of fighters fought
    fighterUrl = findFighter(name)
    driver.get(fighterUrl)
    time.sleep(2)
    seeAllButton = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[2]/div[1]/section/header/div[2]/a/div')
    seeAllButton.click()

    table = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/section/div/div/div/div/div[2]/table')
    table = table.find_element(By.TAG_NAME, 'tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    timesTakenDown = 0
    opponentUrls = []

    # crawl through each opponents stats, tally how many times they've taken down specified fighter
    print('counting...')
    for rowIndex in range(len(rows)):
        time.sleep(1)
        opponent = driver.find_element(
            By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/section/div/div/div/div/div[2]/table/tbody/tr[{rowIndex+1}]/td[2]/a')
        opponentUrl = opponent.get_attribute("href")
        # only consider oppenents fought in the UFC
        # if "ufc" in driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/section/div/div/div/div/div[2]/table/tbody/tr[{rowIndex+1}]/td[7]/a').text.lower():
        opponentUrls.append(opponentUrl)

    for opponentUrl in opponentUrls:
        print(f'{opponentUrls.index(opponentUrl)}/{len(opponentUrls)}')
        # navigate to opponents stats
        statsUrl = opponentUrl.replace('fighter', 'fighter/stats')
        driver.get(statsUrl)
        time.sleep(2)
        try:  # check if opponent has stats up
            table = driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/div[1]/section/div/div[3]/div[2]/div/div[2]/table')
        except Exception as e:
            print(e)
            continue

        table = table.find_element(By.TAG_NAME, 'tbody')
        opponentRows = table.find_elements(By.TAG_NAME, 'tr')
        for opponentRowIndex in range(len(opponentRows)):
            OpponentsOpponent = driver.find_element(
                By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/div[1]/section/div/div[3]/div[2]/div/div[2]/table/tbody/tr[{opponentRowIndex+1}]/td[2]/a')
            # only tally specified fighter's fight
            if (OpponentsOpponent.get_attribute('href') == fighterUrl):
                takedownAmmount = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div/div/div/div/main/div[2]/div[5]/div/div[1]/div[1]/section/div/div[3]/div[2]/div/div[2]/table/tbody/tr[{opponentRowIndex+1}]/td[13]')
                timesTakenDown += int(takedownAmmount.text)
    return timesTakenDown


print(numberOfTimesTakendown("Arman Tsarukyan"))
driver.quit()
