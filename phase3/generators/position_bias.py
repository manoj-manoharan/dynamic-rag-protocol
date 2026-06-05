"""Same extraction task with answer fact placed at different positions in context.
Difficulty encodes position: easy=first, medium=middle, hard=last.
Tests whether the model attends equally to all positions or has recency/primacy bias.
Fixed 10 facts total. Compare accuracy across positions to detect bias."""

import random
import re

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

N_FACTS = 10
POSITION = {"easy": "first", "medium": "middle", "hard": "last"}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    people = rng.sample(NAMES, N_FACTS)
    companies = rng.sample(COMPANIES, N_FACTS)
    roles = [rng.choice(ROLES) for _ in range(N_FACTS)]

    target_person = people[0]
    target_company = companies[0]
    target_role = roles[0]

    target_fact = f"{target_person} serves as {target_role} of {target_company}."
    other_facts = [
        f"{people[i]} serves as {roles[i]} of {companies[i]}."
        for i in range(1, N_FACTS)
    ]
    rng.shuffle(other_facts)

    pos = POSITION[difficulty]
    if pos == "first":
        facts = [target_fact] + other_facts
    elif pos == "middle":
        mid = len(other_facts) // 2
        facts = other_facts[:mid] + [target_fact] + other_facts[mid:]
    else:
        facts = other_facts + [target_fact]

    return {
        "inputs": {
            "facts": facts,
            "question": f"Who is the {target_role} of {target_company}?",
        },
        "expected": target_person,
        "check": {"type": "regex", "pattern": re.escape(target_person)},
    }
