"""Fact contains multiple numbers. Model must extract the specific one asked about.
Easy: one clear number. Medium: two numbers, pick the right one. Hard: numbers with
percentages and comparisons that could confuse.
Tests precise numeric extraction under distraction from other numbers."""

import random


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    projects = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta",
                "Project Epsilon", "Project Omega", "Project Sigma"]
    project = rng.choice(projects)

    if difficulty == "easy":
        budget = rng.randint(3, 12) * 100
        fact = f"{project} has a budget of ${budget}K."
        return {
            "inputs": {"facts": [fact], "question": f"What is the budget of {project}?"},
            "expected": f"${budget}K",
            "check": {"type": "regex", "pattern": str(budget)},
        }

    if difficulty == "medium":
        old_budget = rng.randint(3, 8) * 100
        new_budget = old_budget + rng.choice([100, 150, 200, 250])
        fact = f"{project}'s budget was revised from ${old_budget}K to ${new_budget}K."
        return {
            "inputs": {
                "facts": [fact],
                "question": f"What is the current budget of {project}?",
            },
            "expected": f"${new_budget}K",
            "check": {"type": "regex", "pattern": str(new_budget)},
        }

    # hard: multiple numbers including percentages
    old_budget = rng.randint(3, 8) * 100
    new_budget = old_budget + rng.choice([100, 150, 200])
    pct = round((new_budget - old_budget) / old_budget * 100)
    headcount = rng.randint(8, 25)
    fact = (
        f"{project}'s budget increased from ${old_budget}K to ${new_budget}K, "
        f"a {pct}% increase, while the team size remained at {headcount} members."
    )
    # Ask about the OLD budget to test if model picks the first number
    return {
        "inputs": {
            "facts": [fact],
            "question": f"What was {project}'s original budget before the increase?",
        },
        "expected": f"${old_budget}K",
        "check": {"type": "regex", "pattern": str(old_budget)},
    }
