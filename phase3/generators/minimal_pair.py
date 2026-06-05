"""Exactly two facts about similar entities. Question asks about one.
Easy: different first and last names. Medium: shared last name. Hard: shared last name
and similar roles.
Pure discrimination test: no distractors, just two facts that could be confused."""

import random
import re

SIMILAR_PAIRS = [
    ("Dr. Wei Lin", "Dr. Amy Lin"),
    ("Rachel Torres", "Elena Torres"),
    ("Nina Patel", "Maya Patel"),
    ("Alice Chen", "Sarah Chen"),
    ("Alex Rivera", "Carlos Rivera"),
    ("Bob Martinez", "Rosa Martinez"),
    ("Jack Wilson", "Kate Wilson"),
    ("Leo Fischer", "Anna Fischer"),
]

DISTINCT_PAIRS = [
    ("Alice Chen", "Bob Martinez"),
    ("Carol Smith", "David Kim"),
    ("Eva Johansson", "Frank Okafor"),
    ("Grace Liu", "Henry Brown"),
    ("Iris Yamamoto", "Jack Wilson"),
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
    "Horizon Tech", "Meridian Data", "Forge Robotics", "Helios Cloud", "Nova Logic",
]

ROLES = ["CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
         "Head of Research", "Chief Scientist", "COO", "VP of Marketing", "Head of Product"]

# Roles that sound similar
SIMILAR_ROLES = [
    ("CTO", "VP of Technology"),
    ("CEO", "Managing Director"),
    ("Head of Research", "Chief Scientist"),
    ("VP of Engineering", "Head of Engineering"),
    ("CFO", "VP of Finance"),
]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    if difficulty == "easy":
        pair = rng.choice(DISTINCT_PAIRS)
        roles = rng.sample(ROLES, 2)
    elif difficulty == "medium":
        pair = rng.choice(SIMILAR_PAIRS)
        roles = rng.sample(ROLES, 2)
    else:  # hard
        pair = rng.choice(SIMILAR_PAIRS)
        role_pair = rng.choice(SIMILAR_ROLES)
        roles = list(role_pair)
        rng.shuffle(roles)

    companies = rng.sample(COMPANIES, 2)
    target_idx = rng.randint(0, 1)
    target = pair[target_idx]
    other = pair[1 - target_idx]

    facts = [
        f"{pair[0]} serves as {roles[0]} of {companies[0]}.",
        f"{pair[1]} serves as {roles[1]} of {companies[1]}.",
    ]
    rng.shuffle(facts)

    return {
        "inputs": {
            "facts": facts,
            "question": f"What is {target}'s role?",
        },
        "expected": roles[target_idx],
        "check": {"type": "regex", "pattern": re.escape(roles[target_idx])},
    }
