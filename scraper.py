import requests
from bs4 import BeautifulSoup
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name of a single pokemon to retrieve information on.')
parser.add_argument('--num',  help='The national dex number of a single pokemont to retrieve information on.')
parser.add_argument('--file', help='Path to a file containing the names/numbers of pokemon to scrape info on. One pokemon per line.')
parser.add_argument('--out_csv', help='Path to output data in csv format.')
parser.add_argument('--out_json', help='Path to output data in json format.')
parser.add_argument('--print', action='store_true', help='Use this flag to print the output to the command line.')


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
		value = str(ev[0])
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
	return pokemon_data



def create_ev_dict() -> dict:
	ev = dict()
	ev['hp'] = '0'
	ev['attack'] = '0'
	ev['defense'] = '0'
	ev['specialattack'] = '0'
	ev['specialdefense'] = '0'
	ev['speed'] = '0'
	return ev


def out_csv(data: list, file: str):
	with open(file, 'w') as f:
		f.write("Name, Dex Number, Type 1, Type 2, HP, Attack, Defense, Special Attack, Special Defense, Speed\n")
		for line in data:
			data_str = line['name'] +\
				", " + line['dex_num'] +\
				", " + line['type_1'] +\
				", " + line['type_2'] +\
				", " + line['evs']['hp'] +\
				", " + line['evs']['attack'] +\
				", " + line['evs']['defense'] +\
				", " + line['evs']['specialattack'] +\
				", " + line['evs']['specialdefense'] +\
				", " + line['evs']['speed'] + '\n'
			f.write(data_str)


def out_json(data: list, file: str):
	with open(file, 'w') as f:
		json.dump({'data': data}, f)


if __name__ == '__main__':
	args = parser.parse_args()
	if args.name != None:
		data = [scrape_single_pokemon_name(name=args.name)]
	if args.num != None:
		data = [scrape_single_pokemon_num(num=args.num)]
	if args.file != None:
		data = scrape_pokemon_file(args.file)
	if args.out_csv != None:
		out_csv(data=data, file=args.out_csv)
	if args.out_json != None:
		out_json(data=data, file=args.out_json)
	if args.print:
		for line in data:
			print(line)
