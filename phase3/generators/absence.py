"""Given N people with roles at a company, ask about a role nobody holds. Answer is no.
Difficulty controls fact count and distractor similarity: easy=3 facts with distinct roles,
medium=6 facts, hard=10 facts with roles similar to the absent one.
Tests absence reasoning: model must distinguish 'not stated' from 'false'."""

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

# (absent_role, easy_distractors, hard_distractors_that_look_similar)
ABSENCE_CONFIGS = [
    ("CTO", ["CEO", "CFO", "COO", "VP of Sales"], ["VP of Technology", "Head of Engineering", "Chief Architect", "Tech Lead"]),
    ("CFO", ["CEO", "CTO", "COO", "VP of Sales"], ["VP of Finance", "Head of Accounting", "Financial Director", "Budget Manager"]),
    ("CEO", ["CTO", "CFO", "COO", "VP of Sales"], ["President", "Managing Director", "General Manager", "Board Chair"]),
    ("Head of Research", ["CEO", "CTO", "CFO", "COO"], ["Senior Researcher", "Lead Scientist", "Research Fellow", "Chief Scientist"]),
    ("VP of Marketing", ["CEO", "CTO", "CFO", "COO"], ["Marketing Director", "Head of Brand", "Communications Lead", "Growth Manager"]),
]

FACT_COUNT = {"easy": 3, "medium": 6, "hard": 10}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    n = FACT_COUNT[difficulty]
    config = rng.choice(ABSENCE_CONFIGS)
    absent_role = config[0]

    people = rng.sample(NAMES, n)
    company = rng.choice(COMPANIES)

    if difficulty == "hard":
        # Mix similar-looking roles with normal ones
        similar = config[2]
        normal = config[1]
        available = similar + normal
    else:
        available = config[1]

    facts = []
    for i in range(n):
        role = rng.choice(available)
        facts.append(f"{people[i]} serves as {role} of {company}.")
    rng.shuffle(facts)

    return {
        "inputs": {
            "facts": facts,
            "question": f"Does anyone serve as {absent_role} of {company}?",
        },
        "expected": "No",
        "check": {
            "type": "regex",
            "pattern": r"\b(no|not|none|nobody|no one|cannot determine|isn't|doesn't|does not|no mention)\b",
        },
    }
