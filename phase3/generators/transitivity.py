"""A is married to B, B works at C. Question: where does A's spouse work?
All facts provided together (single-hop reading, not multi-step orchestration).
Difficulty controls distractor count: easy=1, medium=4, hard=8.
Tests whether the model can follow a 2-step chain within provided facts."""

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

DISTRACTOR_COUNT = {"easy": 1, "medium": 4, "hard": 8}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n_dist = DISTRACTOR_COUNT[difficulty]

    all_people = rng.sample(NAMES, 2 + n_dist)
    person_a = all_people[0]
    person_b = all_people[1]
    target_company = rng.choice(COMPANIES)
    target_role = rng.choice(ROLES)

    core_facts = [
        f"{person_a} is married to {person_b}.",
        f"{person_b} serves as {target_role} of {target_company}.",
    ]

    distractor_facts = []
    other_companies = [c for c in COMPANIES if c != target_company]
    for i in range(n_dist):
        p = all_people[2 + i]
        c = rng.choice(other_companies)
        r = rng.choice(ROLES)
        distractor_facts.append(f"{p} serves as {r} of {c}.")

    all_facts = core_facts + distractor_facts
    rng.shuffle(all_facts)

    return {
        "inputs": {
            "facts": all_facts,
            "question": f"Where does {person_a}'s spouse work?",
        },
        "expected": target_company,
        "check": {"type": "regex", "pattern": re.escape(target_company)},
    }
