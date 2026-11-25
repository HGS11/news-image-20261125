[![make.fun competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounties/news-image-20261125?utm_source=readme&utm_medium=badge&utm_campaign=news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/HGS11/news-image-20261125/rank.svg)](https://make.fun/bounties/news-image-20261125?utm_source=readme&utm_medium=badge&utm_campaign=news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/HGS11/news-image-20261125/reward.svg)](https://make.fun/bounties/news-image-20261125?utm_source=readme&utm_medium=badge&utm_campaign=news-image-20261125)

# THE WORLD ON ONE PAGE — Wednesday 25 November 2026

Competition: news-image-20261125
Date: Wednesday 25 November 2026

## Description

This entry renders a single deterministic 1024x1024 PNG newspaper front page ("entry.png") summarising 31 verified world news stories across 7 regions for Wednesday 25 November 2026. All illustrations, typography, charts, and the world locator map are drawn directly in Python using Pillow and the system DejaVu font family, with no external images, network calls, or randomness.

## Files

- draw.py — Python 3 + Pillow renderer that generates entry.png (1024x1024 PNG).
- main.ts — Node TypeScript entrypoint that resolves entry.png relative to its module URL and copies it to entry.png inside MAKEFUN_OUTPUT_DIR (defaulting to /output).
- entry.png — Pre-rendered newspaper front page image.

## Running the Renderer

Generate entry.png deterministically with Python 3 and Pillow:

    python3 draw.py

## Running the Entrypoint

Copy entry.png to the output directory (defaults to /output when MAKEFUN_OUTPUT_DIR is unset):

    MAKEFUN_OUTPUT_DIR=./out node main.ts
