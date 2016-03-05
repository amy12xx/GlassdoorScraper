#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import urllib2
import urllib
import os
import codecs
from datetime import datetime
import time

from bs4 import BeautifulSoup
import mechanize

EMP_NAME = "American-Express"
EMP_ID = 35
FILENAME = "D:/python_files/Glassdoor/glassdoor_amex.txt"
BASE_URL = "http://www.glassdoor.com/"

def scrape_site(company_name, company_id, filename, base_url, start, end):
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Chrome/45.0.2454.99')]
	br.set_handle_robots(False)

	with codecs.open(filename, 'a', encoding='utf-8') as review_file:
		for i in xrange(start,end):
			url = base_url + "Reviews/%s-Reviews-E%d_P%d.htm" % (company_name, company_id,i)
			print
			print url

			soup = BeautifulSoup(br.open(url).read())

			reviews = soup.find_all('div', 'hreview')

			for rev in reviews:
				try:
					summary = rev.find_all('span', 'summary')
					summary = (summary[0].contents[0]).strip() if summary else ""
					print summary

					rating = rev.find_all('span', 'value-title')
					rating = str(rating[0]['title']).strip() if rating else ""

					pros = rev.find_all('p', 'pros noMargVert notranslate truncateThis')
					pros = (pros[0].contents[0]).strip() if pros else ""

					cons = rev.find_all('p', 'cons noMargVert notranslate truncateThis')
					cons = (cons[0].contents[0]).strip() if cons else ""

					advice_mgmt = rev.find_all('p', 'adviceMgmt noMargVert notranslate truncateThis')
					advice_mgmt = (advice_mgmt[0].contents[0]).strip() if advice_mgmt else ""

					# Author details
					author_job_title = rev.find_all('span', 'authorJobTitle')
					author_job_title = (author_job_title[0].contents[0]).strip() if author_job_title else ""

					author_location = rev.find_all('span', 'authorLocation')
					author_location = (author_location[0].contents[0]).strip() if author_location else ""		

					# recommends = rev.find_all('div', 'flex-grid recommends')
					# recommends = str(recommends[0].contents[0]) if recommends else ""

					review_date = rev.find_all('span', 'dtreviewed notranslate')
					review_date = str(review_date[0].contents[0]).strip() if review_date else ""

					# category ratings
					category_ratings = rev.find_all('li')
					
					ratings = {'Work/Life Balance': 0.0, 'Culture & Values': 0.0, 'Career Opportunities': 0.0, 'Comp & Benefits': 0.0, 'Senior Management': 0.0}
					for item in category_ratings:
						i = item.find('div').next_element
						j = item.find('span')["title"]
						ratings[i] = j				
					
					row = [summary, rating, pros, cons, advice_mgmt, author_job_title, author_location, review_date, str(ratings['Work/Life Balance']), \
							str(ratings['Culture & Values']), str(ratings['Career Opportunities']), str(ratings['Comp & Benefits']), str(ratings['Senior Management'])]
					review_file.write('^'.join(row) + '\n')
				except:
					continue

			del reviews, soup

def main():
	scrape_site(EMP_NAME, EMP_ID, FILENAME, BASE_URL,2,3)

if __name__ == '__main__':
	main()