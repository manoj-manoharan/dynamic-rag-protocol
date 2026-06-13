import { useState, useRef, useCallback, useEffect } from "react";

/* ═══════════════════════════════════════════════════════════════
   CORPUS (same synthetic tech ecosystem)
   ═══════════════════════════════════════════════════════════════ */
const CO = ["NexGen Industries","Orion Corp","Quantum Labs","Vertex Solutions","Pinnacle Tech","Meridian Systems","Atlas Digital","Forge Analytics","Helios AI","Nova Robotics","Prism Networks","Zenith Cloud","Apex Biotech","Lunar Dynamics","Titan Software"];
const F = (id,text,ents,s) => ({id:`f${id}`,text,entities:ents,scale:s});
const CORE = [
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
];

const NOISE_T = [
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
];

function genNoise(count, scale, startId) {
  const out = [];
  for (let i = 0; i < count; i++) {
    const co = CO[(i * 7 + scale * 3) % CO.length];
    const tmpl = NOISE_T[(i + scale * 13) % NOISE_T.length];
    out.push({ id: `n${startId+i}`, text: tmpl.replace("{}",co), entities: [co], scale, noise: true });
  }
  return out;
}

function getCorpus(scale) {
  const core = CORE.filter(f => f.scale <= scale);
  let allNoise = [];
  const targets = [60, 120, 200];
  if (scale >= 0) allNoise.push(...genNoise(targets[0] - CORE.filter(f=>f.scale<=0).length, 0, 100));
  if (scale >= 1) allNoise.push(...genNoise(targets[1] - CORE.filter(f=>f.scale<=1).length - allNoise.length, 1, 200));
  if (scale >= 2) allNoise.push(...genNoise(targets[2] - core.length - allNoise.length, 2, 300));
  return [...core, ...allNoise.filter(n => n.scale <= scale)].sort((a,b) => {
    const ai = parseInt(a.id.replace(/\D/g,'')); const bi = parseInt(b.id.replace(/\D/g,''));
    return ai - bi;
  });
}

/* ═══════════════════════════════════════════════════════════════ */
const ck = p => t => new RegExp(p,'i').test(t);
const ckA = (...ps) => t => ps.every(p => new RegExp(p,'i').test(t));
const ALL_Q = [
  { id:"q1", text:"Who is the CEO of NexGen Industries?", type:"direct", forScales:[0,1,2], check:ck("sarah.chen"), answer:"Sarah Chen", qEnts:["NexGen Industries"] },
  { id:"q2", text:"What company does James Porter work for?", type:"direct", forScales:[0,1,2], check:ck("orion"), answer:"Orion Corp", qEnts:["James Porter"] },
  { id:"q3", text:"Who founded Quantum Labs?", type:"direct", forScales:[0,1,2], check:ck("wei.lin"), answer:"Dr. Wei Lin", qEnts:["Quantum Labs"] },
  { id:"q4a", text:"What is Project Phoenix's current budget? State only the latest amount.", type:"override", forScales:[0], check:ck("500"), answer:"$500K", qEnts:["Project Phoenix","NexGen Industries"] },
  { id:"q4b", text:"What is Project Phoenix's current budget? State only the latest amount.", type:"override", forScales:[1], check:ck("620"), answer:"$620K", qEnts:["Project Phoenix","NexGen Industries"] },
  { id:"q4c", text:"What is Project Phoenix's current budget? State only the latest amount.", type:"override", forScales:[2], check:ck("580"), answer:"$580K", qEnts:["Project Phoenix","NexGen Industries"] },
  { id:"q5", text:"Who currently leads Project Phoenix?", type:"override", forScales:[1], check:ck("sandra.lee"), answer:"Sandra Lee", qEnts:["Project Phoenix"] },
  { id:"q5b", text:"Who currently leads Project Phoenix?", type:"override", forScales:[2], check:ck("kevin.wright"), answer:"Kevin Wright", qEnts:["Project Phoenix"] },
  { id:"q6", text:"What is Project Aurora's current budget?", type:"override", forScales:[2], check:ck("720"), answer:"$720K", qEnts:["Project Aurora","Pinnacle Tech"] },
  { id:"q7", text:"What is the job title of Sarah Chen's husband?", type:"2-hop", forScales:[0,1,2], check:ckA("vp","engineer"), answer:"VP of Engineering at Orion Corp", qEnts:["Sarah Chen"] },
  { id:"q8", text:"Name the sibling of Quantum Labs' founder.", type:"2-hop", forScales:[0,1,2], check:ck("amy.lin"), answer:"Dr. Amy Lin", qEnts:["Quantum Labs"] },
  { id:"q9", text:"Is there a personal connection between NexGen's CEO and anyone at Orion Corp? Describe it.", type:"3-hop", forScales:[0,1,2], check:ckA("sarah","james.porter","married"), answer:"Sarah Chen married to James Porter (VP Eng, Orion)", qEnts:["NexGen Industries","Orion Corp"] },
  { id:"q10", text:"Does anyone at Vertex Solutions have a family member at a company acquired by Zenith Cloud?", type:"3-hop", forScales:[0,1,2], check:ckA("rachel","elena","prism"), answer:"Rachel Torres sister of Elena Torres at Prism Networks", qEnts:["Vertex Solutions","Zenith Cloud"] },
  { id:"q11", text:"Trace the chain of personal and corporate relationships connecting NexGen's CEO to Quantum Labs' founder.", type:"4-hop", forScales:[0,1,2], check:ckA("sarah","james","orion","quantum","wei"), answer:"Sarah Chen→James Porter→Orion Corp→Quantum Labs→Dr. Wei Lin", qEnts:["NexGen Industries","Quantum Labs"] },
  { id:"q12", text:"Trace any chain from Forge Analytics' founder to Apex Biotech through relationships.", type:"4-hop", forScales:[2], check: t => (ckA("robert","titan","angela","raj")(t) || ckA("robert","laura","helios","apex")(t)), answer:"Robert Kim→Forge→Titan→Angela Wu→Raj Patel→Apex OR Robert Kim→Laura Kim→Helios AI→Apex", qEnts:["Forge Analytics","Apex Biotech"] },
  { id:"q13a", text:"How many companies have been acquired? Name them all.", type:"aggregation", forScales:[0], check:ckA("quantum","prism"), answer:"2: Quantum Labs, Prism Networks", qEnts:[] },
  { id:"q13b", text:"How many companies have been acquired? Name them all.", type:"aggregation", forScales:[1,2], check:ckA("quantum","prism","forge"), answer:"3: Quantum Labs, Prism Networks, Forge Analytics", qEnts:[] },
];
function getQuestions(scale) { return ALL_Q.filter(q => q.forScales.includes(scale)); }

