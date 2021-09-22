data_file = open("Player stats.csv")
dictionary_keys = [s.strip() for s in data_file.readline().strip().split(',')]
all_players = dict()
for player_data_line in data_file:
    # player_stats = {dictionary_keys[i]: player_data_line.rstrip().split(',')[i] for i in range(len(dictionary_keys))} fun little one line dictionary
    player_stats = [s.strip() for s in player_data_line.strip().split(',')]
    player_dict = dict()
    for i in range(len(dictionary_keys)):
        key = dictionary_keys[i]
        value = player_stats[i]
        if value.isdigit():
            value = int(value)
            # print("int conversion")
        else:
            try:
                value = float(value)
                # print("float conversion")
            except ValueError:
                # print("Non float and non int value left as string")
                pass
        player_dict[key] = value
    all_players[player_dict["Player Name"]] = player_dict

print("You can sort by")
print(dictionary_keys)


def sort_by(sorting_value):
    try:
        print(f'\n---Players sorted by {sorting_value}---')
        sorted_dict = sorted(all_players.items(), key=lambda x: x[1][sorting_value])
        for player, stats in sorted_dict:
            print("%20s %10s" % (player, str(stats[sorting_value])))
    except KeyError:
        print("You can not sort by that key")

# sort_by('Kills')
