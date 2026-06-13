#!/usr/bin/env python3
"""
Phase 2: Memory + Orchestration with Local Small Models
Runs the same experiment as Phase 1 but uses Ollama for the model.
Compare results against Sonnet baseline (12/13 at 200 facts).
"""

import argparse
import json
import re
import sys
import time
from collections import defaultdict
from typing import Optional
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════════════════
# CORPUS
# ═══════════════════════════════════════════════════════════════

COMPANIES = [
    "NexGen Industries","Orion Corp","Quantum Labs","Vertex Solutions",
    "Pinnacle Tech","Meridian Systems","Atlas Digital","Forge Analytics",
    "Helios AI","Nova Robotics","Prism Networks","Zenith Cloud",
    "Apex Biotech","Lunar Dynamics","Titan Software"
]

def F(id, text, ents, scale):
    return {"id": f"f{id}", "text": text, "entities": ents, "scale": scale}

CORE = [
    F(1,"Sarah Chen serves as CEO of NexGen Industries.",["Sarah Chen","NexGen Industries"],0),
    F(2,"James Porter is VP of Engineering at Orion Corp.",["James Porter","Orion Corp"],0),
    F(3,"Dr. Wei Lin founded Quantum Labs and serves as its Chief Scientist.",["Dr. Wei Lin","Quantum Labs"],0),
    F(4,"Dr. Amy Lin serves as CTO of Helios AI.",["Dr. Amy Lin","Helios AI"],0),
    F(5,"Marcus Cole is CTO of Pinnacle Tech.",["Marcus Cole","Pinnacle Tech"],0),
    F(6,"David Park is CEO of Meridian Systems.",["David Park","Meridian Systems"],0),
    F(7,"Lisa Monroe is CEO of Atlas Digital.",["Lisa Monroe","Atlas Digital"],0),
    F(8,"Tom Monroe serves on the board of directors at NexGen Industries.",["Tom Monroe","NexGen Industries"],0),
    F(9,"Rachel Torres is VP of Sales at Vertex Solutions.",["Rachel Torres","Vertex Solutions"],0),
    F(10,"Elena Torres is a lead engineer at Prism Networks.",["Elena Torres","Prism Networks"],0),
    F(11,"Robert Kim founded Forge Analytics.",["Robert Kim","Forge Analytics"],0),
    F(12,"Angela Wu is CEO of Titan Software.",["Angela Wu","Titan Software"],0),
    F(13,"Dr. Raj Patel serves as Chief Scientist at Apex Biotech.",["Dr. Raj Patel","Apex Biotech"],0),
    F(14,"Nina Patel is CTO of Nova Robotics.",["Nina Patel","Nova Robotics"],0),
    F(15,"Yuki Tanaka is VP of Product at Helios AI.",["Yuki Tanaka","Helios AI"],0),
    F(16,"Carlos Rivera is CEO of Prism Networks.",["Carlos Rivera","Prism Networks"],0),
    F(17,"Sophie Zhang works as an engineer at Quantum Labs.",["Sophie Zhang","Quantum Labs"],0),
    F(18,"Sarah Chen is married to James Porter.",["Sarah Chen","James Porter"],0),
    F(19,"Dr. Wei Lin and Dr. Amy Lin are siblings who grew up in Shanghai.",["Dr. Wei Lin","Dr. Amy Lin"],0),
    F(20,"Rachel Torres and Elena Torres are sisters.",["Rachel Torres","Elena Torres"],0),
    F(21,"Orion Corp completed its acquisition of Quantum Labs in March 2024.",["Orion Corp","Quantum Labs"],0),
    F(22,"Prism Networks was acquired by Zenith Cloud in January 2024.",["Prism Networks","Zenith Cloud"],0),
    F(23,"NexGen Industries announced a strategic partnership with Orion Corp in May 2024.",["NexGen Industries","Orion Corp"],0),
    F(24,"NexGen Industries developed NexOS, a next-generation operating system.",["NexGen Industries"],0),
    F(25,"Orion Corp's flagship product is OrionDB, a distributed database.",["Orion Corp"],0),
    F(26,"Project Phoenix at NexGen Industries has an initial budget of $500K.",["Project Phoenix","NexGen Industries"],0),
    F(27,"Project Titan at Orion Corp has an initial budget of $300K.",["Project Titan","Orion Corp"],0),
    F(28,"Kevin Wright serves as CFO of NexGen Industries.",["Kevin Wright","NexGen Industries"],1),
    F(29,"Maria Lopez is VP of Marketing at Orion Corp.",["Maria Lopez","Orion Corp"],1),
    F(30,"Hassan Ali is Senior Architect at Zenith Cloud.",["Hassan Ali","Zenith Cloud"],1),
    F(31,"Irene Volkov is Lead Data Scientist at Meridian Systems.",["Irene Volkov","Meridian Systems"],1),
    F(32,"Emma Richardson is Head of Sales at Zenith Cloud.",["Emma Richardson","Zenith Cloud"],1),
    F(33,"Alex Rivera is Product Manager at Atlas Digital.",["Alex Rivera","Atlas Digital"],1),
    F(34,"Olivia Chen is Junior Developer at Forge Analytics.",["Olivia Chen","Forge Analytics"],1),
    F(35,"Ryan Adams is Security Researcher at Prism Networks.",["Ryan Adams","Prism Networks"],1),
    F(36,"Marcus Cole and David Park were college roommates at MIT.",["Marcus Cole","David Park"],1),
    F(37,"Lisa Monroe is married to Tom Monroe.",["Lisa Monroe","Tom Monroe"],1),
    F(38,"Nina Patel and Yuki Tanaka were colleagues at Stanford AI Lab before their current roles.",["Nina Patel","Yuki Tanaka"],1),
    F(39,"Carlos Rivera has been a professional mentor to Sophie Zhang for several years.",["Carlos Rivera","Sophie Zhang"],1),
    F(40,"Titan Software acquired Forge Analytics in June 2024.",["Titan Software","Forge Analytics"],1),
    F(41,"Meridian Systems entered a partnership with Atlas Digital in February 2024.",["Meridian Systems","Atlas Digital"],1),
    F(42,"Helios AI signed a partnership with Lunar Dynamics for autonomous navigation in April 2024.",["Helios AI","Lunar Dynamics"],1),
    F(43,"Pinnacle Tech offers PinnacleCloud, a cloud infrastructure platform.",["Pinnacle Tech"],1),
    F(44,"Helios AI's flagship product is AutoPilot, a self-driving system.",["Helios AI"],1),
    F(45,"Atlas Digital's main product is AdPulse, a marketing analytics platform.",["Atlas Digital"],1),
    F(46,"Zenith Cloud provides ZenithFlow, a workflow automation engine.",["Zenith Cloud"],1),
    F(47,"BUDGET UPDATE: Project Phoenix budget revised to $620K.",["Project Phoenix","NexGen Industries"],1),
    F(48,"BUDGET UPDATE: Project Titan budget increased to $450K.",["Project Titan","Orion Corp"],1),
    F(49,"Project Aurora at Pinnacle Tech has an initial budget of $800K.",["Project Aurora","Pinnacle Tech"],1),
    F(50,"Kevin Wright was appointed as initial lead of Project Phoenix.",["Kevin Wright","Project Phoenix"],1),
    F(51,"PROJECT UPDATE: Sandra Lee replaced Kevin Wright as lead of Project Phoenix.",["Sandra Lee","Kevin Wright","Project Phoenix"],1),
    F(52,"Dr. Leila Hoffman is VP of Research at Apex Biotech.",["Dr. Leila Hoffman","Apex Biotech"],2),
    F(53,"Chris Nakamura is Operations Manager at Nova Robotics.",["Chris Nakamura","Nova Robotics"],2),
    F(54,"Priya Sharma is Head of Engineering at Lunar Dynamics.",["Priya Sharma","Lunar Dynamics"],2),
    F(55,"Michael Torres is an investor and board member at Pinnacle Tech.",["Michael Torres","Pinnacle Tech"],2),
    F(56,"Sandra Lee is a senior project lead at NexGen Industries.",["Sandra Lee","NexGen Industries"],2),
    F(57,"Derek Huang is Head of AI at Titan Software.",["Derek Huang","Titan Software"],2),
    F(58,"Fatima Al-Rashid is CTO of Zenith Cloud.",["Fatima Al-Rashid","Zenith Cloud"],2),
    F(59,"Pablo Mendez is VP of Business Development at Lunar Dynamics.",["Pablo Mendez","Lunar Dynamics"],2),
    F(60,"Laura Kim is an intern at Helios AI.",["Laura Kim","Helios AI"],2),
    F(61,"Jonathan Blake serves as CTO of Vertex Solutions.",["Jonathan Blake","Vertex Solutions"],2),
    F(62,"Angela Wu is married to Dr. Raj Patel.",["Angela Wu","Dr. Raj Patel"],2),
    F(63,"Michael Torres is the brother of Rachel Torres and Elena Torres.",["Michael Torres","Rachel Torres","Elena Torres"],2),
    F(64,"Laura Kim is the daughter of Robert Kim.",["Laura Kim","Robert Kim"],2),
    F(65,"Sandra Lee previously interned under Marcus Cole.",["Sandra Lee","Marcus Cole"],2),
    F(66,"Pinnacle Tech made a strategic investment in Nova Robotics in July 2024.",["Pinnacle Tech","Nova Robotics"],2),
    F(67,"Apex Biotech licensed AI technology from Helios AI in August 2024.",["Apex Biotech","Helios AI"],2),
    F(68,"NexGen Industries opened a new R&D center in Austin in September 2024.",["NexGen Industries"],2),
    F(69,"Vertex Solutions was contracted to consult for Titan Software in October 2024.",["Vertex Solutions","Titan Software"],2),
    F(70,"NexGen Industries released NexAI, an AI assistant with a GraphQL API.",["NexGen Industries"],2),
    F(71,"Nova Robotics manufactures RoboAssist, an industrial automation robot.",["Nova Robotics"],2),
    F(72,"Apex Biotech created GenomAI, an AI-powered drug discovery platform.",["Apex Biotech"],2),
    F(73,"Titan Software offers TitanERP, an enterprise resource planning system.",["Titan Software"],2),
    F(74,"Forge Analytics built InsightEngine, a real-time analytics tool.",["Forge Analytics"],2),
    F(75,"BUDGET UPDATE: Project Phoenix budget further adjusted to $580K.",["Project Phoenix","NexGen Industries"],2),
    F(76,"BUDGET UPDATE: Project Aurora budget reduced to $650K.",["Project Aurora","Pinnacle Tech"],2),
    F(77,"BUDGET UPDATE: Project Aurora budget revised again to $720K.",["Project Aurora","Pinnacle Tech"],2),
    F(78,"Project Nexus at Zenith Cloud has initial budget of $400K.",["Project Nexus","Zenith Cloud"],2),
    F(79,"BUDGET UPDATE: Project Nexus budget increased to $520K.",["Project Nexus","Zenith Cloud"],2),
    F(80,"PROJECT UPDATE: Kevin Wright reinstated as lead of Project Phoenix, replacing Sandra Lee.",["Kevin Wright","Sandra Lee","Project Phoenix"],2),
]

