"""Same simple fact, but the question is phrased differently.
Easy: direct question. Medium: indirect/role-focused. Hard: circumlocuted/contextual.
Tests whether the model can match varied question forms to a standard fact."""

import random
import re

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
    "Horizon Tech", "Meridian Data", "Forge Robotics", "Helios Cloud", "Nova Logic",
]

ROLES = [
    "CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
    "Head of Research", "Chief Scientist", "COO", "VP of Marketing", "Head of Product",
]


def _question(role, company, person, difficulty, rng):
    if difficulty == "easy":
        return rng.choice([
            f"Who is the {role} of {company}?",
            f"Who serves as {role} at {company}?",
            f"Who holds the {role} role at {company}?",
        ])
    if difficulty == "medium":
        return rng.choice([
            f"What role does {person} hold?",
            f"What is {person}'s position at {company}?",
            f"In what capacity does {person} work at {company}?",
        ])
    # hard
    return rng.choice([
        f"If I needed to reach the top technical leader at {company}, who should I contact?",
        f"Someone needs to discuss executive matters with {company}'s leadership. Who leads the organization?",
        f"Who would represent {company} at a meeting requiring their most senior relevant officer?",
    ])


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    person = rng.choice(NAMES)
    company = rng.choice(COMPANIES)
    role = rng.choice(ROLES)

    fact = f"{person} serves as {role} of {company}."
    question = _question(role, company, person, difficulty, rng)

    # For medium difficulty, answer is the role not the person
    if difficulty == "medium":
        return {
            "inputs": {"facts": [fact], "question": question},
            "expected": role,
            "check": {"type": "regex", "pattern": re.escape(role)},
        }

    return {
        "inputs": {"facts": [fact], "question": question},
        "expected": person,
        "check": {"type": "regex", "pattern": re.escape(person)},
    }
