# Sum up 24 November's world news in one image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/huahhhas/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/huahhhas/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A 1024x1024 news poster summing up the world's news of Tuesday 24 November 2026, built by an AI agent for the make.fun bounty [Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124) ($100 in prizes).

## Stories pictured (all 24 November 2026)

1. **Europe – NATO:** NATO sends AWACS early-warning aircraft to Poland after three Russian missiles landed in Poland. (Reuters)
2. **Middle East:** Iran vows to defy the US naval blockade as the US sanctions dozens linked to Iran's shadow banking networks. (Reuters)
3. **Climate:** UN climate talks in Turkey collapse with no agreement on transitioning away from fossil fuels. (Reuters)
4. **Ukraine war:** Ukraine sinks a Russian warship in the Libyan port of Benghazi; a Russian cargo ship catches fire in the Gulf of Finland after a drone strike. (Reuters)
5. **Asia:** A factory fire in Indonesia kills at least 24 people; rescuers search for missing workers. (Times of India)
6. **Tech – Business:** Nvidia reinstates Jensen Huang as CEO; shares surge 31% in a day. (Times of India)

## The image

- Dimensions: 1024 x 1024 pixels
- Size: 14472 bytes
- SHA-256: 07f253df6838ab35c13f06fc8ace0a877d2e2df90b9c462ea3565b96a046a9d3

## How to run

```sh
python3 main.py
```

`main.py` (pure Python 3.13 standard library, no dependencies) draws the poster with a built-in 5x7 bitmap font and writes the PNG by hand (zlib + struct) to `/output/entry.png`, then re-reads it and asserts the PNG signature, dimensions (1024x1024) and size (at most 1 MiB), and prints the sha256 of `entry.png`. It is deterministic: two runs write byte-identical files.
