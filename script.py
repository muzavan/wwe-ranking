import csv
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
import math
from shutil import copyfile
import sys
from typing import List, Mapping, Tuple

@dataclass
class Wrestler:
    name: str
    rating: float
    brand: str # RAW or Smackdown
    win: int
    loss: int
    total: int

class Result(IntEnum):
    LOSE = 0
    DRAW = 1
    WIN = 2

    def score(self) -> float:
        return float(self) / float(Result.WIN)

K_FACTOR = 30

def to_2_decimal(fl: float):
    return float(f"{fl:.2f}")

def expectation(r1, r2):
    return 1.0 / (1.0 + math.pow(10, (r2 - r1)/400))

def update_wrestler(w: Wrestler, own_rating: float, opponent_rating: float, result: Result):
    e = expectation(own_rating, opponent_rating)
    w.rating = to_2_decimal((w.rating + K_FACTOR * (result.score() - e)))

    if result == Result.WIN:
        w.win += 1
    if result == Result.LOSE:
        w.loss += 1

LATEST_RATING_CSV = "latest_rating.csv"
def get_latest_rating() -> Mapping[str, Wrestler]:
    wrestlers = dict()
    with open(LATEST_RATING_CSV, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            w = Wrestler(r["name"], float(r["rating"]), r["brand"], 
                            int(r["win"]), int(r["loss"]), int(r["total"]))

            if w.name in wrestlers:
                print("Duplicate wrestler:", w.name)
                exit()
            wrestlers[w.name] = w

    return wrestlers

def extract_winner(winners: List[str], wrestler_map: Mapping[str, Wrestler]) -> Tuple[List[Wrestler], float]:
    winner_wrestlers = []
    for w in winners:
        if w not in wrestler_map:
            print("Not in the roster:", w)
            exit()

        winner_wrestlers.append(wrestler_map[w])

    winner_rating = sum([w.rating for w in winner_wrestlers]) / float(len(winner_wrestlers))

    return winner_wrestlers, winner_rating

def extract_losers(losers: List[str], wrestler_map: Mapping[str, Wrestler], skipped: bool) -> Tuple[List[List[Wrestler]], List[float]]:
    loser_wrestlers = []
    loser_ratings = []

    for l in losers:
        ls = l.split("&")
        loser_team = []
        for ll in ls:
            ll = ll.strip()

            if ll not in wrestler_map:
                # assumed to be jobber, skipped
                if skipped:
                    continue
                print("Not in the roster:", ll)
                exit()

            loser_team.append(wrestler_map[ll])

        loser_wrestlers.append(loser_team)
        if len(loser_team) > 0:
            loser_ratings.append(sum([w.rating for w in loser_team]) / float(len(loser_team)))
        else:
            loser_ratings.append(0)

    return loser_wrestlers, loser_ratings

    

def update_from_episode(episode_file: str, wrestler_map: Mapping[str, Wrestler]):
    with open(episode_file, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Note:
            # Assumption: winner to losers is one to many
            # winner/loser is an entity, can be actual user or a team

            winners = r["winners"].strip()
            losers = r["losers"].strip().split("|")

            winners = list(map(lambda x: x.strip(), winners.split("&")))
            winner_entity, winner_rating = extract_winner(winners, wrestler_map)
            
            skipped = int(r["skipped"]) == 1
            loser_entities, loser_ratings = extract_losers(losers, wrestler_map, skipped)

            # Update total match
            for w in winner_entity:
                w.total += 1
            
            for l_entity in loser_entities:
                for l in l_entity:
                    l.total += 1

            if skipped:
                continue

            total_rating = winner_rating + sum(loser_ratings)
            opponent_num = float(len(loser_ratings))
            # Update winner
            for w in winner_entity:
                update_wrestler(w, winner_rating, (total_rating - winner_rating) / opponent_num, Result.WIN)

            # Update losers
            for lrating, l_entity in zip(loser_ratings, loser_entities):
                for ll in l_entity:
                    update_wrestler(ll, lrating, (total_rating - lrating) / opponent_num, Result.LOSE)

def dump_latest_rating(latest_rating: Mapping[str, Wrestler]):
    wrestlers = []
    for _, w in latest_rating.items():
        wrestlers.append(w)

    wrestlers = sorted(wrestlers, key= lambda w: (w.brand, -w.rating, -w.total, -w.win, w.loss, w.name))

    with open(LATEST_RATING_CSV+".new", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "rating", "brand", "win", "loss", "total"])
        rows = [(w.name, w.rating, w.brand, w.win, w.loss, w.total) for w in wrestlers]
        writer.writerows(rows)

    # archive_file = "archive/%s.%s" % (LATEST_RATING_CSV, datetime.today().strftime("%Y%m%d"))
    # copyfile(LATEST_RATING_CSV, archive_file)
    


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


