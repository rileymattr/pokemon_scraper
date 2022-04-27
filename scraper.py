import requests
from bs4 import BeautifulSoup

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name of a single pokemon to retrieve information on.')

def scrape_single_pokemon(name: str) -> dict:
	data = dict()
	url = 'https://pokemondb.net/pokedex/{}'.format(name)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	data['name'] = name

	tables = soup.find_all(class_="vitals-table")
	rows = list()
	for row in tables[0].find_all('tr'):
		row_head = row.find('th').text.lower()
		if 'national' in row_head:
			data['dex_num'] = row.find('td').text
		if 'type' in row_head:
			types = list()
			for type in row.find_all('a'):
				types.append(type.text.strip().lower())
			data['type_1'] = types[0]
			if len(types) > 1:
				data['type_2'] = types[1]
			else:
				data['type_2'] = 'None'
	
	for row in tables[1].find_all('tr'):
		ev_data = row.find('td').text.lower().strip().replace(' ','').split(',')
		break
	evs = create_ev_dict()
	for ev in ev_data:
		value = ev[0]
		key = ev[1:]
		evs[key] = value
	data['evs'] = evs
	print(data)


def create_ev_dict() -> dict:
	ev = dict()
	ev['hp'] = 0
	ev['attack'] = 0
	ev['defense'] = 0
	ev['specialattack'] = 0
	ev['specialdefense'] = 0
	ev['speed'] = 0
	return ev


if __name__ == '__main__':
	args = parser.parse_args()
	scrape_single_pokemon(name=args.name)

