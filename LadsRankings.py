import requests
import re
import requests_html
from bs4 import BeautifulSoup

# open roster file and read it into file_text
roster_file = open("rosters.csv", 'r')
file_text = roster_file.read()

# grabbing the table rows from the season dotabuff
url = "https://www.dotabuff.com/esports/leagues/13450-league-of-lads-season-8/players"
session = requests_html.HTMLSession()
response = session.get(url)
dota_soup = BeautifulSoup(response.content, 'html.parser')
player_table_rows = dota_soup.find_all('tr')
player_table_rows = player_table_rows[2:]
outputfile = open("Player stats.csv", 'w')
outputfile.write("Player Name, Player Team, Record, KDA, Kills, Deaths, Assists, Last Hits, Denies, GPM, XPM\n")
# set up a dictionary for the position pattern matching
# this is to find players in the csv and will work for all positions
# ex: 1,PlayerName
position_patterns = {i: str(i) + ',[A-Za-z 0-9]*' for i in range(1, 6)}


def get_all_players_who_play_position(pos):
    players = [s[2:] for s in re.findall(position_patterns[pos], file_text)]
    return players


def get_stats_for_player(player):
    for player_row in player_table_rows:
        try:
            player_data = player_row.find_all('td')
            if player in player_data[1].get_text():
                # print(player_data[1].get_text())
                # print(f'player {player} found')
                return {
                    "Player Name": player,
                    "Player Team": player_data[1].get_text().replace(player, ''),
                    "Record": player_data[2].get_text(),
                    "KDA": player_data[3].get_text(),
                    "Kills": player_data[4].get_text(),
                    "Deaths": player_data[5].get_text(),
                    "Assists": player_data[6].get_text(),
                    "Last Hits": player_data[7].get_text(),
                    "Denies": player_data[8].get_text(),
                    "GPM": player_data[9].get_text(),
                    "XPM": player_data[10].get_text()
                }
        except IndexError:
            pass


'''
offlane_players = get_all_players_who_play_position(3)
for offlaner in offlane_players:
    stats = get_stats_for_player(offlaner)
    if stats:
        print(stats)
        print()
    else:
        print(f'No stats found for {offlaner}')
        print()
'''


def save_all_players_with_role_stats(pos):
    players = get_all_players_who_play_position(pos)
    for player in players:
        player_stats = get_stats_for_player(player)
        if player_stats:
            save_player_stats(player_stats)
        else:
            while True:
                try:
                    print(f'No stats found for {player}')
                    other_name = input("Enter corrected name: ")
                    player_stats = get_stats_for_player(other_name)
                    player_stats['Player Name'] = player
                    save_player_stats(player_stats)
                    break
                except:
                    print("Mistyped player correction try again.")
        print(f'Saved {player}\n')


def save_player_stats(stats):
    for value in stats.values():
        outputfile.write(str(value) + ',')
    outputfile.write('\n')

save_all_players_with_role_stats(3)
outputfile.close()

'''
for midlaner in get_all_players_who_play_position(2):
    stats = get_stats_for_player(midlaner)
    if stats:
        print(stats)
        print()
    else:
        print(f'No stats found for {midlaner}')
        print()
'''
# for player in get_all_players_who_play_position(3):
#   print(player)

# print(soup.prettify())
# print(soup.find_all('tr')[1])
# print(soup.find_all('tr')[2].find_all('td')[10].get_text())
