import requests
import sys
sys.path.append('..')
from bs4 import BeautifulSoup

from utils.nlp import tokenize, filter_stop_words

def crawl_amazon_url(url):
	"""
		This function crawls an amazon review url, extracts product descriptions and extracts 
		important tokens from the product description.		
	"""
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	try:
		text = soup.find("div", {"id": "productDescription"}).find("p").text
		tokens = tokenize(text)
		return filter_stop_words(tokens)
	except Exception as error:
		print('Exception: {}' + repr(error))
		print "Unable to find product descriptions for URL: {}".format(url)
		return []
	

if __name__=="__main__":
	print crawl_amazon_url('http://www.amazon.com/gp/product/B00HUGXOAU')