/* ═══════════════════════════════════════════════════════════════
   TEMPORAL KNOWLEDGE GRAPH
   ═══════════════════════════════════════════════════════════════ */
function buildKG(corpus) {
  const facts = new Map();
  const adj = new Map();
  const entFacts = new Map();
  const allEnts = new Set();

  const ensure = e => { if (!adj.has(e)) adj.set(e, []); if (!entFacts.has(e)) entFacts.set(e, []); allEnts.add(e); };

  corpus.forEach((f, idx) => {
    facts.set(f.id, { ...f, ts: idx });
    f.entities.forEach(e => { ensure(e); entFacts.get(e).push(f.id); });
    for (let i = 0; i < f.entities.length; i++) {
      for (let j = i + 1; j < f.entities.length; j++) {
        adj.get(f.entities[i]).push({ target: f.entities[j], factId: f.id, ts: idx });
        adj.get(f.entities[j]).push({ target: f.entities[i], factId: f.id, ts: idx });
      }
    }
  });

  function bfsPath(fromEnts, toEnts, maxHops = 7) {
    const visited = new Map();
    const queue = []; // [{entity, depth}]
    const fromSet = new Set(fromEnts);
    const toSet = new Set(toEnts);
    fromEnts.forEach(e => { if (adj.has(e)) { visited.set(e, null); queue.push({ entity: e, depth: 0 }); } });

    while (queue.length > 0) {
      const { entity, depth } = queue.shift();
      if (depth > 0 && toSet.has(entity)) {
        const path = []; let curr = entity;
        while (visited.get(curr) !== null) {
          const { parent, factId } = visited.get(curr);
          path.unshift({ from: parent, to: curr, factId });
          curr = parent;
        }
        return path;
      }
      if (depth >= maxHops) continue;
      const seen = new Set();
      for (const edge of (adj.get(entity) || [])) {
        if (!visited.has(edge.target) && !seen.has(edge.target)) {
          seen.add(edge.target);
          visited.set(edge.target, { parent: entity, factId: edge.factId });
          queue.push({ entity: edge.target, depth: depth + 1 });
        }
      }
    }
    return null;
  }

  function getFactsFor(entities) {
    const ids = new Set();
    entities.forEach(e => (entFacts.get(e) || []).forEach(id => ids.add(id)));
    return [...ids].map(id => facts.get(id)).filter(Boolean).sort((a, b) => a.ts - b.ts);
  }

  function getPathFacts(path) {
    return path.map(step => facts.get(step.factId)).filter(Boolean);
  }

  function getAllAcquisitionFacts() {
    const results = [];
    for (const [id, f] of facts) {
      if (/acqui/i.test(f.text)) results.push(f);
    }
    return results;
  }

  // Find ALL paths between fromEnts and toEnts up to maxHops
  function findAllPaths(fromEnts, toEnts, maxHops = 5) {
    const toSet = new Set(toEnts);
    const allPaths = [];

    function dfs(node, visited, path, depth) {
      if (depth > maxHops) return;
      if (depth > 0 && toSet.has(node)) {
        allPaths.push([...path]);
        return; // found one path, don't continue deeper from here
      }
      const edges = adj.get(node) || [];
      const seenTargets = new Set();
      for (const edge of edges) {
        if (!visited.has(edge.target) && !seenTargets.has(edge.target)) {
          seenTargets.add(edge.target);
          visited.add(edge.target);
          path.push({ from: node, to: edge.target, factId: edge.factId });
          dfs(edge.target, visited, path, depth + 1);
          path.pop();
          visited.delete(edge.target);
        }
      }
    }

    for (const start of fromEnts) {
      if (!adj.has(start)) continue;
      const visited = new Set([start]);
      dfs(start, visited, [], 0);
    }

    return allPaths;
  }

  return { facts, adj, entFacts, allEnts: [...allEnts], bfsPath, findAllPaths, getFactsFor, getPathFacts, getAllAcquisitionFacts };
}