NOISE_TEMPLATES = [
    "{} recently completed headquarters renovation.","{}'s annual retreat is scheduled for next month.",
    "{} updated their employee benefits package.","{}'s cafeteria now offers expanded menu options.",
    "{} celebrated its founding anniversary.","{} installed new printers on every floor.",
    "{} donated to local STEM education programs.","{}'s parking structure is under maintenance.",
    "{} announced a new wellness program.","{}'s lobby was redecorated with modern art.",
    "{} implemented a hybrid work policy.","{} conducted fire drills last Wednesday.",
    "{} upgraded their internal communication tools.","{}'s IT migrated to a new ticketing system.",
    "{} hosted an industry networking event.","{} ordered ergonomic furniture for all staff.",
    "{} started a company book club.","{}'s holiday party will be at the Grand Hotel.",
    "{} launched an internal Q3 hackathon.","{}'s security badges are being upgraded.",
    "{} opened a satellite office in Portland.","{} was featured in a tech magazine.",
    "{}'s engineering blog published its 100th post.","{} expanded the summer internship program.",
    "{} distributed new monitors to all departments.","{} won an award for workplace culture.",
    "{}'s campus added a walking trail.","{} held a town hall about company direction.",
    "{} offers free coding workshops on Fridays.","{} upgraded conference room booking systems.",
    "{} launched a sustainability initiative.","{}'s gym added new fitness equipment.",
    "{} introduced pet-friendly office hours.","{} began offering commuter transit benefits.",
    "{} hosted a charity 5K run for employees.","{} started a mentorship matching program.",
    "{} renovated all meeting rooms with smart boards.","{}'s rooftop garden opened for employee use.",
    "{} switched to fully renewable energy.","{} set up a new employee assistance hotline.",
]

