from time import sleep

from glassdoor import scrape_site

EMP_NAME = "Bank-of-America"
EMP_ID = 8874
FILENAME = "D:/python_files/Glassdoor/glassdoor_bofa.txt"
BASE_URL = "http://www.glassdoor.com/"

start = 400
end = 500

for i in xrange(start, end):
	scrape_site(EMP_NAME, EMP_ID, FILENAME, BASE_URL, i,i+1)
	sleep(15)