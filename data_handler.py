import json


discord_to_brawl_id_file = "data/brawl_ids.json"
player_stats_file_name = "data/players/{}_stats.json"
player_ranked_file_name = "data/players/{}_ranked.json"


def get_brawl_id_by_discord_id(discord_id):
    with open(discord_to_brawl_id_file) as brawl_ids:
        ids = json.load(brawl_ids)
        return ids.get(str(discord_id), None)


def link_discord_to_brawl_id(discord_id, brawl_id):
    try:
        with open(discord_to_brawl_id_file, 'r') as brawl_ids:
            ids = json.load(brawl_ids)
    except json.decoder.JSONDecodeError:
        ids = {}

    ids[str(discord_id)] = brawl_id
    with open(discord_to_brawl_id_file, 'w') as brawl_ids:
        json.dump(ids, brawl_ids)


def get_player_stats_by_brawl_id(brawl_id):
    with open(player_stats_file_name.format(brawl_id)) as player_stats:
        return json.load(player_stats)


def get_player_stats_by_discord_id(discord_id):
    brawl_id = get_brawl_id_by_discord_id(discord_id)
    return get_player_stats_by_brawl_id(brawl_id)


def set_player_stats(brawl_id, stats):
    with open(player_stats_file_name.format(brawl_id), 'w') as player_stats:
        return json.dump(stats, player_stats)


def get_player_ranked_by_brawl_id(brawl_id):
    with open(player_ranked_file_name.format(brawl_id)) as player_ranked:
        return json.load(player_ranked)


def get_player_ranked_by_discord_id(discord_id):
    brawl_id = get_brawl_id_by_discord_id(discord_id)
    return get_player_ranked_by_brawl_id(brawl_id)


def set_player_ranked(brawl_id, ranked):
    with open(player_ranked_file_name.format(brawl_id), 'w') as player_ranked:
        return json.dump(ranked, player_ranked)


def get_all_brawl_ids():
    with open(discord_to_brawl_id_file) as brawl_ids:
        ids = json.load(brawl_ids)
        return ids.values()
