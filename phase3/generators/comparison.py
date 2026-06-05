"""Given N items with numeric values, identify which has the largest.
Difficulty controls item count: easy=2, medium=4, hard=6.
Tests quantitative comparison: model must parse numbers and compare."""

import random
import re

PROJECTS = [
    "Project Alpha", "Project Beta", "Project Gamma", "Project Delta",
    "Project Epsilon", "Project Omega", "Project Sigma", "Project Theta",
    "Project Zenith", "Project Nova", "Project Apex", "Project Forge",
]

ITEM_COUNT = {"easy": 2, "medium": 4, "hard": 6}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n = ITEM_COUNT[difficulty]

    projects = rng.sample(PROJECTS, n)

    # Generate unique budgets
    budgets = rng.sample(range(200, 1600, 50), n)

    facts = [f"{projects[i]} has a budget of ${budgets[i]}K." for i in range(n)]
    rng.shuffle(facts)

    max_idx = budgets.index(max(budgets))
    winner = projects[max_idx]

    return {
        "inputs": {
            "facts": facts,
            "question": "Which project has the largest budget?",
        },
        "expected": winner,
        "check": {"type": "regex", "pattern": re.escape(winner)},
    }
