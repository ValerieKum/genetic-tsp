# Genetic Algorithm: Traveling Salesman

A genetic algorithm evolves shorter and shorter routes through a set of cities, one generation at a time.

Part of my portfolio of small, from-scratch visualisations of computer-science ideas. Built on numpy and matplotlib, so every moving part is visible.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python tsp_genetic.py                  # live animated window
python tsp_genetic.py --save out.gif   # export a looping GIF
python tsp_genetic.py --save out.mp4   # smaller file, best for the web (needs ffmpeg)
```
