"""Given N people at various companies, count how many work at a target company.
Difficulty controls total people and target count: easy=2/4, medium=3/8, hard=5/12.
Tests counting: model must scan all facts and tally correctly."""

import random

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
    "Karen Singh", "Leo Fischer", "Maya Patel", "Nate Cooper", "Olivia Rossi",
    "Pablo Mendez", "Quinn O'Brien", "Rosa Garcia", "Sam Thompson", "Tara Nguyen",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
    "Horizon Tech", "Meridian Data", "Forge Robotics", "Helios Cloud", "Nova Logic",
]

ROLES = [
    "CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
    "Head of Research", "Chief Scientist", "COO", "VP of Marketing", "Head of Product",
]

SETTINGS = {"easy": (2, 4), "medium": (3, 8), "hard": (5, 12)}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    target_count, total = SETTINGS[difficulty]

    people = rng.sample(NAMES, total)
    companies = rng.sample(COMPANIES, 2)
    target_company = companies[0]
    other_company = companies[1]

    facts = []
    for i in range(total):
        company = target_company if i < target_count else other_company
        role = rng.choice(ROLES)
        facts.append(f"{people[i]} serves as {role} of {company}.")

    rng.shuffle(facts)

    return {
        "inputs": {
            "facts": facts,
            "question": f"How many people work at {target_company}?",
        },
        "expected": str(target_count),
        "check": {"type": "regex", "pattern": rf"\b{target_count}\b"},
    }
