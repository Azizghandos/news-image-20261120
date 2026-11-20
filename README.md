# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Azizghandos/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Azizghandos/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A program that draws one front-page infographic summing up Friday 20 November 2026's world news — the ICJ's genocide ruling against Myanmar, the Trump–Xi–Putin summit in Shenzhen, Russia's strikes on Kyiv's bridges, the Houthi missile hit on Riyadh's PIF Tower, markets tumbling on AI fears, and more — as a single 1024×1024 image.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the pre-drawn `entry.png` (drawn by `make-image.py` with Pillow) to the output directory. The program runs with no network and writes the same bytes on every run.

---

<sub>Entered on [make.fun](https://make.fun/?ref=660zm28c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
