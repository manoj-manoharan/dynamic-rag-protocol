"""Given a sentence and a list of known entities, identify which appear.
Difficulty controls list size: easy=6, medium=15, hard=25.
Sentences always contain 2-3 entities from the list. Model must find them in a larger set."""

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
    "Prism Analytics", "Zenith Networks", "Apex Software", "Lunar Computing", "Titan Digital",
]

# Templates: {p} = person, {c} = company
TEMPLATES_PC = [
    "{p} joined {c} as a senior engineer.",
    "{p} was promoted to a leadership role at {c}.",
    "{c} announced that {p} will lead the new initiative.",
    "{p} presented the quarterly results for {c}.",
    "{p} transitioned to a new position at {c}.",
]

# Templates: {p1}, {p2} = people, {c} = company
TEMPLATES_PPC = [
    "{p1} and {p2} joined {c} for the summer program.",
    "{c} hired {p1} and {p2} for the new division.",
    "{p1} introduced {p2} to the leadership team at {c}.",
]

SETTINGS = {
    "easy": {"n_present": 2, "n_list": 6},
    "medium": {"n_present": 2, "n_list": 15},
    "hard": {"n_present": 3, "n_list": 25},
}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    cfg = SETTINGS[difficulty]
    n_present = cfg["n_present"]
    n_list = cfg["n_list"]

    all_entities = NAMES + COMPANIES

    if n_present == 2:
        person = rng.choice(NAMES)
        company = rng.choice(COMPANIES)
        present = [person, company]
        sentence = rng.choice(TEMPLATES_PC).format(p=person, c=company)
    else:
        p1, p2 = rng.sample(NAMES, 2)
        company = rng.choice(COMPANIES)
        present = [p1, p2, company]
        sentence = rng.choice(TEMPLATES_PPC).format(p1=p1, p2=p2, c=company)

    # Build known list: present entities + random others
    remaining = [e for e in all_entities if e not in present]
    rng.shuffle(remaining)
    n_others = min(n_list - len(present), len(remaining))
    known = present + remaining[:n_others]
    rng.shuffle(known)

    return {
        "inputs": {
            "sentence": sentence,
            "entities": known,
        },
        "expected": ", ".join(present),
        "check": {
            "type": "entity_match",
            "expected_found": present,
        },
    }
