"""Given N person-role-company facts, ask who holds a specific role at a specific company.
Difficulty controls total fact count: easy=3, medium=8, hard=15.
All facts are same structure (person-role-company), answer is unique."""

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

FACT_COUNT = {"easy": 3, "medium": 8, "hard": 15}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n = FACT_COUNT[difficulty]

    people = rng.sample(NAMES, n)
    companies = rng.sample(COMPANIES, n)
    roles = [rng.choice(ROLES) for _ in range(n)]

    # Target is index 0
    target_person = people[0]
    target_company = companies[0]
    target_role = roles[0]

    facts = [f"{people[i]} serves as {roles[i]} of {companies[i]}." for i in range(n)]
    rng.shuffle(facts)

    return {
        "inputs": {
            "facts": facts,
            "question": f"Who is the {target_role} of {target_company}?",
        },
        "expected": target_person,
        "check": {"type": "regex", "pattern": re.escape(target_person)},
    }
