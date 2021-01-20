#!/bin/env python3

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup

lb_url = "https://letterboxd.com"
lbSearchFilms_url = "https://letterboxd.com/search/films/"
lbMovie_url = "https://letterboxd.com/film/"
lbMovieRate_url = ["https://letterboxd.com/csi", "/rating-histogram/"]

def getMovieDetails( movieName ):
	
	r = requests.get( lb_url + movieName )
	if(r.status_code != 200):
		return -1

	soup = BeautifulSoup( str(r.content), 'html.parser' )
	section = soup.find('section', id="featured-film-header")

	movieDetails = {}
	movieDetails['name'] = section.find('h1').get_text()
	movieDetails['year'] = section.find('p').find('small', class_="number").find('a').get_text()
	movieDetails['director'] = section.find('p').find('small').find_next_siblings()[0].find('span').get_text()

	## Getting the rate
	rateUrl = lbMovieRate_url[0] + movieName + lbMovieRate_url[1]
	r = requests.get( rateUrl )
	if(r.status_code != 200):
		print(movieName)
		print(rateUrl)
		return -1
	soup = BeautifulSoup( str(r.content), 'html.parser')
	movieDetails['starsRate'] = soup.find('a', class_="tooltip display-rating").get_text()
	return movieDetails

def getMovieFromSearch( contentSearch, indexResult = 0 ):
	
	soup = BeautifulSoup( str(contentSearch), 'html.parser' )
	
	listOfResults = soup.find('ul', class_="results")
	results = listOfResults.find_all('li')
	
	getMovieDetails( results[indexResult].find('div')['data-target-link'] )

def searchMovie( search_str, indexResult = 0 ):
	
	full_lbSearch_url = lbSearchFilms_url + search_str.replace(' ', '+')
	
	r = requests.get( full_lbSearch_url )
	if(r.status_code != 200):
		return -1
	
	contentSearch = r.content

	movie_url = getMovieFromSearch( contentSearch, indexResult )
	return movie_url


if __name__ == '__main__':
	
	#movieSearch = input('Movie: ')
	
	filePage = open('output.html', 'r')
	content = filePage.read()	
	filePage.close()
	
	getMovieFromSearch( str(content) )

	
