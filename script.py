import csv
from dataclasses import dataclass
import math
import sys
from typing import Mapping

@dataclass
class Wrestler:
    name: str
    rating: float
    brand: str # RAW or Smackdown
    win: int
    loss: int
    total: int

# Use the same as chess?
K_FACTOR = 24

def expectation(r1, r2):
    return (1.0 / (1.0 + math.pow(10, r2 - r1)/400))

def update(winner: Wrestler, loser: Wrestler):
    e_win = expectation(winner.rating, loser.rating)
    e_loss = expectation(loser.rating, winner.rating)

    winner.rating = (winner.rating + K_FACTOR * (1 - e_win))
    loser.rating = (loser.rating + K_FACTOR * (0 - e_loss))

LATEST_RATING_CSV = "latest_rating.csv"
def get_latest_rating() -> Mapping[str, Wrestler]:
    wrestlers = dict()
    with open(LATEST_RATING_CSV, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            w = Wrestler(r["name"], r["rating"], r["brand"], 
                            r["win"], r["loss"], r["total"])

            if w.name in wrestlers:
                print("Duplicate wrestler:", w.name)
                exit()
            wrestlers[w.name] = w

    return wrestlers

def update_from_episode(episode_file: str, latest_rating: Mapping[str, Wrestler]):
    with open(episode_file, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            winners = r["winners"].strip().split("&")
            losers = r["losers"].strip().split("&")
            is_tag_team = r["is_tag_team"] == 1
            skipped = r["skipped"] == 1 # will increment total match, does not affect score

            for w_name in winners:
                for l_name in losers:
                    w_name = w_name.strip()
                    l_name = l_name.strip()

                    if w_name not in latest_rating:
                        print("Unregonized wrestler:", w_name)
                        exit()
                    if l_name not in latest_rating:
                        print("Unrecognized wrestler:", l_name)
                        exit()

                    winner = latest_rating[w_name]
                    loser = latest_rating[l_name]

                    if not skipped:
                        update(winner, loser)
                        winner.win += 1
                        loser.loss += 1

                    winner.total += 1
                    loser.total += 1

    


def dump_latest_rating(latest_rating: Mapping[str, Wrestler]):
    wrestlers = []
    for _, w in latest_rating.items():
        wrestlers.append(w)

    wrestlers = sorted(wrestlers, key= lambda w: (w.brand, -w.rating, w.name))

    with open(LATEST_RATING_CSV, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "rating", "brand", "win", "loss", "total"])
        rows = [(w.name, w.rating, w.brand, w.win, w.loss, w.total) for w in wrestlers]
        writer.writerows(rows)


# Usage: python script.py episode.csv
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass the episode file")
        exit()

    episode_files = sys.argv[1:]
    latest_rating = get_latest_rating()

    for episode in episode_files:
        print("Process episode:", episode)
        update_from_episode(episode, latest_rating)

    dump_latest_rating(latest_rating)
    print("Done!")


