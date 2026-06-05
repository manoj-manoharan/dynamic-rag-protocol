"""Facts use one phrasing, question uses a paraphrase of key terms.
Difficulty controls paraphrase distance: easy=minor synonym, medium=role description,
hard=structural rephrase.
Tests matching: can the model recognize the question refers to the same thing as the fact?"""

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

# (role_in_fact, easy_paraphrase, medium_paraphrase, hard_paraphrase)
ROLE_VARIANTS = [
    ("CEO", "Chief Executive Officer", "the person who runs", "the top leader of"),
    ("CTO", "Chief Technology Officer", "the head of technology at", "the person in charge of tech at"),
    ("CFO", "Chief Financial Officer", "the head of finance at", "the person managing money at"),
    ("VP of Engineering", "Vice President of Engineering", "the engineering leader at", "the person overseeing all engineers at"),
    ("VP of Sales", "Vice President of Sales", "the sales leader at", "the person responsible for revenue at"),
    ("Head of Research", "Research Director", "the person leading research at", "the one directing scientific work at"),
    ("Chief Scientist", "Lead Scientist", "the top scientist at", "the primary researcher at"),
    ("COO", "Chief Operating Officer", "the head of operations at", "the person running day-to-day operations at"),
]

FILLERS = [
    "CEO", "CTO", "CFO", "VP of Engineering", "VP of Sales",
    "Head of Research", "Chief Scientist", "COO",
]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)

    variant = rng.choice(ROLE_VARIANTS)
    role_in_fact = variant[0]
    paraphrase_idx = {"easy": 1, "medium": 2, "hard": 3}[difficulty]
    role_in_question = variant[paraphrase_idx]

    people = rng.sample(NAMES, 6)
    companies = rng.sample(COMPANIES, 6)
    target_person = people[0]
    target_company = companies[0]

    facts = [f"{target_person} serves as {role_in_fact} of {target_company}."]
    other_roles = [r for r in FILLERS if r != role_in_fact]
    for i in range(1, 6):
        facts.append(f"{people[i]} serves as {rng.choice(other_roles)} of {companies[i]}.")
    rng.shuffle(facts)

    # Question uses the paraphrase
    if paraphrase_idx <= 1:
        question = f"Who is the {role_in_question} of {target_company}?"
    else:
        question = f"Who is {role_in_question} {target_company}?"

    return {
        "inputs": {"facts": facts, "question": question},
        "expected": target_person,
        "check": {"type": "regex", "pattern": re.escape(target_person)},
    }