def gen_noise(count, scale, start_id):
    facts = []
    for i in range(count):
        co = COMPANIES[(i * 7 + scale * 3) % len(COMPANIES)]
        tmpl = NOISE_TEMPLATES[(i + scale * 13) % len(NOISE_TEMPLATES)]
        facts.append({"id": f"n{start_id+i}", "text": tmpl.replace("{}", co), "entities": [co], "scale": scale, "noise": True})
    return facts

def get_corpus(scale):
    core = [f for f in CORE if f["scale"] <= scale]
    targets = [60, 120, 200]
    all_noise = []
    if scale >= 0:
        all_noise += gen_noise(targets[0] - len([f for f in CORE if f["scale"] <= 0]), 0, 100)
    if scale >= 1:
        all_noise += gen_noise(targets[1] - len([f for f in CORE if f["scale"] <= 1]) - len(all_noise), 1, 200)
    if scale >= 2:
        all_noise += gen_noise(targets[2] - len(core) - len(all_noise), 2, 300)
    combined = core + [n for n in all_noise if n["scale"] <= scale]
    def sort_key(f):
        nums = re.sub(r'\D', '', f["id"])
        return int(nums) if nums else 0
    return sorted(combined, key=sort_key)


# ═══════════════════════════════════════════════════════════════
# QUESTIONS
# ═══════════════════════════════════════════════════════════════

