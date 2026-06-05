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
from generators.temporal_ordering import generate as temporal_ordering_gen
from generators.comparison import generate as comparison_gen
from generators.counting import generate as counting_gen
from generators.similar_names import generate as similar_names_gen
from generators.position_bias import generate as position_bias_gen
from generators.paraphrase import generate as paraphrase_gen
from generators.absence import generate as absence_gen
from generators.transitivity import generate as transitivity_gen
from generators.supersession_detection import generate as supersession_detection_gen
from generators.relationship_extraction import generate as relationship_extraction_gen

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
    "temporal_ordering": {
        "description": "Pick the latest value from N chronological updates to the same property",
        "difficulties": ["easy", "medium", "hard"],
        "generator": temporal_ordering_gen,
        "trials": 20,
    },
    "comparison": {
        "description": "Identify which item has the largest value among N items",
        "difficulties": ["easy", "medium", "hard"],
        "generator": comparison_gen,
        "trials": 20,
    },
    "counting": {
        "description": "Count how many entities match a criterion",
        "difficulties": ["easy", "medium", "hard"],
        "generator": counting_gen,
        "trials": 20,
    },
    "similar_names": {
        "description": "Extract info when confusable entity names (shared surname) are present",
        "difficulties": ["easy", "medium", "hard"],
        "generator": similar_names_gen,
        "trials": 20,
    },
    "position_bias": {
        "description": "Same task with answer placed at first/middle/last position in context",
        "difficulties": ["easy", "medium", "hard"],
        "generator": position_bias_gen,
        "trials": 20,
    },
    "paraphrase": {
        "description": "Question uses different vocabulary than the facts for the same concept",
        "difficulties": ["easy", "medium", "hard"],
        "generator": paraphrase_gen,
        "trials": 20,
    },
    "absence": {
        "description": "Asked-about property doesn't exist in facts; correct answer is no",
        "difficulties": ["easy", "medium", "hard"],
        "generator": absence_gen,
        "trials": 20,
    },
    "transitivity": {
        "description": "Follow a 2-hop chain (A married to B, B works at C) from co-located facts",
        "difficulties": ["easy", "medium", "hard"],
        "generator": transitivity_gen,
        "trials": 20,
    },
    "supersession_detection": {
        "description": "Determine if a new fact replaces an existing one or is additive",
        "difficulties": ["easy", "medium", "hard"],
        "generator": supersession_detection_gen,
        "trials": 20,
    },
    "relationship_extraction": {
        "description": "Extract structured relationship triples from a sentence",
        "difficulties": ["easy", "medium", "hard"],
        "generator": relationship_extraction_gen,
        "trials": 20,
    },
}
