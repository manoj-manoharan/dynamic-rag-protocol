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
from generators.surface_form import generate as surface_form_gen
from generators.question_form import generate as question_form_gen
from generators.multi_info_extraction import generate as multi_info_extraction_gen
from generators.negation_in_fact import generate as negation_in_fact_gen
from generators.numeric_precision import generate as numeric_precision_gen
from generators.temporal_precision import generate as temporal_precision_gen
from generators.domain_language import generate as domain_language_gen
from generators.minimal_pair import generate as minimal_pair_gen
from generators.instruction_adherence import generate as instruction_adherence_gen
from generators.embedded_correction import generate as embedded_correction_gen
from generators.conditional_fact import generate as conditional_fact_gen
from generators.quoted_attribution import generate as quoted_attribution_gen

TESTS = {
    # ── Locate ──
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
    "position_bias": {
        "description": "Same task with answer placed at first/middle/last position in context",
        "difficulties": ["easy", "medium", "hard"],
        "generator": position_bias_gen,
        "trials": 20,
    },

    # ── Match ──
    "paraphrase": {
        "description": "Question uses different vocabulary than the facts for the same concept",
        "difficulties": ["easy", "medium", "hard"],
        "generator": paraphrase_gen,
        "trials": 20,
    },
    "similar_names": {
        "description": "Extract info when confusable entity names (shared surname) are present",
        "difficulties": ["easy", "medium", "hard"],
        "generator": similar_names_gen,
        "trials": 20,
    },

    # ── Reason ──
    "negation": {
        "description": "Identify which person does NOT work at a target company",
        "difficulties": ["easy", "medium", "hard"],
        "generator": negation_gen,
        "trials": 20,
    },
    "absence": {
        "description": "Asked-about property doesn't exist in facts; correct answer is no",
        "difficulties": ["easy", "medium", "hard"],
        "generator": absence_gen,
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
    "transitivity": {
        "description": "Follow a 2-hop chain (A married to B, B works at C) from co-located facts",
        "difficulties": ["easy", "medium", "hard"],
        "generator": transitivity_gen,
        "trials": 20,
    },

    # ── Ingestion ──
    "entity_extraction_known": {
        "description": "Given a sentence and known entity list, identify which appear",
        "difficulties": ["easy", "medium", "hard"],
        "generator": entity_extraction_gen,
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

    # ── Load-bearing: single-fact comprehension ──
    "surface_form": {
        "description": "Same fact in different syntactic structures (active/passive/dense/informal)",
        "difficulties": ["easy", "medium", "hard"],
        "generator": surface_form_gen,
        "trials": 20,
    },
    "question_form": {
        "description": "Same fact, question phrased differently (direct/indirect/circumlocuted)",
        "difficulties": ["easy", "medium", "hard"],
        "generator": question_form_gen,
        "trials": 20,
    },
    "multi_info_extraction": {
        "description": "One fact has 3-4 data points, ask about a specific one",
        "difficulties": ["easy", "medium", "hard"],
        "generator": multi_info_extraction_gen,
        "trials": 20,
    },
    "negation_in_fact": {
        "description": "Fact itself contains negation; model must parse what IS true",
        "difficulties": ["easy", "medium", "hard"],
        "generator": negation_in_fact_gen,
        "trials": 20,
    },
    "numeric_precision": {
        "description": "Extract the correct number when multiple numbers are present in the fact",
        "difficulties": ["easy", "medium", "hard"],
        "generator": numeric_precision_gen,
        "trials": 20,
    },
    "temporal_precision": {
        "description": "Extract the correct date when multiple dates are present in the fact",
        "difficulties": ["easy", "medium", "hard"],
        "generator": temporal_precision_gen,
        "trials": 20,
    },
    "domain_language": {
        "description": "Same fact in domain-specific register (corporate/legal/CRM/technical)",
        "difficulties": ["easy", "medium", "hard"],
        "generator": domain_language_gen,
        "trials": 20,
    },
    "minimal_pair": {
        "description": "Exactly two similar facts, must discriminate the right one",
        "difficulties": ["easy", "medium", "hard"],
        "generator": minimal_pair_gen,
        "trials": 20,
    },
    "instruction_adherence": {
        "description": "Fact contradicts world knowledge; model must follow the fact",
        "difficulties": ["easy", "medium", "hard"],
        "generator": instruction_adherence_gen,
        "trials": 20,
    },
    "embedded_correction": {
        "description": "Fact contains both old and corrected values; pick the correction",
        "difficulties": ["easy", "medium", "hard"],
        "generator": embedded_correction_gen,
        "trials": 20,
    },
    "conditional_fact": {
        "description": "Distinguish asserted facts from hedged/conditional statements",
        "difficulties": ["easy", "medium", "hard"],
        "generator": conditional_fact_gen,
        "trials": 20,
    },
    "quoted_attribution": {
        "description": "Distinguish attributed claims from asserted facts",
        "difficulties": ["easy", "medium", "hard"],
        "generator": quoted_attribution_gen,
        "trials": 20,
    },
}
