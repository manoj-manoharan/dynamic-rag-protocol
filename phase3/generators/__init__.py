"""
Test registry. Add new tests by writing a generator module and registering it here.

Generator contract:
    def generate(difficulty: str, trial: int, seed: int) -> dict

    Must return:
        "inputs": dict      # facts+question (reader) or sentence+entities (ingester)
        "expected": str      # ground truth
        "check": dict        # {"type": "regex", "pattern": "..."} or
                             # {"type": "regex_all", "patterns": [...]} or
                             # {"type": "entity_match", "expected_found": [...]}

    Must be deterministic given (difficulty, trial, seed).
"""

from generators.simple_extraction import generate as simple_extraction_gen
from generators.distractor_density import generate as distractor_density_gen
from generators.negation import generate as negation_gen
from generators.entity_extraction_known import generate as entity_extraction_gen

TESTS = {
    "simple_extraction": {
        "description": "Given N person-role-company facts, extract who holds a specific role",
        "difficulties": ["easy", "medium", "hard"],
        "generator": simple_extraction_gen,
        "trials": 20,
    },
    "distractor_density": {
        "description": "Extract a role-holder when many others at the same company are distractors",
        "difficulties": ["easy", "medium", "hard"],
        "generator": distractor_density_gen,
        "trials": 20,
    },
    "negation": {
        "description": "Identify which person does NOT work at a target company",
        "difficulties": ["easy", "medium", "hard"],
        "generator": negation_gen,
        "trials": 20,
    },
    "entity_extraction_known": {
        "description": "Given a sentence and known entity list, identify which appear",
        "difficulties": ["easy", "medium", "hard"],
        "generator": entity_extraction_gen,
        "trials": 20,
    },
}
