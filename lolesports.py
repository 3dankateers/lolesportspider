'''
Use this to get urls from lolesports.com and turn them into:
region
gameId
gameHash

which are then plugged into a seperate api to grab the json and store the results of the match in a DB
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, date

driver = webdriver.Firefox()

import time

GLOBAL_SLEEP_TIME = 10

#def main():
	#print GetEventNames(http://www.lolesports.com/en_US/)
	#print GetURLsFromScheduleURL(http://www.lolesports.com/en_US/lck/lck_2017_summer/schedule/promotion_relegation/Spring%20Promotion)
	#print GetURLsFromBracketURL(http://www.lolesports.com/en_US/lck/lck_2017_summer/matches/lck_2018_spring_promotion/match-a)
	#print APIDataFromURL(http://matchhistory.na.leagueoflegends.com/en/#match-details/WMC2TMNT1/290059?gameHash=8a91e4d6956af1cb&tab=overview)

'''
Give it the url from match history such as:
http://matchhistory.na.leagueoflegends.com/en/#match-details/WMC2TMNT1/290059?gameHash=8a91e4d6956af1cb&tab=overview
it will return the 3 pieces needed for the API call: region, gameId and gamehash in a list

'''
def APIDataFromURL(url):
	info = url.split("match-details/")[1]
	data = info.split("&tab=overview")[0]

	firstTwoData = data.split('/')

	region = firstTwoData[0]

	lastTwoData = firstTwoData[1].split("?gameHash=")

	gameID = lastTwoData[0]
	gameHash = lastTwoData[1]

	print "Region: " + region
	print "GameID: " + gameID
	print "GameHash: " + gameHash

	zipped = []
	zipped.append(region)
	zipped.append(gameID)
	zipped.append(gameHash)

	return zipped

'''
Gets the URLs of all the matchhistories from the bracket. IE:
http://www.lolesports.com/en_US/lck/lck_2017_summer/matches/lck_2018_spring_promotion/match-a
It will return the urls of all the games which were played (if best of 5 and teams only played 3 games, there will be a return of 3 urls)
'''
def GetURLsFromBracketURL(url):
	driver.get(url)
	time.sleep(GLOBAL_SLEEP_TIME)
	gameStatsHref = []

	gameStatsClassList = driver.find_elements_by_class_name("stats-link")

	for i in range(len(gameStatsClassList)):
		gameStatsHref.append(gameStatsClassList[i].get_attribute('href'))

	return gameStatsHref

'''
Gets the urls of each of the bo3 matches, ie:
http://www.lolesports.com/en_US/lck/lck_2017_summer/schedule/promotion_relegation/Spring%20Promotion
This would return every url if you were to click on the matches in a list

NOTE: each of these schedules can be selected on the top left, theres a button that says either Promotion,Regular Season, Playoffs or Regionals
		If you want to browse them youre going to have to add the url that calls this function to it. It seems to be a constant
		but theres no hrefs so its kinda hard to do it in a function like this
		Just need to add:::::
		Regular Season: regular_season/9
		Playoffs: playoffs/Finals
		Regionals: regionals/Regional Qualifier
		Promotionals: promotion_relegation/Spring Promotion

		Sometimes they're actually different but meh

'''
def GetURLsFromScheduleURL(url):
	driver.get(url)
	time.sleep(GLOBAL_SLEEP_TIME)

	bracketHref = []
	scheduleDiv = driver.find_element_by_id("main-container")
	emberViewClassList = scheduleDiv.find_elements_by_class_name("ember-view")

	for i in range(len(emberViewClassList)):
		href = emberViewClassList[i].get_attribute('href')

		try:
			if "/matches/" in href:
				bracketHref.append(emberViewClassList[i].get_attribute('href'))
		except:
			print "hhe"

	return bracketHref

'''
returns the urls of all the schedule listings from the main page
http://www.lolesports.com/en_US/
would return all the urls you get by clicking on "More Competitions"
'''
def GetEventNames(url):
	driver.get(url)
	time.sleep(GLOBAL_SLEEP_TIME)

	eventsHref = []

	dropDownNavs = driver.find_elements_by_class_name("dropdown-nav")

	for i in range(len(dropDownNavs)):
		style = dropDownNavs[i].get_attribute('style')

		if "min-width:" in style:
			emberViews = dropDownNavs[i].find_elements_by_class_name("ember-view")

			for k in range(len(emberViews)):
				eventsHref.append(emberViews[k].get_attribute('href'))

	return eventsHref