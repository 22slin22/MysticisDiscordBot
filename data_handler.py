import json


discord_to_brawl_id_file = "data/brawl_ids.json"
player_stats_file_name = "data/players/{}_stats.json"
player_ranked_file_name = "data/players/{}_ranked.json"


def get_brawl_id_by_discord_id(discord_id):
    with open(discord_to_brawl_id_file) as brawl_ids:
        ids = json.load(brawl_ids)
        return ids[str(discord_id)]


def link_discord_to_brawl_id(discord_id, brawl_id):
    with open(discord_to_brawl_id_file, 'r+') as brawl_ids:
        ids = json.load(brawl_ids)
        ids[str(discord_id)] = brawl_id
        json.dump(brawl_ids, ids)


def get_player_stats_by_brawl_id(brawl_id):
    with open(player_stats_file_name.format(brawl_id)) as player_info:
        return json.load(player_info)


def get_player_stats_by_discord_id(discord_id):
    brawl_id = get_brawl_id_by_discord_id(discord_id)
    return get_player_stats_by_brawl_id(brawl_id)


def get_player_ranked_by_brawl_id(brawl_id):
    with open(player_ranked_file_name.format(brawl_id)) as player_info:
        return json.load(player_info)


def get_player_ranked_by_discord_id(discord_id):
    brawl_id = get_brawl_id_by_discord_id(discord_id)
    return get_player_ranked_by_brawl_id(brawl_id)