def ck(pattern):
    return lambda t: bool(re.search(pattern, t, re.IGNORECASE))

def ck_all(*patterns):
    return lambda t: all(re.search(p, t, re.IGNORECASE) for p in patterns)

ALL_QUESTIONS = [
    {"id":"q1","text":"Who is the CEO of NexGen Industries?","type":"direct","forScales":[0,1,2],"check":ck(r"sarah.chen"),"answer":"Sarah Chen","qEnts":["NexGen Industries"]},
    {"id":"q2","text":"What company does James Porter work for?","type":"direct","forScales":[0,1,2],"check":ck(r"orion"),"answer":"Orion Corp","qEnts":["James Porter"]},
    {"id":"q3","text":"Who founded Quantum Labs?","type":"direct","forScales":[0,1,2],"check":ck(r"wei.lin"),"answer":"Dr. Wei Lin","qEnts":["Quantum Labs"]},
    {"id":"q4a","text":"What is Project Phoenix's current budget? State only the latest amount.","type":"override","forScales":[0],"check":ck(r"500"),"answer":"$500K","qEnts":["Project Phoenix","NexGen Industries"]},
    {"id":"q4b","text":"What is Project Phoenix's current budget? State only the latest amount.","type":"override","forScales":[1],"check":ck(r"620"),"answer":"$620K","qEnts":["Project Phoenix","NexGen Industries"]},
    {"id":"q4c","text":"What is Project Phoenix's current budget? State only the latest amount.","type":"override","forScales":[2],"check":ck(r"580"),"answer":"$580K","qEnts":["Project Phoenix","NexGen Industries"]},
    {"id":"q5","text":"Who currently leads Project Phoenix?","type":"override","forScales":[1],"check":ck(r"sandra.lee"),"answer":"Sandra Lee","qEnts":["Project Phoenix"]},
    {"id":"q5b","text":"Who currently leads Project Phoenix?","type":"override","forScales":[2],"check":ck(r"kevin.wright"),"answer":"Kevin Wright","qEnts":["Project Phoenix"]},
    {"id":"q6","text":"What is Project Aurora's current budget?","type":"override","forScales":[2],"check":ck(r"720"),"answer":"$720K","qEnts":["Project Aurora","Pinnacle Tech"]},
    {"id":"q7","text":"What is the job title of Sarah Chen's husband?","type":"2-hop","forScales":[0,1,2],"check":ck_all(r"vp",r"engineer"),"answer":"VP of Engineering at Orion Corp","qEnts":["Sarah Chen"]},
    {"id":"q8","text":"Name the sibling of Quantum Labs' founder.","type":"2-hop","forScales":[0,1,2],"check":ck(r"amy.lin"),"answer":"Dr. Amy Lin","qEnts":["Quantum Labs"]},
    {"id":"q9","text":"Is there a personal connection between NexGen's CEO and anyone at Orion Corp? Describe it.","type":"3-hop","forScales":[0,1,2],"check":ck_all(r"sarah",r"james.porter",r"married"),"answer":"Sarah Chen married to James Porter (VP Eng, Orion)","qEnts":["NexGen Industries","Orion Corp"]},
    {"id":"q10","text":"Does anyone at Vertex Solutions have a family member at a company acquired by Zenith Cloud?","type":"3-hop","forScales":[0,1,2],"check":ck_all(r"rachel",r"elena",r"prism"),"answer":"Rachel Torres sister of Elena Torres at Prism Networks","qEnts":["Vertex Solutions","Zenith Cloud"]},
    {"id":"q11","text":"Trace the chain of personal and corporate relationships connecting NexGen's CEO to Quantum Labs' founder.","type":"4-hop","forScales":[0,1,2],"check":ck_all(r"sarah",r"james",r"orion",r"quantum",r"wei"),"answer":"Sarah Chen→James Porter→Orion Corp→Quantum Labs→Dr. Wei Lin","qEnts":["NexGen Industries","Quantum Labs"]},
    {"id":"q12","text":"Trace any chain from Forge Analytics' founder to Apex Biotech through relationships.","type":"4-hop","forScales":[2],
     "check": lambda t: ck_all(r"robert",r"titan",r"angela",r"raj")(t) or ck_all(r"robert",r"laura",r"helios",r"apex")(t),
     "answer":"Robert Kim→Forge→Titan→Angela Wu→Raj Patel→Apex OR Robert Kim→Laura Kim→Helios AI→Apex","qEnts":["Forge Analytics","Apex Biotech"]},
    {"id":"q13a","text":"How many companies have been acquired? Name them all.","type":"aggregation","forScales":[0],"check":ck_all(r"quantum",r"prism"),"answer":"2: Quantum Labs, Prism Networks","qEnts":[]},
    {"id":"q13b","text":"How many companies have been acquired? Name them all.","type":"aggregation","forScales":[1,2],"check":ck_all(r"quantum",r"prism",r"forge"),"answer":"3: Quantum Labs, Prism Networks, Forge Analytics","qEnts":[]},
]

