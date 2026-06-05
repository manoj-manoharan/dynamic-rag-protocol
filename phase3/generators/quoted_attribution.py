"""Fact is attributed to a source rather than directly asserted.
Easy: answer a factual question where attribution doesn't matter.
Medium: ask whether the claim is confirmed (should note attribution).
Hard: attributed claim contradicts another fact; model must distinguish.
Tests whether the model recognizes "X said Y" is not the same as "Y is true"."""

import random
import re

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
]

SOURCES = [
    "industry analysts", "internal documents", "a company spokesperson",
    "anonymous sources", "a leaked memo", "the quarterly report",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
]

PROJECTS = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta"]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    company = rng.choice(COMPANIES)
    source = rng.choice(SOURCES)
    project = rng.choice(PROJECTS)
    person = rng.choice(NAMES)

    if difficulty == "easy":
        # Attribution present but question is about a simple fact within it
        budget = rng.randint(3, 9) * 100
        fact = f"According to {source}, {project} at {company} has a budget of ${budget}K."
        return {
            "inputs": {
                "facts": [fact],
                "question": f"What budget is reported for {project}?",
            },
            "expected": f"${budget}K",
            "check": {"type": "regex", "pattern": str(budget)},
        }

    if difficulty == "medium":
        # Ask whether the claim is confirmed
        fact = f"{person} claimed that {company} is planning to acquire {rng.choice(COMPANIES)}."
        return {
            "inputs": {
                "facts": [fact],
                "question": f"Is {company} planning an acquisition? Is this confirmed?",
            },
            "expected": "claimed by source, not confirmed",
            "check": {
                "type": "regex",
                "pattern": r"claim|alleged|not confirmed|unverified|according to|stated|assert|not .+ fact",
            },
        }

    # hard: two facts, one asserted and one attributed, they conflict
    budget_real = rng.randint(5, 8) * 100
    budget_claimed = budget_real + rng.choice([200, 300, 400])
    facts = [
        f"{company}'s official filing shows {project} has a budget of ${budget_real}K.",
        f"{person} claimed that {project}'s budget is actually ${budget_claimed}K.",
    ]
    rng.shuffle(facts)
    return {
        "inputs": {
            "facts": facts,
            "question": f"What is the confirmed budget of {project}?",
        },
        "expected": f"${budget_real}K (official), ${budget_claimed}K (claimed)",
        "check": {"type": "regex", "pattern": str(budget_real)},
    }
