import urllib.request,urllib.parse,urllib.error
import requests
import os
import pprint
import hidden
import pandas as pd
from requests_html import HTML

base_dir = os.path.dirname(__file__)

def get_title_id(name):
	url = 'http://www.omdbapi.com/?'
	param = dict()
	param['apikey']=hidden.apikey()
	param['t']=name

	url = url + urllib.parse.urlencode(param)
	data = requests.get(url).json()
	#pprint.pprint(data)
	imdb_id = data['imdbID']
	#print(imdb_id)
	return imdb_id

def get_html_data(url):
	data = requests.get(url)
	if data.status_code != 200:
		print("Could not access url")
		quit()

	html_text = data.text
	html_data = HTML(html=html_text)

	return html_data

table_data = []
headers = ['Title','Rating','Plot']

def parse_data(html_data,count):

	if count==0:
		return

	try:
		title = html_data.find('.title_wrapper')[0].text.split('&')[0]
	except:
		title = html_data.find('.title_wrapper')[0].text

	rating = html_data.find('.ratingValue')[0].text
	plot = html_data.find('.plot_summary .summary_text')[0].text
	row_data = [title,rating,plot]
	table_data.append(row_data)
	print("==================")
	print(title)
	print(rating)
	print(plot)

	new_links = html_data.find('.rec_item a')
	to_go_links = []
	for link in new_links:
		new_url = "https://www.imdb.com/" + list(link.links)[0]
		to_go_links.append(new_url)

	for link in to_go_links:
		if count-1 == 0:
			continue
		parse_data(get_html_data(link),count-1)


name = "His dark materials"
url = 'https://www.imdb.com/title/' + get_title_id(name) + '/'
html_data = get_html_data(url)
parse_data(html_data,2)

df = pd.DataFrame(table_data,columns=headers)
df.to_csv('recommendations.csv',index=False)