"""Extract information about a specific person when similar names exist in context.
Difficulty controls confusion level: easy=no similar names, medium=shared surname,
hard=shared surname plus similar first names.
Tests resistance to name confusion, a real failure mode from Phase 2."""

import random
import re

# Groups of confusable names (shared surname or similar structure)
CONFUSABLE = [
    ["Dr. Wei Lin", "Dr. Amy Lin", "Dr. Jason Lin"],
    ["Rachel Torres", "Elena Torres", "Michael Torres"],
    ["Nina Patel", "Maya Patel", "Dr. Raj Patel"],
    ["Alice Chen", "Sarah Chen", "Olivia Chen"],
    ["Alex Rivera", "Carlos Rivera", "Pablo Rivera"],
]

# Unambiguous names (no overlapping parts)
DISTINCT = [
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto",
    "Jack Wilson", "Karen Singh", "Leo Fischer", "Tara Nguyen",
    "Quinn O'Brien", "Bob Martinez", "Eva Johansson", "Sam Thompson",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
    "Horizon Tech", "Meridian Data", "Forge Robotics", "Helios Cloud", "Nova Logic",
]

ROLES = [
    "CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
    "Head of Research", "Chief Scientist", "COO", "VP of Marketing", "Head of Product",
]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    if difficulty == "easy":
        # No similar names at all
        people = rng.sample(DISTINCT, 5)
        target = people[0]
        companies = rng.sample(COMPANIES, 5)
        roles = rng.sample(ROLES, 5)
        facts = [f"{people[i]} serves as {roles[i]} of {companies[i]}." for i in range(5)]
        rng.shuffle(facts)
        return {
            "inputs": {"facts": facts, "question": f"Who is the {roles[0]} of {companies[0]}?"},
            "expected": target,
            "check": {"type": "regex", "pattern": re.escape(target)},
        }

    if difficulty == "medium":
        # One confusable pair, ask about one
        group = rng.choice(CONFUSABLE)
        pair = rng.sample(group, 2)
        target = pair[0]
        distractor = pair[1]
        companies = rng.sample(COMPANIES, 5)
        roles = rng.sample(ROLES, 5)
        # Target and distractor get different companies and roles
        facts = [
            f"{target} serves as {roles[0]} of {companies[0]}.",
            f"{distractor} serves as {roles[1]} of {companies[1]}.",
        ]
        fillers = rng.sample(DISTINCT, 3)
        for i, p in enumerate(fillers):
            facts.append(f"{p} serves as {roles[i + 2]} of {companies[i + 2]}.")
        rng.shuffle(facts)
        return {
            "inputs": {"facts": facts, "question": f"Who is the {roles[0]} of {companies[0]}?"},
            "expected": target,
            "check": {"type": "regex", "pattern": re.escape(target)},
        }

    # hard: two confusable groups mixed together
    g1, g2 = rng.sample(CONFUSABLE, 2)
    confusables = rng.sample(g1, 2) + rng.sample(g2, 2)
    target = confusables[0]
    companies = rng.sample(COMPANIES, 8)
    roles = rng.sample(ROLES, 8)
    facts = [f"{confusables[i]} serves as {roles[i]} of {companies[i]}." for i in range(4)]
    fillers = rng.sample(DISTINCT, 4)
    for i, p in enumerate(fillers):
        facts.append(f"{p} serves as {roles[i + 4]} of {companies[i + 4]}.")
    rng.shuffle(facts)
    return {
        "inputs": {"facts": facts, "question": f"Who is the {roles[0]} of {companies[0]}?"},
        "expected": target,
        "check": {"type": "regex", "pattern": re.escape(target)},
    }
