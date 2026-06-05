"""Extract a role-holder when multiple other people at the SAME company are distractors.
Difficulty controls distractor count: easy=2, medium=6, hard=12.
Only the target has the target role. Others have different roles at the same company."""

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

DISTRACTOR_COUNT = {"easy": 2, "medium": 6, "hard": 12}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n_dist = DISTRACTOR_COUNT[difficulty]

    people = rng.sample(NAMES, n_dist + 1)
    target_person = people[0]
    target_company = rng.choice(COMPANIES)
    target_role = rng.choice(ROLES)

    # Distractor roles: anything except the target role
    other_roles = [r for r in ROLES if r != target_role]

    facts = [f"{target_person} serves as {target_role} of {target_company}."]
    for i in range(n_dist):
        role = rng.choice(other_roles)
        facts.append(f"{people[i + 1]} serves as {role} of {target_company}.")

    rng.shuffle(facts)

    return {
        "inputs": {
            "facts": facts,
            "question": f"Who is the {target_role} of {target_company}?",
        },
        "expected": target_person,
        "check": {"type": "regex", "pattern": re.escape(target_person)},
    }
