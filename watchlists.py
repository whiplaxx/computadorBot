import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup

WATCHLIST_URL = "https://letterboxd.com/{}/watchlist/page/{}"

def getMoviesFromWLPage( wl_html ):
	
	soup = BeautifulSoup( wl_html, 'html.parser' )
	
	watchlist_links = []

	movies = soup.find_all('div', class_="poster film-poster really-lazy-load")
	if( len( movies ) == 0):
		return []

	for movie in movies:
		watchlist_links.append( movie['data-target-link'] )

	return watchlist_links

def getUserWLLinks( username ):

	if( username == ""):
		return []

	watchlist_links = []
	
	page = 1
	while True:
		wl_html = getHTMLFromURL( WATCHLIST_URL.format(username, page) )
		
		page_links = getMoviesFromWLPage(wl_html)
		if( len(page_links) == 0 ):
			break
		watchlist_links.extend(page_links)
		page += 1
	
	return watchlist_links

def getHTMLFromURL( url ):
	
	r = requests.get( url )
	if(r.status_code != 200):
		return ""
	return r.content

def getCommonWLMovies( users ):

	usersWL = []

	for user in users:
		userWL = getUserWLLinks( user )
		if( len(userWL) > 0 ):
			usersWL.append(userWL)
	
	intersectionsLinks = usersWL[0]
	for i in range(1,len(usersWL)):
		intersectionsLinks = list( set(intersectionsLinks) & set(usersWL[i]) )

	return intersectionsLinks


if __name__ == '__main__':
	
	#with open('wl.html', 'r') as temp_file:
	#	wl_html = temp_file.read()

	usersWL = getCommonWLMovies( ['alexbatista', 'josecanas'] )

	print(usersWL)







