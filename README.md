# pokemon_scraper
This is a web scraper that gathers data about pokemon from www.pokemondb.net.

## Usage
To gather data on an individual pokemon you can use the `--name` or `--num` arguments. These arguments take in the name or national dex number of a single pokemon and gather the name, type, national pokedex number, and EV yield of the pokemon.

To get data on many pokemon use the `--file` argument to retrieve data on all pokemon listed in the file. The file may contain the name or national pokedex number of the pokemon. Each line should contain exactly one pokemon name or number.

Note that only one input method can be used at a time.

The data can be output in any of three methods. The first is with the `--out_csv` argument. This argument writes the data to the file provided to the argument in csv format. The next option is the `--out_json` argument. This writes the data to json at the given location. Lastly, the `--print` prints the raw data on the command line. These options maybe used in any combination.

## Examples
```
$ python scraper.py --name=bulbasaur --print
```
{'name': 'bulbasaur', 'dex_num': '001', 'type_1': 'grass', 'type_2': 'poison', 'evs': {'hp': '0', 'attack': '0', 'defense': '0', 'specialattack': '1', 'specialdefense': '0', 'speed': '0'}}
```
$ python scraper.py --num=643 --print
```
{'name': 'reshiram', 'dex_num': '643', 'type_1': 'dragon', 'type_2': 'fire', 'evs': {'hp': '0', 'attack': '0', 'defense': '0', 'specialattack': '3', 'specialdefense': '0', 'speed': '0'}}
```
$ python scraper.py --file=pokemon_names.txt --out_csv=pokemon.csv
```
| Name      | Dex Number | Type 1   | Type 2 | HP | Attack | Defense | Special Attack | Special Defense | Speed |
|-----------|------------|----------|--------|----|--------|---------|----------------|-----------------|-------|
| bulbasaur | 001        | grass    | poison | 0  | 0      | 0       | 1              | 0               | 0     |
| charizard | 006        | fire     | flying | 0  | 0      | 0       | 3              | 0               | 0     |
| turtwig   | 387        | grass    | none   | 0  | 1      | 0       | 0              | 0               | 0     |
| gyarados  | 130        | water    | flying | 0  | 2      | 0       | 0              | 0               | 0     |
| bonsly    | 438        | rock     | none   | 0  | 0      | 1       | 0              | 0               | 0     |
| cufant    | 878        | steel    | none   | 0  | 1      | 0       | 0              | 0               | 0     |
| ampharos  | 181        | electric | none   | 0  | 0      | 0       | 3              | 0               | 0     |
```
$ python sracper.py --file=pokemon_names.txt --out_json=pokemon.json
```
{"data": [{"name": "bulbasaur", "dex_num": "001", "type_1": "grass", "type_2": "poison", "evs": {"hp": "0", "attack": "0", "defense": "0", "specialattack": "1", "specialdefense": "0", "speed": "0"}}, {"name": "charizard", "dex_num": "006", "type_1": "fire", "type_2": "flying", "evs": {"hp": "0", "attack": "0", "defense": "0", "specialattack": "3", "specialdefense": "0", "speed": "0"}}, {"name": "turtwig", "dex_num": "387", "type_1": "grass", "type_2": "none", "evs": {"hp": "0", "attack": "1", "defense": "0", "specialattack": "0", "specialdefense": "0", "speed": "0"}}, {"name": "gyarados", "dex_num": "130", "type_1": "water", "type_2": "flying", "evs": {"hp": "0", "attack": "2", "defense": "0", "specialattack": "0", "specialdefense": "0", "speed": "0"}}, {"name": "bonsly", "dex_num": "438", "type_1": "rock", "type_2": "none", "evs": {"hp": "0", "attack": "0", "defense": "1", "specialattack": "0", "specialdefense": "0", "speed": "0"}}, {"name": "cufant", "dex_num": "878", "type_1": "steel", "type_2": "none", "evs": {"hp": "0", "attack": "1", "defense": "0", "specialattack": "0", "specialdefense": "0", "speed": "0"}}, {"name": "ampharos", "dex_num": "181", "type_1": "electric", "type_2": "none", "evs": {"hp": "0", "attack": "0", "defense": "0", "specialattack": "3", "specialdefense": "0", "speed": "0"}}]}