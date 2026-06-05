"""Single fact containing 3-4 data points. Question asks about one specific piece.
Easy: ask about the most prominent piece (person's name). Medium: secondary piece (date/salary).
Hard: deeply embedded detail (percentage, predecessor name).
Tests selective extraction from information-dense facts."""

import random
import re

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
    "Karen Singh", "Leo Fischer", "Maya Patel", "Nate Cooper", "Olivia Rossi",
]

PREDECESSORS = [
    "Tom Walker", "Sandra Lee", "Marcus Young", "Diana Cruz", "Paul Foster",
    "Emily Shaw", "Victor Huang", "Laura Price", "Nathan Cole", "Julia Ross",
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
    predecessor = rng.choice(PREDECESSORS)
    company = rng.choice(COMPANIES)
    role = rng.choice(ROLES)
    month = rng.choice(MONTHS)
    year = rng.choice([2023, 2024, 2025])
    salary = rng.choice([250, 300, 350, 400, 450, 500, 550, 600])

    fact = (
        f"{person} was appointed {role} of {company} in {month} {year}, "
        f"replacing {predecessor}, with an annual compensation of ${salary}K."
    )

    if difficulty == "easy":
        return {
            "inputs": {"facts": [fact], "question": f"Who is the {role} of {company}?"},
            "expected": person,
            "check": {"type": "regex", "pattern": re.escape(person)},
        }

    if difficulty == "medium":
        return {
            "inputs": {"facts": [fact], "question": f"When was {person} appointed {role}?"},
            "expected": f"{month} {year}",
            "check": {"type": "regex_all", "patterns": [month, str(year)]},
        }

    # hard: ask about the embedded detail
    q = rng.choice([
        (f"Who did {person} replace as {role}?", predecessor, re.escape(predecessor)),
        (f"What is {person}'s annual compensation?", f"${salary}K", str(salary)),
    ])
    return {
        "inputs": {"facts": [fact], "question": q[0]},
        "expected": q[1],
        "check": {"type": "regex", "pattern": q[2]},
    }
