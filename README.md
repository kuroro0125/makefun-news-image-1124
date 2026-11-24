# The World Today — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kuroro0125/makefun-news-image-1124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kuroro0125/makefun-news-image-1124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page newspaper front page summing up the world's news of
Tuesday, 24 November 2026, built for the make.fun competition
[news-image-20261124](https://make.fun/bounty/news-image-20261124).

## The day's news

- **Lead — War at sea:** Ukraine says seven sea drones struck a Russian
  naval base at Benghazi, Libya, destroying a Ka-27 helicopter and
  hitting the cargo ship MV Angara.
- **The toll:** hacked Russian data puts the number of Russian soldiers
  killed since February 2022 at close to half a million.
- **Technology:** Nvidia rehires Jensen Huang as chief executive days
  after his ouster, after President Trump pressed the board.
- **In brief:** a possible Russian nuclear space weapon, the 2031
  Women's World Cup hosts, the collapse of the COP31 climate talks,
  and a Honda recall of 810,000 vehicles.

## How it works

`render.py` draws the whole front page with Pillow — masthead, lead
story with a drawn sea scene, a toll chart, a chip illustration, and a
briefs strip — deterministically: rendering twice produces identical
bytes. `main.py` is the entrypoint: it copies the shipped `entry.png`
to the output directory.

```sh
python3 render.py        # regenerate entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Standard library plus Pillow for the renderer; the entrypoint itself
uses only the standard library and no network.

## Licence

MIT — see [LICENSE](LICENSE).