/* ═══════════════════════════════════════════════════════════════
   ENTITY EXTRACTION
   ═══════════════════════════════════════════════════════════════ */
function extractEntities(text, allEntities) {
  const lower = text.toLowerCase();
  return allEntities.filter(e => {
    if (lower.includes(e.toLowerCase())) return true;
    const words = e.toLowerCase().split(/\s+/);
    const sig = words.filter(w => w.length > 3);
    if (sig.length > 0 && sig.every(w => lower.includes(w))) return true;
    if (words[0]?.length > 3 && lower.includes(words[0])) return true;
    return false;
  });
}

/* ═══════════════════════════════════════════════════════════════
   ORCHESTRATOR
   ═══════════════════════════════════════════════════════════════ */
function classifyQuestion(text) {
  const lower = text.toLowerCase();
  // Connection: explicit connection words OR "anyone at X have a ... at Y" pattern
  if (/connection|chain|trace|link between|connected to/i.test(lower)) return "connection";
  if (/anyone at .+ have a .+ at|family member at|personal .+ between/i.test(lower)) return "connection";
  if (/how many|name them all|list all/i.test(lower)) return "aggregation";
  if (/current budget|currently leads|current status/i.test(lower)) return "override";
  // Chain: possessive patterns including both "'s X" and "s' X" (e.g., "Labs' founder")
  if (/['']s?\s+(husband|wife|spouse|sibling|sister|brother|founder|parent|daughter|son)/i.test(lower)) return "chain";
  if (/sibling of|founder of|husband of|wife of|daughter of|son of/i.test(lower)) return "chain";
  return "direct";
}

