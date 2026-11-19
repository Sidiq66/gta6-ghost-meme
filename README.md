# gta6-ghost-meme

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Sidiq66/gta6-ghost-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Sidiq66/gta6-ghost-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

One meme for make.fun's "Post a GTA 6 meme on X" bounty, posted on X: a gamer who waited 13 years for GTA 6 has grown a grey beard on the couch, controller in hand, watching the download bar stick at 99% — while the make.fun ghost, his AI agent, sits beside him having already won real money on make.fun before the game even finished downloading. The picture (`meme.png`, 1080×1080) composites the official make.fun ghost mark from the make.fun press kit into an AI-generated Vice City gamer-room scene; `build_meme.py` cuts the ghost out of its magenta disc, seats it in the room and letters the captions. `main.ts` hands the house the post's address: it copies `POST.json` to the output directory and prints nothing on success.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=x9j98tfg&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
