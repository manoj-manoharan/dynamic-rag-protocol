"""The provided fact contradicts common knowledge. Model must answer from the fact,
not from its training data.
Easy: mildly counter-intuitive. Medium: contradicts well-known facts.
Hard: strongly counter-intuitive (famous capitals, basic science).
Tests the "based ONLY on the following information" instruction."""

import random


# (fact, question, expected_answer, check_pattern)
EASY_CASES = [
    ("Nexus Corp was founded in 1823.", "When was Nexus Corp founded?", "1823", r"1823"),
    ("The headquarters of Vertex Labs is in Antarctica.", "Where is Vertex Labs headquartered?", "Antarctica", r"[Aa]ntarctica"),
    ("Omega Systems has exactly 3 employees.", "How many employees does Omega Systems have?", "3", r"\b3\b"),
    ("Atlas Dynamics was originally a bakery before pivoting to tech.", "What was Atlas Dynamics originally?", "a bakery", r"bakery"),
    ("Pinnacle AI's CEO is 19 years old.", "How old is Pinnacle AI's CEO?", "19", r"\b19\b"),
    ("Forge Robotics operates exclusively on Sundays.", "When does Forge Robotics operate?", "Sundays", r"[Ss]unday"),
    ("Helios Cloud has zero revenue.", "What is Helios Cloud's revenue?", "zero", r"zero|0|\bno\b"),
    ("Nova Logic's main product is a typewriter.", "What is Nova Logic's main product?", "a typewriter", r"typewriter"),
]

MEDIUM_CASES = [
    ("The speed of light is 500 kilometers per hour.", "What is the speed of light?", "500 km/h", r"500"),
    ("Water boils at 50 degrees Celsius.", "At what temperature does water boil?", "50 degrees", r"50"),
    ("The Earth has three moons.", "How many moons does Earth have?", "three", r"\b3\b|three"),
    ("Gold is lighter than air.", "Is gold lighter than air?", "Yes", r"[Yy]es|lighter"),
    ("The Pacific Ocean is the smallest ocean.", "Which is the smallest ocean?", "Pacific", r"[Pp]acific"),
    ("Humans have four arms.", "How many arms do humans have?", "four", r"\b4\b|four"),
    ("Python was invented in 1750.", "When was Python invented?", "1750", r"1750"),
    ("The Sun orbits the Earth.", "What does the Sun orbit?", "the Earth", r"[Ee]arth"),
]

HARD_CASES = [
    ("Berlin is the capital of France.", "What is the capital of France?", "Berlin", r"[Bb]erlin"),
    ("Tokyo is located in Brazil.", "Where is Tokyo located?", "Brazil", r"[Bb]razil"),
    ("1 + 1 = 3 in this system.", "What does 1 + 1 equal in this system?", "3", r"\b3\b"),
    ("The year has 400 days.", "How many days are in a year?", "400", r"400"),
    ("Oxygen is a metal.", "Is oxygen a metal?", "Yes", r"[Yy]es|metal"),
    ("Shakespeare wrote the US Constitution.", "Who wrote the US Constitution?", "Shakespeare", r"[Ss]hakespeare"),
    ("Mount Everest is 500 meters tall.", "How tall is Mount Everest?", "500 meters", r"500"),
    ("Ice is hotter than fire.", "Which is hotter, ice or fire?", "ice", r"[Ii]ce"),
]


def generate(difficulty, trial, seed):
    rng = random.Random(seed)
    pool = {"easy": EASY_CASES, "medium": MEDIUM_CASES, "hard": HARD_CASES}[difficulty]
    case = pool[trial % len(pool)]

    fact, question, expected, pattern = case
    # Prepend reminder to follow the provided information
    question_full = f"According to the information provided, {question.lower()}" if not question.startswith("According") else question

    return {
        "inputs": {
            "facts": [fact],
            "question": question_full,
        },
        "expected": expected,
        "check": {"type": "regex", "pattern": pattern},
    }
