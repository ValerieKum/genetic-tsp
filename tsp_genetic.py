from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.viz import (PALETTE, card_figure, caption, save_animation,
                        use_headless_if_saving)

# ---- tunables -------------------------------------------------------------
N_CITIES = 14
POP_SIZE = 250
MUTATION = 0.15
GENS_PER_FRAME = 1
TOTAL_FRAMES = 160


def tour_len(order, cities):
    pts = cities[order]
    d = np.diff(np.vstack([pts, pts[0]]), axis=0)
    return np.sqrt((d ** 2).sum(1)).sum()


def ordered_crossover(a, b):
    n = len(a)
    i, j = sorted(np.random.randint(0, n, 2))
    child = -np.ones(n, dtype=int)
    child[i:j] = a[i:j]
    fill = [c for c in b if c not in a[i:j]]
    k = 0
    for p in range(n):
        if child[p] == -1:
            child[p] = fill[k]
            k += 1
    return child


def mutate(order):
    if np.random.rand() < MUTATION:
        i, j = np.random.randint(0, len(order), 2)
        order[i], order[j] = order[j], order[i]
    return order


def evolve(pop, cities):
    lengths = np.array([tour_len(p, cities) for p in pop])
    fitness = 1.0 / lengths
    order = np.argsort(lengths)
    elite = [pop[i].copy() for i in order[:2]]   # keep the best 2 unchanged
    probs = fitness / fitness.sum()
    new = elite
    while len(new) < len(pop):
        a, b = pop[np.random.choice(len(pop), p=probs)], \
               pop[np.random.choice(len(pop), p=probs)]
        new.append(mutate(ordered_crossover(a, b)))
    return new, lengths[order[0]], pop[order[0]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", metavar="OUT.gif")
    args = ap.parse_args()
    use_headless_if_saving(args.save)

    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    cities = np.random.rand(N_CITIES, 2)
    pop = [np.random.permutation(N_CITIES) for _ in range(POP_SIZE)]

    fig, ax = card_figure()
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.08, 1.08)
    ax.set_aspect("equal")

    (route_line,) = ax.plot([], [], color=PALETTE["pink"], lw=1.8, alpha=0.9)
    ax.scatter(cities[:, 0], cities[:, 1], s=42, color=PALETTE["orange"],
               zorder=3, edgecolors=PALETTE["bg"], linewidths=1.2)
    txt = caption(ax, "")

    state = {"pop": pop, "best": None}

    def render(frame):
        for _ in range(GENS_PER_FRAME):
            state["pop"], best_len, best = evolve(state["pop"], cities)
            state["best"] = best
        loop = np.append(state["best"], state["best"][0])
        route_line.set_data(cities[loop, 0], cities[loop, 1])
        txt.set_text(f"gen {frame * GENS_PER_FRAME:>3}   len {best_len:.2f}")
        return route_line, txt

    anim = FuncAnimation(fig, render, frames=TOTAL_FRAMES, interval=60,
                         blit=True)

    if args.save:
        save_animation(anim, args.save, fps=20)
    else:
        plt.show()


if __name__ == "__main__":
    main()
