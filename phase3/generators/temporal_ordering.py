"""Given N chronological updates to the same property, identify the current (latest) value.
Difficulty controls update count: easy=2, medium=4, hard=8.
Tests temporal reasoning: model must identify recency, not just any mentioned value."""

import random
import re

PROJECTS = [
    "Project Alpha", "Project Beta", "Project Gamma", "Project Delta",
    "Project Epsilon", "Project Omega", "Project Sigma", "Project Theta",
    "Project Zenith", "Project Nova", "Project Apex", "Project Forge",
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

UPDATE_COUNT = {"easy": 2, "medium": 4, "hard": 8}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n = UPDATE_COUNT[difficulty]

    project = rng.choice(PROJECTS)
    month_indices = sorted(rng.sample(range(12), n))

    # Generate budgets that change each update
    budget = rng.randint(3, 8) * 100
    budgets = [budget]
    for _ in range(n - 1):
        budget += rng.choice([-150, -100, -50, 50, 100, 150, 200])
        budget = max(100, budget)
        budgets.append(budget)

    facts = []
    for i, (m_idx, b) in enumerate(zip(month_indices, budgets)):
        month = MONTHS[m_idx]
        if i == 0:
            facts.append(f"In {month} 2024, {project} had an initial budget of ${b}K.")
        else:
            facts.append(f"In {month} 2024, {project} budget was revised to ${b}K.")

    rng.shuffle(facts)
    latest = budgets[-1]

    return {
        "inputs": {
            "facts": facts,
            "question": f"What is the current budget of {project}? State only the latest amount.",
        },
        "expected": f"${latest}K",
        "check": {"type": "regex", "pattern": str(latest)},
    }
