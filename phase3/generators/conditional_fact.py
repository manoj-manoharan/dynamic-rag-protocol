"""Fact is either asserted, hedged, or conditional. Model must respond appropriately.
Easy: clear assertion (should extract answer). Medium: hedged/attributed (should note uncertainty).
Hard: conditional (should say uncertain/conditional).
Tests epistemic status recognition: the model must know what it can and can't assert."""

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

ROLES = ["CEO", "CTO", "CFO", "VP of Engineering", "Head of Research"]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    person = rng.choice(NAMES)
    company = rng.choice(COMPANIES)
    role = rng.choice(ROLES)

    if difficulty == "easy":
        # Clear assertion, answer should be the person
        templates = [
            f"{person} serves as {role} of {company}.",
            f"{person} is the current {role} of {company}.",
            f"{company} confirmed {person} as {role}.",
        ]
        fact = rng.choice(templates)
        return {
            "inputs": {"facts": [fact], "question": f"Who is the {role} of {company}?"},
            "expected": person,
            "check": {"type": "regex", "pattern": re.escape(person)},
        }

    if difficulty == "medium":
        # Hedged: reportedly, expected, rumored
        templates = [
            f"{person} is reportedly serving as {role} of {company}.",
            f"{person} is expected to be named {role} of {company}.",
            f"Sources indicate that {person} may be the new {role} of {company}.",
            f"According to unconfirmed reports, {person} has been appointed {role} of {company}.",
        ]
        fact = rng.choice(templates)
        # Model should give the name but note the uncertainty
        return {
            "inputs": {
                "facts": [fact],
                "question": f"Who is the {role} of {company}? Is this confirmed?",
            },
            "expected": f"{person} (unconfirmed)",
            "check": {
                "type": "regex_all",
                "patterns": [
                    re.escape(person),
                    r"report|expect|unconfirm|may|rumor|source|not confirm|indicat|uncertain",
                ],
            },
        }

    # hard: clearly conditional, answer should be uncertain
    templates = [
        f"If the board approves, {person} will become {role} of {company}.",
        f"{person} will serve as {role} of {company} only if the merger is finalized.",
        f"Pending regulatory approval, {person} is slated to become {role} of {company}.",
        f"Should the acquisition close, {person} would assume the {role} position at {company}.",
    ]
    fact = rng.choice(templates)
    return {
        "inputs": {
            "facts": [fact],
            "question": f"Who is currently the {role} of {company}?",
        },
        "expected": "uncertain/conditional",
        "check": {
            "type": "regex",
            "pattern": r"uncertain|conditional|not yet|pending|if|would|cannot determine|not confirmed|will .+ if|no current",
        },
    }
