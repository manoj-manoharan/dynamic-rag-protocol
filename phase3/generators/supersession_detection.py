"""Given existing facts about an entity and a new fact, determine if the new fact
supersedes (replaces) an existing fact or is additive (new information).
Difficulty: easy=explicit markers, medium=same property no marker, hard=reversal.
Tests a core ingestion operation: knowing when to update vs append."""

import random

NAMES = [
    "Alice Chen", "Bob Martinez", "Carol Smith", "David Kim", "Eva Johansson",
    "Frank Okafor", "Grace Liu", "Henry Brown", "Iris Yamamoto", "Jack Wilson",
]

COMPANIES = [
    "Nexus Corp", "Vertex Labs", "Omega Systems", "Pinnacle AI", "Atlas Dynamics",
]

PROJECTS = [
    "Project Alpha", "Project Beta", "Project Gamma", "Project Delta",
]

ROLES = ["CEO", "CTO", "CFO", "VP of Engineering", "Head of Research"]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    if difficulty == "easy":
        # Explicit marker: "BUDGET UPDATE:" or "PROJECT UPDATE:"
        project = rng.choice(PROJECTS)
        company = rng.choice(COMPANIES)
        old_budget = rng.randint(3, 8) * 100
        new_budget = old_budget + rng.choice([-100, 100, 150, 200])
        person = rng.choice(NAMES)

        existing = [
            f"{project} at {company} has an initial budget of ${old_budget}K.",
            f"{person} is the lead of {project}.",
            f"{company} launched {project} in January 2024.",
        ]
        new_fact = f"BUDGET UPDATE: {project} budget revised to ${new_budget}K."
        expected = "supersedes"
        pattern = r"supersede|replace|update|overwrite|fact.?1|first fact"

    elif difficulty == "medium":
        # Same property, different value, no explicit marker
        project = rng.choice(PROJECTS)
        company = rng.choice(COMPANIES)
        old_budget = rng.randint(3, 8) * 100
        new_budget = old_budget + rng.choice([-100, 100, 150])
        person = rng.choice(NAMES)

        existing = [
            f"{project} at {company} has a budget of ${old_budget}K.",
            f"{person} leads {project}.",
            f"{company} started {project} in Q1 2024.",
        ]
        new_fact = f"In March 2024, {project} budget was set to ${new_budget}K."
        expected = "supersedes"
        pattern = r"supersede|replace|update|overwrite|fact.?1|first fact"

    else:  # hard
        # Additive fact that LOOKS like it could be supersession
        project = rng.choice(PROJECTS)
        company = rng.choice(COMPANIES)
        budget = rng.randint(3, 8) * 100
        person1 = rng.choice(NAMES)
        person2 = rng.choice([n for n in NAMES if n != person1])

        existing = [
            f"{project} at {company} has a budget of ${budget}K.",
            f"{person1} leads {project}.",
            f"{company} launched {project} in January 2024.",
        ]
        # New team member, not a replacement
        new_fact = f"{person2} joined {project} as a senior contributor."
        expected = "additive"
        pattern = r"additive|additional|new information|does not replace|supplement|new fact"

    existing_text = "\n".join(f"{i + 1}. {f}" for i, f in enumerate(existing))

    return {
        "inputs": {
            "facts": [
                f"EXISTING FACTS:\n{existing_text}",
                f"NEW FACT: {new_fact}",
            ],
            "question": (
                "Does the NEW FACT supersede (replace) any of the existing facts, "
                "or is it additive (new information)? "
                "Answer: SUPERSEDES [which fact] or ADDITIVE."
            ),
        },
        "expected": expected,
        "check": {"type": "regex", "pattern": pattern},
    }