def get_questions(scale):
    return [q for q in ALL_QUESTIONS if scale in q["forScales"]]


# ═══════════════════════════════════════════════════════════════
# TEMPORAL KNOWLEDGE GRAPH
# ═══════════════════════════════════════════════════════════════

class TemporalKG:
    def __init__(self, corpus):
        self.facts = {}
        self.adj = defaultdict(list)
        self.ent_facts = defaultdict(list)
        self.all_ents = set()

        for idx, fact in enumerate(corpus):
            self.facts[fact["id"]] = {**fact, "ts": idx}
            for e in fact["entities"]:
                self.all_ents.add(e)
                self.ent_facts[e].append(fact["id"])
            ents = fact["entities"]
            for i in range(len(ents)):
                for j in range(i+1, len(ents)):
                    self.adj[ents[i]].append({"target": ents[j], "factId": fact["id"], "ts": idx})
                    self.adj[ents[j]].append({"target": ents[i], "factId": fact["id"], "ts": idx})

    def get_facts_for(self, entities):
        ids = set()
        for e in entities:
            for fid in self.ent_facts.get(e, []):
                ids.add(fid)
        return sorted([self.facts[fid] for fid in ids if fid in self.facts], key=lambda f: f["ts"])

    def get_path_facts(self, path):
        return [self.facts[step["factId"]] for step in path if step["factId"] in self.facts]

    def find_all_paths(self, from_ents, to_ents, max_hops=5):
        to_set = set(to_ents)
        all_paths = []

        def dfs(node, visited, path, depth):
            if depth > max_hops:
                return
            if depth > 0 and node in to_set:
                all_paths.append(list(path))
                return
            seen_targets = set()
            for edge in self.adj.get(node, []):
                t = edge["target"]
                if t not in visited and t not in seen_targets:
                    seen_targets.add(t)
                    visited.add(t)
                    path.append({"from": node, "to": t, "factId": edge["factId"]})
                    dfs(t, visited, path, depth + 1)
                    path.pop()
                    visited.discard(t)

        for start in from_ents:
            if start in self.adj:
                dfs(start, {start}, [], 0)
        return all_paths

    def get_acquisition_facts(self):
        return [f for f in self.facts.values() if re.search(r"acqui", f["text"], re.IGNORECASE)]