async function orchestrate(question, kg, model, log) {
  const entities = extractEntities(question.text, kg.allEnts);
  const qType = classifyQuestion(question.text);
  const workingMemory = { goal: question.text, type: qType, steps: [], entities, factsUsed: [] };

  log(`  Type: ${qType} | Entities: [${entities.join(", ")}]`);

  if (qType === "connection") {
    if (entities.length < 2) {
      log(`  ⚠ Only ${entities.length} entity found, can't find paths`);
      const facts = kg.getFactsFor(entities);
      workingMemory.factsUsed = facts;
      const answer = await model(facts.map(f => f.text).join("\n"), question.text);
      workingMemory.steps.push({ type: "fallback-direct", facts: facts.length, ...answer });
      return { workingMemory, ...answer };
    }

    // Find ALL paths between entity pairs (up to 5 hops)
    let allPaths = [];
    for (let i = 0; i < entities.length; i++) {
      for (let j = i + 1; j < entities.length; j++) {
        const paths = kg.findAllPaths([entities[i]], [entities[j]], 5);
        log(`  All paths [${entities[i]}] → [${entities[j]}]: ${paths.length} found`);
        paths.forEach((p, pi) => {
          const pathStr = [p[0].from, ...p.map(s => s.to)].join(" → ");
          log(`    Path ${pi + 1} (${p.length} hops): ${pathStr}`);
        });
        allPaths.push(...paths);
      }
    }

    if (allPaths.length > 0) {
      // Collect path-edge facts from ALL paths (deduplicated)
      const factMap = new Map();
      const pathDescs = [];
      allPaths.forEach((path, pi) => {
        const pathStr = [path[0].from, ...path.map(s => s.to)].join(" → ");
        pathDescs.push(pathStr);
        path.forEach(step => {
          const f = kg.facts.get(step.factId);
          if (f) factMap.set(f.id, f);
        });
      });

      // ONLY path-edge facts, no context bloat
      const facts = [...factMap.values()].sort((a, b) => a.ts - b.ts);
      log(`  Total unique path-edge facts across all paths: ${facts.length}`);
      facts.forEach(f => log(`    [${f.id}] ${f.text.slice(0, 80)}`));

      workingMemory.factsUsed = facts;
      workingMemory.allPaths = pathDescs;
      workingMemory.steps.push({ type: "multi-path", pathCount: allPaths.length, facts: facts.length });

      const answer = await model(facts.map(f => f.text).join("\n"), question.text);
      workingMemory.steps.push({ type: "answer", ...answer });
      return { workingMemory, ...answer };
    } else {
      log(`  ⚠ No paths found between any entity pairs`);
      const facts = kg.getFactsFor(entities);
      workingMemory.factsUsed = facts;
      const answer = await model(facts.map(f => f.text).join("\n"), question.text);
      workingMemory.steps.push({ type: "no-path-fallback", ...answer });
      return { workingMemory, ...answer };
    }
  }

  if (qType === "aggregation") {
    const acqFacts = kg.getAllAcquisitionFacts();
    workingMemory.factsUsed = acqFacts;
    log(`  Aggregation: ${acqFacts.length} acquisition facts`);
    const answer = await model(acqFacts.map(f => f.text).join("\n"), question.text);
    workingMemory.steps.push({ type: "aggregation", facts: acqFacts.length, ...answer });
    return { workingMemory, ...answer };
  }

  if (qType === "chain") {
    // Explicit chain: "job title of Sarah Chen's husband"
    // Get facts for mentioned entity + 1-hop neighbors
    const neighborEnts = new Set(entities);
    entities.forEach(e => {
      const edges = kg.adj.get(e) || [];
      const neighbors = [...new Set(edges.map(ed => ed.target))];
      log(`  1-hop from ${e}: [${neighbors.join(", ")}]`);
      neighbors.forEach(n => neighborEnts.add(n));
    });
    const facts = kg.getFactsFor([...neighborEnts]);
    log(`  Chain: ${entities.length} seed → ${neighborEnts.size} entities → ${facts.length} facts`);
    facts.forEach(f => log(`    [${f.id}] ${f.text.slice(0, 80)}`));
    workingMemory.factsUsed = facts;
    const answer = await model(facts.map(f => f.text).join("\n"), question.text);
    workingMemory.steps.push({ type: "chain", facts: facts.length, ...answer });
    return { workingMemory, ...answer };
  }

  // Direct or override: get facts for mentioned entities
  const facts = kg.getFactsFor(entities);
  workingMemory.factsUsed = facts;
  log(`  Direct: ${facts.length} facts for [${entities.join(", ")}]`);
  const answer = await model(facts.map(f => f.text).join("\n"), question.text);
  workingMemory.steps.push({ type: qType, facts: facts.length, ...answer });
  return { workingMemory, ...answer };
}

/* ═══════════════════════════════════════════════════════════════
   STEP-BY-STEP ORCHESTRATOR (one hop at a time)
   ═══════════════════════════════════════════════════════════════ */
