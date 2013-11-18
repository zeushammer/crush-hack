import requests
import hashlib
import json
import random
import time
import sys


class CCrush(object):
    def __init__(self, session):
        self.session = session

    def hand_out_winnings(self, item_type, amount):
        item = [{"type": item_type, "amount": amount}]
        params = {
            "_session": self.session,
            "arg0": json.dumps(item),
            "arg1": 1,
            "arg2": 1,
            "arg3": "hash",
        }
        return requests.get("http://candycrush.king.com/api/handOutItemWinnings", params=params)

    def add_life(self):
        params = {"_session": self.session}
        return requests.get("http://candycrush.king.com/api/addLife", params=params)

    def start_game(self, episode, level):
        params = {"_session": self.session, "arg0": episode, "arg1": level}
        response = requests.get("http://candycrush.king.com/api/gameStart", params=params)
        return response.json()["seed"]

    def end_game(self, episode, level, seed, score=None):
        if score is None:
            score = random.randrange(3000, 6000) * 1000
        dic = {
            "timeLeftPercent": -1,
            "episodeId": episode,
            "levelId": level,
            "score": score,
            "variant": 0,
            "seed": seed,
            "reason": 0,
        }
        dic["cs"] = hashlib.md5("%(episodeId)s:%(levelId)s:%(score)s:%(timeLeftPercent)s:1129022562:%(seed)s:BuFu6gBFv79BH9hk" % dic).hexdigest()[:6]

        params = {"_session": self.session, "arg0": json.dumps(dic)}
        response = requests.get("http://candycrush.king.com/api/gameEnd", params=params)
        return response

    def play_game(self, episode, level, score=None):
        seed = self.start_game(episode, level)
        return self.end_game(episode, level, seed, score)


if __name__ == "__main__":
    ccrush = CCrush(sys.argv[1])
    episode = int(sys.argv[2])
    level = int(sys.argv[3])
    seed = ccrush.start_game(episode, level)
    ccrush.end_game(episode, level, seed)
