import requests
from bs4 import BeautifulSoup

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name of a single pokemon to retrieve information on.')
parser.add_argument('--num',  help='The national dex number of a single pokemont to retrieve information on.')
parser.add_argument('--file', help='Path to a file containing the names/numbers of pokemon to scrape info on. One pokemon per line.')

def scrape_single_pokemon_name(name: str) -> dict:
	data = dict()
	evs = create_ev_dict()
	
	url = 'https://pokemondb.net/pokedex/{}'.format(name)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	data['name'] = name.lower()

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
				data['type_2'] = 'none'
	
	for row in tables[1].find_all('tr'):
		ev_data = row.find('td').text.lower().strip().replace(' ','').split(',')
		break
	
	for ev in ev_data:
		value = ev[0]
		key = ev[1:]
		evs[key] = value
	data['evs'] = evs
	return data


def scrape_single_pokemon_num(num: str) -> dict:
	url = 'https://pokemondb.net/pokedex/{}'.format(num)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	name = soup.find('h1').text.strip()
	return scrape_single_pokemon_name(name)


def scrape_pokemon_file(file: str) -> list:
	pokemon_data = list()
	with open(file, 'r') as f:
		pokemon = f.readlines()
	for line in pokemon:
		if line[0].isdigit():
			pokemon_data.append(scrape_single_pokemon_num(line.strip()))
		else:
			pokemon_data.append(scrape_single_pokemon_name(line.strip()))
	print(pokemon_data)
	return pokemon_data



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
	if args.name != None:
		scrape_single_pokemon_name(name=args.name)
	if args.num != None:
		scrape_single_pokemon_num(num=args.num)
	if args.file != None:
		scrape_pokemon_file(args.file)