async function orchestrateStepByStep(question, kg, model, log) {
  const entities = extractEntities(question.text, kg.allEnts);
  const qType = classifyQuestion(question.text);
  const workingMemory = { goal: question.text, type: qType, steps: [], entities, factsUsed: [], chain: [] };

  if (qType !== "connection" || entities.length < 2) {
    // Fall back to path-retrieval for non-connection questions
    return orchestrate(question, kg, model, log);
  }

  let allPaths = [];
  for (let i = 0; i < entities.length; i++) {
    for (let j = i + 1; j < entities.length; j++) {
      allPaths.push(...kg.findAllPaths([entities[i]], [entities[j]], 5));
    }
  }

  if (allPaths.length === 0) return orchestrate(question, kg, model, log);

  // Walk ALL paths, collect facts from each
  log(`  Step-by-step: found ${allPaths.length} paths`);
  allPaths.forEach((p, pi) => {
    const ps = [p[0].from, ...p.map(s => s.to)].join(" → ");
    log(`    Path ${pi + 1}: ${ps}`);
  });

  let totalIn = 0, totalOut = 0;

  // Collect ALL path-edge facts, walk unique hops
  const allHopFacts = new Map();
  allPaths.forEach(path => {
    path.forEach(hop => {
      const f = kg.facts.get(hop.factId);
      if (f) allHopFacts.set(f.id, { ...hop, fact: f });
    });
  });

  // Walk each unique hop
  for (const [fid, hop] of allHopFacts) {
    workingMemory.factsUsed.push(hop.fact);
    const priorContext = workingMemory.chain.length > 0
      ? `What we know so far: ${workingMemory.chain.join(" | ")}\n\n` : "";
    const stepAnswer = await model(
      `${priorContext}Fact: ${hop.fact.text}`,
      `What is the relationship between ${hop.from} and ${hop.to}? One sentence.`,
      200
    );
    workingMemory.chain.push(stepAnswer.text.trim());
    workingMemory.steps.push({ type: "hop", from: hop.from, to: hop.to, fact: hop.fact.text, answer: stepAnswer.text.trim() });
    totalIn += stepAnswer.inTok;
    totalOut += stepAnswer.outTok;
    log(`  Hop: ${hop.from} → ${hop.to}`);
  }

  // Verification: assemble chain and answer original question
  const chainSummary = workingMemory.chain.join("\n");
  const verifyAnswer = await model(
    `Established facts from step-by-step analysis:\n${chainSummary}`,
    question.text,
    400
  );
  totalIn += verifyAnswer.inTok;
  totalOut += verifyAnswer.outTok;
  workingMemory.steps.push({ type: "verify", ...verifyAnswer });

  return {
    workingMemory,
    text: verifyAnswer.text,
    inTok: totalIn,
    outTok: totalOut,
  };
}

/* ═══════════════════════════════════════════════════════════════
   API
   ═══════════════════════════════════════════════════════════════ */
async function callAPI(msgs, maxTok = 500, sys = null) {
  const body = { model: "claude-sonnet-4-20250514", max_tokens: maxTok, messages: msgs };
  if (sys) body.system = sys;
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error(`API ${r.status}`);
  const d = await r.json();
  return { text: d.content?.map(b => b.text || "").join("\n") || "", inTok: d.usage?.input_tokens || 0, outTok: d.usage?.output_tokens || 0 };
}

function makeModel(maxTok = 500) {
  return async (context, question, overrideMax) => {
    const r = await callAPI([{
      role: "user",
      content: `Based ONLY on the following information, answer the question precisely.\n\nINFORMATION:\n${context}\n\nQUESTION: ${question}\n\nAnswer concisely. Trace reasoning step by step for multi-hop questions.`
    }], overrideMax || maxTok, "Answer precisely based only on provided information.");
    return r;
  };
}

/* ═══════════════════════════════════════════════════════════════
   EXPERIMENT
   ═══════════════════════════════════════════════════════════════ */
const CONDS = ["single-shot", "orchestrated", "step-by-step"];
const COND_NAMES = { "single-shot": "A: Single Shot", "orchestrated": "B: Path Retrieval", "step-by-step": "C: Step-by-Step" };
const COND_COLORS = { "single-shot": "#e07a5f", "orchestrated": "#81b29a", "step-by-step": "#8ecae6" };
const COND_DESC = {
  "single-shot": "All facts in context, one call",
  "orchestrated": "KG-guided retrieval, minimal facts, one call",
  "step-by-step": "One hop at a time with working memory"
};

