"""Same person-role-company fact expressed in varied syntactic structures.
Easy: active/passive (standard). Medium: compound/relative/nominalized. Hard: inverted/dense/informal.
If the model fails on hard, it means sentence parsing breaks at complex surface forms."""

import random
import re

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
    "Karen Singh", "Leo Fischer", "Maya Patel", "Nate Cooper", "Olivia Rossi",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
    "Horizon Tech", "Meridian Data", "Forge Robotics", "Helios Cloud", "Nova Logic",
]

ROLES = [
    "CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
    "Head of Research", "Chief Scientist", "COO", "VP of Marketing", "Head of Product",
]


def _make(person, role, company, form, rng):
    first = person.split()[0]
    if form == "active":
        return rng.choice([
            f"{person} serves as {role} of {company}.",
            f"{person} holds the position of {role} at {company}.",
            f"{person} is the {role} of {company}.",
        ])
    if form == "passive":
        return rng.choice([
            f"The {role} position at {company} is held by {person}.",
            f"{company}'s {role} is {person}.",
            f"The role of {role} at {company} has been filled by {person}.",
        ])
    if form == "compound":
        return rng.choice([
            f"{person}, who joined in 2023, currently serves as {role} of {company}.",
            f"After years in the industry, {person} now serves as {role} of {company}.",
            f"A veteran executive, {person} serves as {role} of {company}.",
        ])
    if form == "relative":
        return rng.choice([
            f"The person who holds the {role} position at {company} is {person}.",
            f"It is {person} who serves as {role} at {company}.",
            f"{company}'s {role}, appointed last year, is {person}.",
        ])
    if form == "nominalized":
        return rng.choice([
            f"{person}'s current role at {company} is {role}.",
            f"The current {role} appointment at {company} belongs to {person}.",
        ])
    if form == "inverted":
        return rng.choice([
            f"As {role}, {person} leads the executive team at {company}.",
            f"In the role of {role}, {person} oversees operations at {company}.",
            f"Serving as {role}, {person} directs {company}'s strategy.",
        ])
    if form == "dense":
        return rng.choice([
            f"Following the Q3 board meeting, {company} appointed {person} as {role}, effective immediately.",
            f"In a move announced Tuesday, {person} was named {role} of {company}, succeeding the outgoing executive.",
            f"The board of {company} confirmed {person} as the new {role} during yesterday's emergency session.",
        ])
    if form == "informal":
        return rng.choice([
            f"{first} is running things over at {company} as {role} now.",
            f"So {first} got the {role} gig at {company}.",
            f"{first} took over as {role} at {company} a few months back.",
        ])


FORMS = {
    "easy": ["active", "passive"],
    "medium": ["compound", "relative", "nominalized"],
    "hard": ["inverted", "dense", "informal"],
}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    person = rng.choice(NAMES)
    company = rng.choice(COMPANIES)
    role = rng.choice(ROLES)
    form = rng.choice(FORMS[difficulty])

    fact = _make(person, role, company, form, rng)

    return {
        "inputs": {
            "facts": [fact],
            "question": f"Who is the {role} of {company}?",
        },
        "expected": person,
        "check": {"type": "regex", "pattern": re.escape(person)},
    }
