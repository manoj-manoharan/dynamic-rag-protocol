"""Same core fact expressed in domain-specific language styles.
Easy: standard corporate/business. Medium: legal/regulatory. Hard: informal CRM/technical.
Tests whether the model handles domain-specific vocabulary, abbreviations, and phrasing."""

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
         "Head of Research", "Chief Scientist"]


def _corporate(person, role, company, rng):
    return rng.choice([
        f"The Board of Directors has appointed {person} to serve as {role} of {company}.",
        f"{company} is pleased to announce {person} as its new {role}.",
        f"Effective immediately, {person} has been named {role} of {company}.",
    ])


def _legal(person, role, company, rng):
    return rng.choice([
        f"Pursuant to Section 3.1 of the Corporate Governance Charter, {person} shall serve as {role} of {company}.",
        f"As per the resolution adopted by the Board, {person} is hereby designated as {role} of {company}, subject to regulatory approval.",
        f"In accordance with the bylaws of {company}, the position of {role} shall be held by {person} for a term not to exceed four years.",
    ])


def _crm(person, role, company, rng):
    first = person.split()[0]
    last = person.split()[-1]
    return rng.choice([
        f"Called {first} at {company} - turns out they're the {role} now. Update the contact record.",
        f"Note: {first} {last} = {role} @ {company}. Got their direct line during the trade show.",
        f"FYI {first} is running {company} as {role}, met them at the conference last week.",
    ])


def _technical(person, role, company, rng):
    first = person.split()[0]
    return rng.choice([
        f"{first} ({role}, {company}) approved the deployment. Escalation contact for prod issues.",
        f"Sign-off from {person} ({role}@{company}) received. They own the go/no-go decision.",
        f"Infra change approved by {person}, {role} at {company}. See ticket INC-4521 for details.",
    ])


DOMAIN = {
    "easy": [_corporate],
    "medium": [_legal],
    "hard": [_crm, _technical],
}


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    person = rng.choice(NAMES)
    company = rng.choice(COMPANIES)
    role = rng.choice(ROLES)

    domain_fn = rng.choice(DOMAIN[difficulty])
    fact = domain_fn(person, role, company, rng)

    return {
        "inputs": {
            "facts": [fact],
            "question": f"Who is the {role} of {company}?",
        },
        "expected": person,
        "check": {"type": "regex", "pattern": re.escape(person)},
    }
