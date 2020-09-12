import requests
import configparser
import threading
import time
from data_handler import get_all_brawl_ids, set_player_stats, set_player_ranked

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config["Brawlhalla"]["api_key"]


class BrawlhallaDataUpdater(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.ids_to_update = []

    def run(self):
        while True:
            to_update = 90
            if len(self.ids_to_update) < 90:
                new_ids = get_all_brawl_ids()
                self.ids_to_update.extend(new_ids)
                to_update = min(len(new_ids), 90)
            for brawl_id in self.ids_to_update[:to_update]:
                update_player_data(brawl_id)
                time.sleep(0.1)
            self.ids_to_update = self.ids_to_update[90:]

            time.sleep(15*60)


def get_player_stats(brawl_id):
    response = requests.get(
        "https://api.brawlhalla.com/player/{player}/stats?api_key={api_key}".format(player=brawl_id,
                                                                                    api_key=api_key))
    return response.json()


def get_player_ranked(brawl_id):
    response = requests.get(
        "https://api.brawlhalla.com/player/{player}/ranked?api_key={api_key}".format(player=brawl_id,
                                                                                     api_key=api_key))
    return response.json()


def update_player_data(brawl_id):
    set_player_stats(brawl_id, get_player_stats(brawl_id))
    set_player_ranked(brawl_id, get_player_ranked(brawl_id))


if __name__ == '__main__':
    brawlhalla_data_updater = BrawlhallaDataUpdater()
    brawlhalla_data_updater.start()