# ═══════════════════════════════════════════════════════════════
# ENTITY EXTRACTION
# ═══════════════════════════════════════════════════════════════

def extract_entities(text, all_ents):
    lower = text.lower()
    found = []
    for e in all_ents:
        e_lower = e.lower()
        if e_lower in lower:
            found.append(e)
            continue
        words = e_lower.split()
        sig = [w for w in words if len(w) > 3]
        if sig and all(w in lower for w in sig):
            found.append(e)
            continue
        if words and len(words[0]) > 3 and words[0] in lower:
            found.append(e)
    return found


# ═══════════════════════════════════════════════════════════════
# QUESTION CLASSIFICATION
# ═══════════════════════════════════════════════════════════════

def classify_question(text):
    lower = text.lower()
    if re.search(r"connection|chain|trace|link between|connected to", lower):
        return "connection"
    if re.search(r"anyone at .+ have a .+ at|family member at|personal .+ between", lower):
        return "connection"
    if re.search(r"how many|name them all|list all", lower):
        return "aggregation"
    if re.search(r"current budget|currently leads|current status", lower):
        return "override"
    if re.search(r"['']s?\s+(husband|wife|spouse|sibling|sister|brother|founder|parent|daughter|son)", lower):
        return "chain"
    if re.search(r"sibling of|founder of|husband of|wife of|daughter of|son of", lower):
        return "chain"
    return "direct"


# ═══════════════════════════════════════════════════════════════
# OLLAMA API
# ═══════════════════════════════════════════════════════════════

def call_ollama(model, context, question, base_url="http://localhost:11434"):
    prompt = f"""Based ONLY on the following information, answer the question precisely.

INFORMATION:
{context}

QUESTION: {question}

Answer concisely. Trace reasoning step by step for multi-hop questions."""

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "Answer precisely based only on provided information."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data.get("message", {}).get("content", "")
            prompt_tokens = data.get("prompt_eval_count", 0)
            eval_tokens = data.get("eval_count", 0)
            return {"text": text, "inTok": prompt_tokens, "outTok": eval_tokens}
    except urllib.error.URLError as e:
        print(f"  ⚠ Ollama error: {e}")
        return {"text": "", "inTok": 0, "outTok": 0}


# ═══════════════════════════════════════════════════════════════
# ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════