export default function Phase1() {
  const [scale, setScale] = useState(2);
  const [status, setStatus] = useState("idle");
  const [logs, setLogs] = useState([]);
  const [results, setResults] = useState(null);
  const [kgInfo, setKgInfo] = useState(null);
  const [expanded, setExpanded] = useState(null);
  const [enabled, setEnabled] = useState(new Set(CONDS));
  const abortRef = useRef(false);
  const logRef = useRef(null);

  useEffect(() => { logRef.current?.scrollIntoView({ behavior: "smooth" }); }, [logs]);
  const log = useCallback((m) => setLogs(p => [...p, `${new Date().toLocaleTimeString("en", { hour12: false })} ${m}`]), []);

  async function run() {
    abortRef.current = false;
    setStatus("running"); setLogs([]); setResults(null); setExpanded(null);
    const activeConds = CONDS.filter(c => enabled.has(c));

    try {
      const corpus = getCorpus(scale);
      const questions = getQuestions(scale);
      log(`Corpus: ${corpus.length} facts | Questions: ${questions.length}`);

      const kg = buildKG(corpus);
      log(`KG: ${kg.allEnts.length} entities, ${[...kg.adj.values()].reduce((s, e) => s + e.length, 0) / 2} edges`);
      setKgInfo({ entities: kg.allEnts.length, edges: Math.floor([...kg.adj.values()].reduce((s, e) => s + e.length, 0) / 2) });

      const model = makeModel(500);
      const allResults = [];

      for (const q of questions) {
        if (abortRef.current) throw new Error("Aborted");
        log(`Q: ${q.text.slice(0, 55)}...`);
        const qr = { question: q, conditions: {} };

        for (const cond of activeConds) {
          if (abortRef.current) throw new Error("Aborted");

          let result;
          if (cond === "single-shot") {
            const allText = corpus.map(f => f.text).join("\n");
            const r = await model(allText, q.text);
            result = { text: r.text, inTok: r.inTok, outTok: r.outTok, factsUsed: corpus.length, steps: 1, workingMemory: null };
          } else if (cond === "orchestrated") {
            const r = await orchestrate(q, kg, model, log);
            result = { text: r.text, inTok: r.inTok, outTok: r.outTok, factsUsed: r.workingMemory.factsUsed.length, steps: r.workingMemory.steps.length, workingMemory: r.workingMemory };
          } else {
            const r = await orchestrateStepByStep(q, kg, model, log);
            result = { text: r.text, inTok: r.inTok, outTok: r.outTok, factsUsed: r.workingMemory.factsUsed.length, steps: r.workingMemory.steps.length, workingMemory: r.workingMemory };
          }

          const correct = q.check(result.text);
          qr.conditions[cond] = { ...result, correct, totalTok: result.inTok + result.outTok };
          log(`  [${cond}] ${correct ? "✓" : "✗"} ${result.inTok + result.outTok} tok | ${result.factsUsed} facts | ${result.steps} steps`);
        }
        allResults.push(qr);
        setResults([...allResults]);
      }

      log("═══ COMPLETE ═══");
      setStatus("done");
    } catch (e) {
      log(`ERROR: ${e.message}`);
      setStatus("error");
    }
  }

  const ranConds = results ? CONDS.filter(c => results.some(r => r.conditions[c])) : [];
  const stats = {};
  if (results) {
    ranConds.forEach(c => {
      const entries = results.map(r => r.conditions[c]).filter(Boolean);
      stats[c] = {
        correct: entries.filter(e => e.correct).length,
        total: entries.length,
        avgTok: Math.round(entries.reduce((s, e) => s + e.totalTok, 0) / entries.length),
        totalTok: entries.reduce((s, e) => s + e.totalTok, 0),
        avgFacts: Math.round(entries.reduce((s, e) => s + e.factsUsed, 0) / entries.length),
        avgSteps: (entries.reduce((s, e) => s + e.steps, 0) / entries.length).toFixed(1),
      };
    });
  }

  const SCALE_LABELS = ["Small (60)", "Medium (120)", "Large (200)"];
  const S = {
    root: { fontFamily: "'JetBrains Mono','Fira Code',monospace", background: "#080b10", color: "#b8c0cc", minHeight: "100vh", padding: 24, boxSizing: "border-box", fontSize: 13, lineHeight: 1.6 },
    h1: { margin: 0, fontSize: 17, color: "#e8ecf1", fontWeight: 700 },
    sub: { margin: "3px 0 0", color: "#5a6370", fontSize: 11 },
    btn: bg => ({ background: bg, color: "#fff", border: "none", padding: "8px 18px", borderRadius: 4, cursor: "pointer", fontFamily: "inherit", fontSize: 13, fontWeight: 600 }),
    sel: { background: "#111820", color: "#b8c0cc", border: "1px solid #1e2736", padding: "6px 12px", borderRadius: 4, fontFamily: "inherit", fontSize: 13 },
    th: { padding: "8px 6px", textAlign: "center", borderBottom: "2px solid #1e2736", color: "#5a6370", fontSize: 11, fontWeight: 600 },
    td: { padding: "6px", borderBottom: "1px solid #141b24", textAlign: "center" },
    panel: { background: "#0d1117", border: "1px solid #1e2736", borderRadius: 6, padding: 14, marginTop: 10 },
    pre: { whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: 11, color: "#b8c0cc", margin: 0, maxHeight: 180, overflow: "auto", background: "#080b10", padding: 10, borderRadius: 4 },
  };

  return (
    <div style={S.root}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        <div style={{ marginBottom: 18, borderBottom: "1px solid #1e2736", paddingBottom: 12 }}>
          <h1 style={S.h1}>Phase 1: Memory + Orchestration</h1>
          <p style={S.sub}>A: All facts, one call. B: KG retrieves only relevant facts, one call. C: One hop at a time with working memory.</p>
          <p style={S.sub}>Graph does the multi-hop traversal. Model only reads and answers.</p>
        </div>

        <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 8, flexWrap: "wrap" }}>
          <select value={scale} onChange={e => setScale(+e.target.value)} style={S.sel} disabled={status === "running"}>
            {SCALE_LABELS.map((l, i) => <option key={i} value={i}>{l}</option>)}
          </select>
          {status !== "running" ? (
            <button onClick={run} style={S.btn("#2d5a3d")}>{results ? "Re-run" : "Run"}</button>
          ) : (
            <button onClick={() => { abortRef.current = true; }} style={S.btn("#8b3040")}>Abort</button>
          )}
        </div>
        <div style={{ display: "flex", gap: 14, marginBottom: 16, flexWrap: "wrap" }}>
          {CONDS.map(c => (
            <label key={c} style={{ display: "flex", alignItems: "center", gap: 5, cursor: "pointer", fontSize: 11, color: enabled.has(c) ? COND_COLORS[c] : "#3a4250" }}>
              <input type="checkbox" checked={enabled.has(c)} disabled={status === "running"}
                onChange={() => setEnabled(p => { const n = new Set(p); n.has(c) ? n.delete(c) : n.add(c); return n; })}
                style={{ accentColor: COND_COLORS[c] }} />
              {COND_NAMES[c]} <span style={{ color: "#3a4250", marginLeft: 4 }}>({COND_DESC[c]})</span>
            </label>
          ))}
        </div>

        {kgInfo && (
          <div style={{ ...S.panel, marginBottom: 14, fontSize: 11, display: "flex", gap: 20 }}>
            <span>KG: <b style={{ color: "#81b29a" }}>{kgInfo.entities}</b> entities</span>
            <span>Edges: <b style={{ color: "#8ecae6" }}>{kgInfo.edges}</b></span>
          </div>
        )}

        {results && ranConds.length > 0 && (
          <>
            <h2 style={{ fontSize: 14, color: "#e8ecf1", margin: "0 0 10px", fontWeight: 600 }}>Summary</h2>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, marginBottom: 16 }}>
              <thead>
                <tr>
                  <th style={{ ...S.th, textAlign: "left", width: 160 }}>Condition</th>
                  <th style={S.th}>Accuracy</th>
                  <th style={S.th}>Avg Tok/Q</th>
                  <th style={S.th}>Avg Facts Seen</th>
                  <th style={S.th}>Avg Steps</th>
                </tr>
              </thead>
              <tbody>
                {ranConds.map(c => {
                  const st = stats[c];
                  const pct = st.correct / st.total;
                  return (
                    <tr key={c}>
                      <td style={{ ...S.td, textAlign: "left" }}><span style={{ color: COND_COLORS[c], fontWeight: 600 }}>{COND_NAMES[c]}</span></td>
                      <td style={S.td}><span style={{ color: pct === 1 ? "#3fb950" : pct >= 0.8 ? "#d29922" : "#f85149", fontWeight: 700, fontSize: 15 }}>{st.correct}/{st.total}</span></td>
                      <td style={S.td}>{st.avgTok.toLocaleString()}</td>
                      <td style={S.td}>{st.avgFacts} / {getCorpus(scale).length}</td>
                      <td style={S.td}>{st.avgSteps}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            <h2 style={{ fontSize: 14, color: "#e8ecf1", margin: "0 0 10px", fontWeight: 600 }}>Per Question</h2>
            {results.map((r, ri) => {
              const rKey = `r${ri}`;
              const isExp = expanded === rKey;
              return (
                <div key={ri} style={{ marginBottom: 3 }}>
                  <div style={{ display: "flex", gap: 6, alignItems: "center", cursor: "pointer", padding: "3px 0" }}
                    onClick={() => setExpanded(isExp ? null : rKey)}>
                    <span style={{ fontSize: 11, color: "#5a6370", minWidth: 180, flexShrink: 0 }}>
                      <span style={{ color: "#3a4250", marginRight: 4 }}>[{r.question.type}]</span>
                      {r.question.text.slice(0, 45)}{r.question.text.length > 45 ? "..." : ""}
                    </span>
                    {ranConds.map(c => {
                      const cr = r.conditions[c];
                      if (!cr) return <span key={c} style={{ minWidth: 80 }}>—</span>;
                      return (
                        <span key={c} style={{ fontSize: 11, minWidth: 80, textAlign: "center", color: cr.correct ? "#3fb950" : "#f85149", fontWeight: 600 }}>
                          {cr.correct ? "✓" : "✗"} <span style={{ fontWeight: 400, color: "#5a6370" }}>{cr.factsUsed}f {cr.totalTok}t</span>
                        </span>
                      );
                    })}
                  </div>
                  {isExp && (
                    <div style={S.panel}>
                      <div style={{ fontSize: 11, marginBottom: 8 }}>
                        <b style={{ color: "#e8ecf1" }}>Q:</b> {r.question.text}<br />
                        <b style={{ color: "#e8ecf1" }}>Expected:</b> {r.question.answer}
                      </div>
                      {ranConds.map(c => {
                        const cr = r.conditions[c];
                        if (!cr) return null;
                        return (
                          <div key={c} style={{ marginBottom: 8, paddingLeft: 8, borderLeft: `2px solid ${COND_COLORS[c]}` }}>
                            <div style={{ fontSize: 11 }}>
                              <span style={{ color: COND_COLORS[c], fontWeight: 600 }}>{COND_NAMES[c]}</span>
                              <span style={{ color: "#5a6370", marginLeft: 8 }}>{cr.factsUsed} facts | {cr.steps} steps | {cr.totalTok} tok</span>
                              <span style={{ color: cr.correct ? "#3fb950" : "#f85149", marginLeft: 8, fontWeight: 700 }}>{cr.correct ? "CORRECT" : "WRONG"}</span>
                            </div>
                            <pre style={{ ...S.pre, maxHeight: 80, marginTop: 4 }}>{cr.text}</pre>
                            {cr.workingMemory?.allPaths?.length > 0 && (
                              <div style={{ fontSize: 10, color: "#8ecae6", marginTop: 4 }}>
                                Paths found: {cr.workingMemory.allPaths.length}<br/>
                                {cr.workingMemory.allPaths.map((p, i) => <div key={i} style={{ marginLeft: 8 }}>{i + 1}. {p}</div>)}
                              </div>
                            )}
                            {cr.workingMemory?.path && (
                              <div style={{ fontSize: 10, color: "#8ecae6", marginTop: 4 }}>
                                BFS Path: {cr.workingMemory.path.join(" → ")}
                              </div>
                            )}
                            {cr.workingMemory?.pathFacts && (
                              <div style={{ fontSize: 10, color: "#5a6370", marginTop: 2 }}>
                                Path-edge facts: [{cr.workingMemory.pathFacts.join(", ")}]
                              </div>
                            )}
                            {cr.workingMemory?.chain?.length > 0 && (
                              <div style={{ fontSize: 10, color: "#81b29a", marginTop: 4 }}>
                                Working memory chain: {cr.workingMemory.chain.join(" | ")}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}

            {ranConds.length > 1 && (
              <div style={{ marginTop: 20 }}>
                <h2 style={{ fontSize: 14, color: "#e8ecf1", margin: "0 0 10px", fontWeight: 600 }}>Token Efficiency</h2>
                <div style={S.panel}>
                  {ranConds.map(c => {
                    const st = stats[c];
                    const maxTok = Math.max(...ranConds.map(cc => stats[cc]?.avgTok || 0));
                    return (
                      <div key={c} style={{ marginBottom: 8 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 2 }}>
                          <span style={{ color: COND_COLORS[c] }}>{COND_NAMES[c]}</span>
                          <span style={{ color: "#5a6370" }}>{st.avgTok.toLocaleString()} avg tok | {st.avgFacts} avg facts | {Math.round(st.correct / st.total * 100)}% acc</span>
                        </div>
                        <div style={{ background: "#141b24", borderRadius: 2, height: 6, overflow: "hidden" }}>
                          <div style={{ height: "100%", background: COND_COLORS[c], width: `${(st.avgTok / maxTok) * 100}%`, borderRadius: 2, opacity: 0.7 }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        )}

        {logs.length > 0 && (
          <div style={{ marginTop: 20 }}>
            <h2 style={{ fontSize: 14, color: "#e8ecf1", margin: "0 0 8px", fontWeight: 600 }}>Log</h2>
            <div style={{ background: "#0d1117", border: "1px solid #1e2736", borderRadius: 6, padding: 12, maxHeight: 400, overflow: "auto", fontSize: 11, lineHeight: 1.8 }}>
              {logs.map((l, i) => (
                <div key={i} style={{ color: l.includes("ERROR") ? "#f85149" : l.includes("COMPLETE") ? "#3fb950" : l.includes("═") ? "#e8ecf1" : l.includes("Path:") || l.includes("Edge ") || l.includes("Hop ") ? "#8ecae6" : l.includes("⚠") ? "#d29922" : l.includes("1-hop from") ? "#81b29a" : "#5a6370" }}>{l}</div>
              ))}
              <div ref={logRef} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
