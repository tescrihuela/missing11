from selenium import webdriver
from bs4 import BeautifulSoup
import random
from pprint import pprint
import csv
import datetime
import os

#############
## Paramètres
file = 'missing11.csv'
url_missing = u"https://missing11.com/?game="
matching = {"id":276, "date":datetime.datetime.strptime("04/11/2022", '%d/%m/%Y')}

matchs = []

# # Chrome driver
#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument(f"--remote-debugging-port={random.randint(5000,9999)}")  # this
#browser = webdriver.Chrome(options=options, executable_path='./chromedriver')

# Chrome driver on heroku with buildpacks
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(f"--remote-debugging-port={random.randint(5000,9999)}") 
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

############
## Fonctions
def get_publication_date(id):
	jours_ecoules = matching["id"] - id
	publication_date = matching["date"] - datetime.timedelta(days=jours_ecoules)
	
	return publication_date.strftime("%d/%m/%Y")

def get_last_match_from_csv():
	with open(file, 'r', encoding='utf8', newline='') as csvfile:
		f = csvfile.readlines()
		last_date = f[-1].split(',')[-1].strip()
		last_id = int(f[-1].split(',')[0].split('=')[1].strip())
		last_date = datetime.datetime.strptime(last_date, '%d/%m/%Y')
		
		return last_date, last_id

def scrap_match(id):
	url = f"{url_missing}{id}"
	pprint(url)
	browser.get(url)
	soup = BeautifulSoup(browser.page_source,features="html.parser")
	intro = soup.find_all('div', {"class": "intro"})[0].find_all('div')[1:-2]

	match = intro[0].text
	team1 = match.split("'")[0].strip()
	team2 = match.split(" vs ")[-1].split(" to ")[-1].split(" with ")[-1].split(" against ")[-1].strip()
	score = match.split("'")[1].split(" ")[1].strip()
	competition = intro[1].text
	stade = intro[2].text
	date_match = intro[3].text
	jour, mois, annee = date_match.split('/')

	matchs.append([url, competition, annee, team1, team2, score, stade, date_match, get_publication_date(id)])

def write_csv(file, delete):
	if delete:
		with open(file, 'w', encoding='utf8', newline='') as csvfile:
			fieldnames = ['URL', 'Compétition', 'Année', 'Team à trouver', 'Team opposée', 'Score', 'Stade', 'Date du match', 'Date de publication']
			writer = csv.writer(csvfile)
			writer.writerow(fieldnames)
			writer.writerows(matchs)
	else:
		with open(file, 'a', encoding='utf8', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(matchs)


######
# Main

date_today = datetime.datetime.now()
date_derniere_publication, id_derniere_publication = get_last_match_from_csv()
difference_jours = (date_today - date_derniere_publication).days
if difference_jours != 0:
	for i in range(id_derniere_publication + 1, id_derniere_publication +1 + difference_jours):
		scrap_match(i)
	write_csv(file, False)
else:
	print("Déjà à jour")

# # Re-création depuis le début
# for i in range(1,matching["id"] + difference_jours + 1):
# 	scrap_match(i)
# write_csv(file, True)

browser.quit()
