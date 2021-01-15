#!/bin/env python3

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup

lb_url = "https://letterboxd.com"
lbSearchFilms_url = "https://letterboxd.com/search/films/"
lbMovie_url = "https://letterboxd.com/film/"

def getMovieFromSearch( contentSearch, indexResult = 0 ):
	
	soup = BeautifulSoup( str(contentSearch), 'html.parser' )
	
	listOfResults = soup.find('ul', class_="results")
	results = listOfResults.find_all('li')
	
	lbMovieResult_url = lb_url + results[indexResult].find('div')['data-target-link']
	return lbMovieResult_url

def searchMovie( search_str, indexResult = 0 ):
	
	full_lbSearch_url = lbSearchFilms_url + search_str.replace(' ', '+')
	
	r = requests.get( full_lbSearch_url )
	if(r.status_code != 200):
		return -1
	
	contentSearch = r.content

	movie_url = getMovieFromSearch( contentSearch, indexResult )
	return movie_url


if __name__ == '__main__':
	
	movieSearch = input('Movie: ')

	movie_url = searchMovie( movieSearch )
	print( movie_url )
