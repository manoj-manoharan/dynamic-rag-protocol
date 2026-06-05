"""The fact contains negation. Model must parse what IS true, not what is denied.
Easy: "X is not Y but Z" (clear correction). Medium: "X is no longer Y" (state change).
Hard: "X serves as Y, not Z" with a distractor asking about Z.
Distinct from the negation test which asks "who does NOT work at X"."""

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

ROLES = ["CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
         "Head of Research", "Chief Scientist", "COO"]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    person = rng.choice(NAMES)
    company = rng.choice(COMPANIES)
    correct_role, wrong_role = rng.sample(ROLES, 2)

    if difficulty == "easy":
        # Clear correction: "not X but Y"
        fact = f"{person} is not the {wrong_role} but the {correct_role} of {company}."
        return {
            "inputs": {"facts": [fact], "question": f"What is {person}'s role at {company}?"},
            "expected": correct_role,
            "check": {"type": "regex", "pattern": re.escape(correct_role)},
        }

    if difficulty == "medium":
        # State change: "no longer X, now Y"
        fact = f"{person} is no longer {wrong_role} of {company} and now serves as {correct_role}."
        return {
            "inputs": {"facts": [fact], "question": f"What is {person}'s current role at {company}?"},
            "expected": correct_role,
            "check": {"type": "regex", "pattern": re.escape(correct_role)},
        }

    # hard: negation + distractor question that targets the negated part
    fact = f"{person} serves as {correct_role} of {company}, not {wrong_role}."
    return {
        "inputs": {"facts": [fact], "question": f"Is {person} the {wrong_role} of {company}?"},
        "expected": f"No, {person} is the {correct_role}",
        "check": {
            "type": "regex_all",
            "patterns": [
                r"\b(no|not)\b",
                re.escape(correct_role),
            ],
        },
    }
