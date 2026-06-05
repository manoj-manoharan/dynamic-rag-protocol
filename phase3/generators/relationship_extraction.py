"""Given a sentence, extract the key relationship as a structured triple.
Difficulty: easy=simple role statement, medium=compound sentence with 2 relationships,
hard=implicit relationship requiring inference.
Tests core ingestion: can the model produce structured output from natural language?"""

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

ROLES = ["CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales", "Head of Research"]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    if difficulty == "easy":
        # Simple: "X serves as ROLE of COMPANY."
        person = rng.choice(NAMES)
        company = rng.choice(COMPANIES)
        role = rng.choice(ROLES)
        sentence = f"{person} serves as {role} of {company}."

        return {
            "inputs": {
                "facts": [sentence],
                "question": (
                    "Extract the relationship in this sentence. "
                    "State the person, their role, and the organization."
                ),
            },
            "expected": f"{person}, {role}, {company}",
            "check": {
                "type": "regex_all",
                "patterns": [re.escape(person), re.escape(company), re.escape(role)],
            },
        }

    if difficulty == "medium":
        # Compound: "X, who founded Y, serves as its Chief Scientist."
        person = rng.choice(NAMES)
        company = rng.choice(COMPANIES)
        sentence = f"{person}, who founded {company}, serves as its Chief Scientist."

        return {
            "inputs": {
                "facts": [sentence],
                "question": (
                    "Extract ALL relationships in this sentence. "
                    "For each, state the person, relationship, and organization."
                ),
            },
            "expected": f"{person} founded {company}; {person} is Chief Scientist of {company}",
            "check": {
                "type": "regex_all",
                "patterns": [re.escape(person), re.escape(company), r"found", r"[Cc]hief [Ss]cientist"],
            },
        }

    # hard: implicit relationship
    person = rng.choice(NAMES)
    company1 = rng.choice(COMPANIES)
    company2 = rng.choice([c for c in COMPANIES if c != company1])
    role = rng.choice(ROLES)
    sentence = f"{person} left {company1} to join {company2} as {role}."

    return {
        "inputs": {
            "facts": [sentence],
            "question": (
                "Extract ALL relationships in this sentence, including implied ones. "
                "State each as: person, relationship, organization."
            ),
        },
        "expected": f"{person} departed {company1}; {person} is {role} of {company2}",
        "check": {
            "type": "regex_all",
            "patterns": [
                re.escape(person), re.escape(company1), re.escape(company2),
                re.escape(role), r"left|depart|former|no longer",
            ],
        },
    }
