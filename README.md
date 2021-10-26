# WWE Ranking

## Description
This repository will store and generate un-official ranking of WWE Superstars. The ranking will be determined by using [Elo Rating System](https://www.hackerearth.com/blog/developers/elo-rating-system-common-link-facemash-chess/) (you might recognize it if you watch The Social Network film. It's the algorithm taught by Eduard Saverin to Mark Zuckeberg when he wants to create Facemash).

The latest ranking can be accessed [here](latest_rating.csv).

## Assumption and Rule
The assumption and rule applied to this ranking are determined as follows.
- The rating will be based on the win/loss record. Since I use Elo Rating System, the rate is not solely determined by the number of win or loss. How meaningful the win/loss will affect the rating as well (e.g. lower-tier wrestler that wins against high-tier wrestler will get a better boost rather than wins against the same-tier). Win/loss is only recorded if it happens in a match. So, if A pins B and then B beats up A until B stands tall in the final moment, the record will still show that A is the winner and B is the loser.

- Every wrestler will start with a base rating score of 2500. Higher rating means higher ranking (higher meaningful wins). The score will be reset after every draft (including single draft).

- DQ and Non Finish will be considered as draw

- A match with multiple participant, the rating will be updated based on the average expectation from the participant rating and average of other participant rating. For example, if we have Triple Threat for A, B, C. The rating and expecation will counted with (Rc, avg(Ra, Rb)), (Rb, avg(Ra, Rc)), (Rc, avg(Ra, Rb)) | TODO: Find a better way or justification?

- Note that Gauntlet match will be considered as a normal match since only two competitors wrestle at the same time.

- Only televised match (including PPV) are considered to update the ranking. Meaning that the ranking will be updated after RAW, Smackdown, and PPV (for now, I will exclude NXT since I do not follow it closely, help appreciated :p)

- Each tag team / faction / stable members will have their own rating. So, the rating for them might be different (since sometimes they book a 1-on-1 match to serve the feud).

- Squash matches with unamed jobbers will be ignored (since the jobbers, ideally, has 0 rating anyway)

- These assumptions and rule might be updated later. I create this just for fun, do not take it seriously! In the end, WWE product is a form of entertainment. We seek a pleasure by watching/discussing it.

