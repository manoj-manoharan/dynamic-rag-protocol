"""Fact contains multiple dates/times. Model must extract the one asked about.
Easy: single date. Medium: two dates (start and end). Hard: three dates (appointed,
predecessor's tenure, effective date).
Tests precise temporal extraction under distraction from other timestamps."""

import random

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
]

PREDECESSORS = [
    "Tom Walker", "Sandra Lee", "Marcus Young", "Diana Cruz", "Paul Foster",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
]

ROLES = ["CEO", "CTO", "CFO", "VP of Engineering", "Head of Research"]

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    person = rng.choice(NAMES)
    company = rng.choice(COMPANIES)
    role = rng.choice(ROLES)

    if difficulty == "easy":
        month = rng.choice(MONTHS)
        year = rng.choice([2023, 2024, 2025])
        fact = f"{person} was appointed {role} of {company} in {month} {year}."
        return {
            "inputs": {"facts": [fact], "question": f"When was {person} appointed?"},
            "expected": f"{month} {year}",
            "check": {"type": "regex_all", "patterns": [month, str(year)]},
        }

    if difficulty == "medium":
        start_month = rng.choice(MONTHS[:6])
        end_month = rng.choice(MONTHS[6:])
        year = rng.choice([2023, 2024])
        predecessor = rng.choice(PREDECESSORS)
        fact = (
            f"{predecessor} served as {role} of {company} from {start_month} "
            f"until {end_month} {year}, when {person} took over."
        )
        return {
            "inputs": {
                "facts": [fact],
                "question": f"When did {person} take over as {role}?",
            },
            "expected": f"{end_month} {year}",
            "check": {"type": "regex_all", "patterns": [end_month, str(year)]},
        }

    # hard: three dates
    predecessor = rng.choice(PREDECESSORS)
    hire_year = 2019
    depart_month = rng.choice(MONTHS[:6])
    depart_year = 2024
    effective_month = rng.choice(MONTHS[6:])
    effective_year = 2024
    fact = (
        f"{predecessor}, who joined {company} in {hire_year}, stepped down as {role} "
        f"in {depart_month} {depart_year}. {person} was announced as successor, "
        f"effective {effective_month} {effective_year}."
    )
    return {
        "inputs": {
            "facts": [fact],
            "question": f"When does {person} officially start as {role}?",
        },
        "expected": f"{effective_month} {effective_year}",
        "check": {"type": "regex_all", "patterns": [effective_month, str(effective_year)]},
    }