def orchestrate(question, kg, model_name, verbose=False):
    entities = extract_entities(question["text"], kg.all_ents)
    q_type = classify_question(question["text"])

    if verbose:
        print(f"  Type: {q_type} | Entities: {entities}")

    # CONNECTION: multi-path DFS
    if q_type == "connection":
        if len(entities) < 2:
            if verbose: print(f"  ⚠ Only {len(entities)} entity, falling back to direct")
            facts = kg.get_facts_for(entities)
            ctx = "\n".join(f["text"] for f in facts)
            r = call_ollama(model_name, ctx, question["text"])
            return {**r, "factsUsed": len(facts), "steps": 1}

        all_paths = []
        for i in range(len(entities)):
            for j in range(i+1, len(entities)):
                paths = kg.find_all_paths([entities[i]], [entities[j]], 5)
                if verbose:
                    print(f"  Paths [{entities[i]}] → [{entities[j]}]: {len(paths)} found")
                    for pi, p in enumerate(paths):
                        path_str = " → ".join([p[0]["from"]] + [s["to"] for s in p])
                        print(f"    Path {pi+1} ({len(p)} hops): {path_str}")
                all_paths.extend(paths)

        if all_paths:
            fact_map = {}
            for path in all_paths:
                for step in path:
                    f = kg.facts.get(step["factId"])
                    if f:
                        fact_map[f["id"]] = f
            facts = sorted(fact_map.values(), key=lambda f: f["ts"])
            if verbose:
                print(f"  Path-edge facts: {len(facts)}")
                for f in facts:
                    print(f"    [{f['id']}] {f['text'][:80]}")
            ctx = "\n".join(f["text"] for f in facts)
            r = call_ollama(model_name, ctx, question["text"])
            return {**r, "factsUsed": len(facts), "steps": 1}
        else:
            facts = kg.get_facts_for(entities)
            ctx = "\n".join(f["text"] for f in facts)
            r = call_ollama(model_name, ctx, question["text"])
            return {**r, "factsUsed": len(facts), "steps": 1}

    # AGGREGATION
    if q_type == "aggregation":
        facts = kg.get_acquisition_facts()
        if verbose: print(f"  Aggregation: {len(facts)} facts")
        ctx = "\n".join(f["text"] for f in facts)
        r = call_ollama(model_name, ctx, question["text"])
        return {**r, "factsUsed": len(facts), "steps": 1}

    # CHAIN (explicit possessive)
    if q_type == "chain":
        neighbor_ents = set(entities)
        for e in entities:
            for edge in kg.adj.get(e, []):
                neighbor_ents.add(edge["target"])
        facts = kg.get_facts_for(list(neighbor_ents))
        if verbose: print(f"  Chain: {len(entities)} seed → {len(neighbor_ents)} entities → {len(facts)} facts")
        ctx = "\n".join(f["text"] for f in facts)
        r = call_ollama(model_name, ctx, question["text"])
        return {**r, "factsUsed": len(facts), "steps": 1}

    # DIRECT / OVERRIDE
    facts = kg.get_facts_for(entities)
    if verbose: print(f"  Direct: {len(facts)} facts")
    ctx = "\n".join(f["text"] for f in facts)
    r = call_ollama(model_name, ctx, question["text"])
    return {**r, "factsUsed": len(facts), "steps": 1}


def single_shot(question, corpus, model_name, verbose=False):
    ctx = "\n".join(f["text"] for f in corpus)
    if verbose: print(f"  Single-shot: {len(corpus)} facts")
    r = call_ollama(model_name, ctx, question["text"])
    return {**r, "factsUsed": len(corpus), "steps": 1}


# ═══════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════

