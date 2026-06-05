"""Fact mentions both an old/wrong value and a corrected value. Model must pick the correct one.
Easy: explicit "revised from X to Y". Medium: "initially X, actually Y".
Hard: correction buried in a subordinate clause.
Tests whether the model picks the updated value, not the first number it sees."""

import random

PROJECTS = [
    "Project Alpha", "Project Beta", "Project Gamma", "Project Delta",
    "Project Epsilon", "Project Omega", "Project Sigma", "Project Theta",
]

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    project = rng.choice(PROJECTS)
    old_val = rng.randint(3, 7) * 100
    new_val = old_val + rng.choice([100, 150, 200, 250])
    company = rng.choice(COMPANIES)

    if difficulty == "easy":
        fact = f"BUDGET UPDATE: {project} budget revised from ${old_val}K to ${new_val}K."
        return {
            "inputs": {
                "facts": [fact],
                "question": f"What is the current budget of {project}?",
            },
            "expected": f"${new_val}K",
            "check": {"type": "regex", "pattern": str(new_val)},
        }

    if difficulty == "medium":
        fact = f"Initially estimated at ${old_val}K, {project}'s actual budget is ${new_val}K."
        return {
            "inputs": {
                "facts": [fact],
                "question": f"What is {project}'s actual budget?",
            },
            "expected": f"${new_val}K",
            "check": {"type": "regex", "pattern": str(new_val)},
        }

    # hard: correction in subordinate clause
    person = rng.choice(NAMES)
    templates = [
        f"{project}'s ${old_val}K budget, which was adjusted following the Q3 review, now stands at ${new_val}K.",
        f"Despite the original ${old_val}K allocation, {project} at {company} currently operates with a ${new_val}K budget after mid-year adjustments.",
        f"The {project} budget that {person} initially set at ${old_val}K has been corrected to ${new_val}K per the latest filing.",
    ]
    fact = rng.choice(templates)
    return {
        "inputs": {
            "facts": [fact],
            "question": f"What is {project}'s current budget?",
        },
        "expected": f"${new_val}K",
        "check": {"type": "regex", "pattern": str(new_val)},
    }
