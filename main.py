import lolesports
import getTournies

def main():
	url = "http://www.lolesports.com/en_US/na-lcs/na_2017_summer/schedule/regular_season/"

	for week in range(1,10):
		eventsHref = lolesports.GetURLsFromScheduleURL(url+str(week))
		for matches in range(len(eventsHref)):
			gamesHref = lolesports.GetURLsFromBracketURL(eventsHref[matches])
			for games in range(len(gamesHref)):
				gameList = lolesports.APIDataFromURL(gamesHref[games])
				region, gameId, gameHash = gameList
				getTournies.gameID_to_match(region,gameId,gameHash)
		


main()