def run_experiment(model_name, scale, conditions, verbose=False):
    corpus = get_corpus(scale)
    questions = get_questions(scale)
    kg = TemporalKG(corpus)

    print(f"\n{'='*60}")
    print(f"  Model: {model_name}")
    print(f"  Scale: {['Small (60)','Medium (120)','Large (200)'][scale]}")
    print(f"  Corpus: {len(corpus)} facts | KG: {len(kg.all_ents)} entities")
    print(f"  Questions: {len(questions)}")
    print(f"  Conditions: {', '.join(conditions)}")
    print(f"{'='*60}\n")

    results = {c: [] for c in conditions}
    sonnet_baseline = {"direct": "✓", "override": "✓", "2-hop": "✓", "3-hop": "✓", "4-hop": "~", "aggregation": "✓"}

    for qi, q in enumerate(questions):
        print(f"Q{qi+1}/{len(questions)}: [{q['type']}] {q['text'][:60]}...")

        for cond in conditions:
            t0 = time.time()

            if cond == "single-shot":
                r = single_shot(q, corpus, model_name, verbose)
            elif cond == "orchestrated":
                r = orchestrate(q, kg, model_name, verbose)
            else:
                continue

            elapsed = time.time() - t0
            correct = q["check"](r["text"])
            results[cond].append({
                "question": q,
                "answer": r["text"],
                "correct": correct,
                "facts": r["factsUsed"],
                "tokens": r["inTok"] + r["outTok"],
                "time": elapsed,
            })

            mark = "✓" if correct else "✗"
            print(f"  [{cond}] {mark} | {r['factsUsed']}f | {r['inTok']+r['outTok']}tok | {elapsed:.1f}s")
            if not correct and verbose:
                print(f"    Expected: {q['answer']}")
                print(f"    Got: {r['text'][:200]}")

    # ─── RESULTS TABLE ───
    print(f"\n{'='*60}")
    print("  RESULTS")
    print(f"{'='*60}")

    # Sonnet baseline
    print(f"\n  {'Condition':<22} {'Accuracy':>10} {'Avg Facts':>12} {'Avg Tok':>10} {'Avg Time':>10}")
    print(f"  {'-'*64}")
    print(f"  {'Sonnet (baseline)':<22} {'12/13':>10} {'11':>12} {'4,399':>10} {'—':>10}")

    for cond in conditions:
        rs = results[cond]
        if not rs:
            continue
        correct = sum(1 for r in rs if r["correct"])
        total = len(rs)
        avg_facts = sum(r["facts"] for r in rs) / total
        avg_tok = sum(r["tokens"] for r in rs) / total
        avg_time = sum(r["time"] for r in rs) / total
        pct = correct / total * 100

        print(f"  {cond:<22} {f'{correct}/{total}':>10} {f'{avg_facts:.0f}':>12} {f'{avg_tok:,.0f}':>10} {f'{avg_time:.1f}s':>10}")

    # ─── PER-TYPE BREAKDOWN ───
    print(f"\n  Per question type:")
    print(f"  {'Type':<15}", end="")
    print(f"  {'Sonnet':>8}", end="")
    for cond in conditions:
        print(f"  {cond:>14}", end="")
    print()
    print(f"  {'-'*55}")

    types_seen = []
    for q in questions:
        if q["type"] not in types_seen:
            types_seen.append(q["type"])

    for qtype in types_seen:
        type_qs = [(qi, q) for qi, q in enumerate(questions) if q["type"] == qtype]
        print(f"  {qtype:<15}", end="")
        # Sonnet baseline for this type
        sonnet_mark = sonnet_baseline.get(qtype, "?")
        print(f"  {sonnet_mark:>8}", end="")
        for cond in conditions:
            rs = results[cond]
            type_results = [rs[qi] for qi, q in type_qs if qi < len(rs)]
            correct = sum(1 for r in type_results if r["correct"])
            total = len(type_results)
            marks = "".join("✓" if r["correct"] else "✗" for r in type_results)
            print(f"  {f'{correct}/{total} {marks}':>14}", end="")
        print()

    print()


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Phase 2: Memory + Orchestration with Local Models")
    parser.add_argument("--model", default="llama3.1:8b", help="Ollama model name (default: llama3.1:8b)")
    parser.add_argument("--scale", type=int, default=2, choices=[0, 1, 2], help="Corpus scale: 0=small(60), 1=medium(120), 2=large(200)")
    parser.add_argument("--conditions", nargs="+", default=["single-shot", "orchestrated"],
                        choices=["single-shot", "orchestrated"], help="Conditions to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed retrieval logs")
    parser.add_argument("--ollama-url", default="http://localhost:11434", help="Ollama API base URL")
    args = parser.parse_args()

    # Test Ollama connection
    print(f"Testing connection to Ollama at {args.ollama_url}...")
    try:
        req = urllib.request.Request(f"{args.ollama_url}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m["name"] for m in data.get("models", [])]
            print(f"Connected. Available models: {', '.join(models)}")
            if not any(args.model in m for m in models):
                print(f"\n⚠ Model '{args.model}' not found. Pull it first:")
                print(f"  ollama pull {args.model}")
                sys.exit(1)
    except Exception as e:
        print(f"\n⚠ Cannot connect to Ollama: {e}")
        print("Make sure Ollama is running: ollama serve")
        sys.exit(1)

    # Override base URL for call_ollama
    global call_ollama
    original_call = call_ollama
    def patched_call(model, context, question, base_url=args.ollama_url):
        return original_call(model, context, question, base_url)
    call_ollama = patched_call

    run_experiment(args.model, args.scale, args.conditions, args.verbose)


if __name__ == "__main__":
    main()
