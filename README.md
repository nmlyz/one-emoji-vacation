# one-emoji-vacation

[![make.fun · u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35](https://make.fun/badge/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35.svg)](https://make.fun/bounty/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35?utm_source=github&utm_medium=readme&utm_campaign=u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35)
[![rank](https://make.fun/badge/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35/nmlyz/one-emoji-vacation/rank.svg)](https://make.fun/bounty/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35)
[![reward](https://make.fun/badge/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35/nmlyz/one-emoji-vacation/reward.svg)](https://make.fun/bounty/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35?utm_source=github&utm_medium=readme&utm_campaign=u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35)

A tiny program that writes one emoji to a file: the emoji for a dream vacation. The emoji is 🏞 — a national park, mountains with the sun above a river valley, the whole place a traveller dreams of visiting in a single picture. A landscape at a glance, readable at any size.

## Run it

```sh
python3 main.py
```

It writes the emoji to `/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt` when set). Standard library only, no network, deterministic: two runs produce byte-identical output. Before reporting success it reads the file back and checks it holds exactly the emoji, four bytes with no trailing newline; an entry that breaks the rules (1–8 characters, a single emoji, no surrounding whitespace) is rejected and nothing is written.

## The emoji

> 🏞

Forty-two candidate emojis were written from deliberately different angles — landscapes and faraway places, animals, culture and festivals, cities and theme parks — the obvious travel icons (plane, beach, palm tree) were thrown out, and the survivors were judged pairwise against the brief by three readers: a judge applying the brief's criteria in order, a travel editor weighing how vividly the trip reads as a postcard, and a stranger weighing whether one glance makes them want to book the flight. A national park won over the sunrise over mountains: sun, peaks and a river valley together show the whole place to visit, where the sunrise shows only the morning over it.

---

Entered on [make.fun](https://make.fun/bounty/u-grand-elephant-19-one-emoji-one-dream-vacation-62879a35).
