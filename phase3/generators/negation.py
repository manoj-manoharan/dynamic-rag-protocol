"""Given N people, N-1 at the target company and 1 elsewhere, identify the outsider.
Difficulty controls group size: easy=3 total, medium=5, hard=8.
Tests negation reasoning: model must check each person and find the exception."""

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
    "Prism Analytics", "Zenith Networks", "Apex Software", "Lunar Computing", "Titan Digital",
]

ROLES = [
    "CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
    "Head of Research", "Chief Scientist", "COO", "VP of Marketing", "Head of Product",
]

TOTAL_PEOPLE = {"easy": 3, "medium": 5, "hard": 8}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n = TOTAL_PEOPLE[difficulty]

    people = rng.sample(NAMES, n)
    companies = rng.sample(COMPANIES, 2)
    target_company = companies[0]
    other_company = companies[1]

    # First person is the answer (works elsewhere)
    answer = people[0]
    answer_role = rng.choice(ROLES)

    facts = [f"{answer} serves as {answer_role} of {other_company}."]
    for i in range(1, n):
        role = rng.choice(ROLES)
        facts.append(f"{people[i]} serves as {role} of {target_company}.")

    rng.shuffle(facts)

    return {
        "inputs": {
            "facts": facts,
            "question": f"Which person does NOT work at {target_company}?",
        },
        "expected": answer,
        "check": {"type": "regex", "pattern": re.escape(answer)},
    }
