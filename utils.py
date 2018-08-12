import pandas as pd
import numpy as np
import urllib.robotparser as rp
import requests
from itertools import chain
from bs4 import BeautifulSoup
import re
from textblob import TextBlob, Word
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords, wordnet

parser = rp.RobotFileParser()

def robot_checker(base_url, agent="*"):
	parser.set_url(base_url+"/robots.txt")
	parser.read()
	if parser.can_fetch(base_url, agent) == True:
		print("Allowed!")
	else:
		print("Disallowed!")

def request_url(url):
	response = requests.get(url)
	return response.content

class Scrape_All:

	def __init__(self, page, base_url):

		self.page = BeautifulSoup(page, "html.parser")
		self.base_url = base_url[:-1]

	# def __repr__(self):

	# 	repr = """Scrape_All class, which will scrape from a given page all:
	# 			  a. hyperlinks (<a>) and provide the absolute link if relative one is given in the page,
	# 			  b. headings and paragraphs and merge them inside one string with a new line between different 
	# 			  headings/paragraphs, without distorting order).
	# 			  c. custom tags provided by the user (i.e. if the user provides li.author or similar input then 
	# 			  all the list items that have class author must be scraped."""
	# 	return repr

	def get_links(self):

		a_tags = self.page.find_all("a")
		hrefs = [i.get("href") for i in a_tags]
		#links = [i if "http" in i else self.base_url + i for i in hrefs]
		return hrefs

	def get_head_par(self):

		return Super_List([i.get_text() for i in list(self.page.find_all(re.compile(r'(h[1-6]|p)')))]).merge() 

	def get_user_lists(self):

		user_lists = [i.get_text() for i in self.page.find_all("li", class_='author')]
		return user_lists

class Super_List:

	def __init__(self, ls):

		self.ls = ls

	# def __repr__(self):

	# 	repr = """Super_list class, which will take a list as input and provide the following functionalities:
	# 				a. untilst function, that will return the unlisted version of a nested list or the same one if list was not nested,
	# 				b. merge function, that will merge all the elements of any list into strings,
	# 				c. find function that will take a type argument as an input. If type =:
	# 					i. number, then it will return all the list elements that include a number,
	# 					ii. letter, then it will return all the list elements that include a letter."""
	# 	return repr

	def untilst(self):

		try:
			return list(chain.from_iterable(self.ls))
		except TypeError:
			return self.ls

	def merge(self):

		return "\n".join([str(i) for i in self.ls])

	def find(self, type):

		if type == 'number':
			return list([float(i) for i in self.ls if i.isdigit() == True])
		elif type == 'letter':
			return list([str(i) for i in self.ls if i.isalpha() == True])
		else:
			print("Invalid 'type' input.")		

class Cleaner:

	def __init__(self, string):

		self.string = TextBlob(string)

	# def __repr__(self):

	# 	repr = """Cleaner class, which will take a string as an input and provide the following methods:
	# 				a. tokenize into words/sentences,
	# 				b. lemmatize, clean stopwords,
	# 				c. make plural/singular,
	# 				d. uppercase/lowercase,
	# 				e. draw frequency distributions of words."""
	# 	return repr

	def tokenize(self):

		return (self.string.words, self.string.sentences)


	def lematize(self):

		return [word.lemmatize() for word in self.string.words]

	def plural(self):

		return [word.pluralize() for word in self.string.words]

	def singular(self):

		return [word.singularize() for word in self.string.words]

	def uppercase(self):

		sw = stopwords.words("english")
		return [i.upper() for i in self.string.words if i not in sw]
		 
	def lowercase(self):

		sw = stopwords.words("english")
		return [i.lower() for i in self.string.words if i not in sw]

	def freq_dist(self):
 
		nltk.FreqDist(self.lowercase()).plot(10, cumulative=False)
