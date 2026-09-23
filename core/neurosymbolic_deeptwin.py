#!/usr/bin/env python3
"""
Master JEV Neurosymbolic Deep Twin Engine v5.0 (5-Loop World Best Decision Model)
==================================================================================
[Loop 1] Shannon Entropy Confidence Scoring + Immutable Audit Trail
[Loop 2] Charlie Munger Pre-mortem Kill Criteria + 25-Bias Lollapalooza Detector
[Loop 3] Smart OpenRouter Task Routing + Batch Multi-Question Pipeline
[Loop 4] Dialectical Aufheben Engine (Thesis-Antithesis-Synthesis)
[Loop 5] 5-Loop Self-Evolution Controller + NDB Value Index Quantification
"""

import os
import sys
import io
import json
import time
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import asdict

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.append(str(Path(__file__).resolve().parent))
from jev_client import (
    JevClient, PreMortemEngine, DialecticalAufhebenEngine,
    SmartOpenRouter, NDBValueScore
)


class NeurosymbolicDeepTwinEngine:
    """Master JEV Neurosymbolic Deep Twin Engine v5.0 (5-Loop Self-Evolving)"""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._find_ontology_db()
        self.jev = JevClient()
        self.premortem = PreMortemEngine(self.jev)
        self.aufheben = DialecticalAufhebenEngine(self.jev)
        self.router = SmartOpenRouter(self.jev)

    def _find_ontology_db(self) -> str:
        candidates = [
            "local_ontology.db",
            "../local_ontology.db",
            "C:/Users/USER/Desktop/luca연구에이전트/local_ontology.db"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return "local_ontology.db"

    def fetch_ontology_context(self, topic: str) -> Dict[str, Any]:
        """Fetch node facts from SQLite ontology DB."""
        tables_summary = []
        node_count = 0
        if os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [t[0] for t in cur.fetchall()]
                tables_summary = tables[:15]
                # Try counting ontology nodes
                for tbl in tables:
                    if 'node' in tbl.lower() or 'triple' in tbl.lower() or 'fact' in tbl.lower():
                        try:
                            cur.execute(f"SELECT COUNT(*) FROM {tbl};")
                            node_count += cur.fetchone()[0]
                        except Exception:
                            pass
                conn.close()
            except Exception as e:
                tables_summary = [f"DB error: {e}"]
        return {
            "db_path": self.db_path,
            "status": "ONLINE" if os.path.exists(self.db_path) else "STANDALONE_LOCAL",
            "active_tables": len(tables_summary),
            "table_names": tables_summary,
            "total_fact_nodes": node_count
        }

    def evaluate_decision(self, topic: str, candidate_actions: List[str]) -> Dict[str, Any]:
        """
        Full 5-Loop Decision Pipeline:
        Loop 1: JEV Binary Mask Decoupling (0/1/TOO_TOUGH) + Shannon Entropy
        Loop 2: Pre-mortem & Lollapalooza Bias Detection
        Loop 3: Optimal Choice Selection via JEV Choice + Smart Router
        Loop 4: Dialectical Aufheben if top options are too close
        Loop 5: NDB Value Index Quantification + Self-Evolution
        """
        start_time = time.time()
        onto_ctx = self.fetch_ontology_context(topic)
        print(f"\n{'='*72}")
        print(f"⚡ [JEV Neurosymbolic Deep Twin v5.0] 5-Loop World Best Decision Engine")
        print(f"{'='*72}")
        print(f"📋 Topic: {topic}")
        print(f"🗄️ Ontology: {onto_ctx['active_tables']} tables, {onto_ctx['total_fact_nodes']} fact nodes")

        # ── Loop 1: Binary Mask Decoupling + Entropy ───────────────────
        print(f"\n--- Loop 1: JEV Binary Mask Decoupling (M=1/M=0/TOO_TOUGH) ---")
        evaluations = []
        baskets = {"YES_BASKET_M1": [], "NO_BASKET_M0": [], "TOO_TOUGH_CEO_GATE": []}
        all_probabilities = []

        for action in candidate_actions:
            state = f"TOPIC: {topic}\nPROPOSED ACTION: {action}"
            mask_res = self.jev.binary_mask_filter(
                state=state,
                criteria="Is this action aligned with long-term strategic ROI and core value creation?"
            )
            eval_item = {
                "action": action,
                "mask": mask_res["mask"],
                "description": mask_res["description"],
                "probability": mask_res["probability"],
                "reasoning": mask_res["reasoning"]
            }
            evaluations.append(eval_item)
            all_probabilities.append(mask_res["probability"])
            print(f"  ⚡ [{mask_res['mask']}] {action[:50]}... | P={mask_res['probability']:.2f}")

            if mask_res["mask"] == 1:
                baskets["YES_BASKET_M1"].append(eval_item)
            elif mask_res["mask"] == 0:
                baskets["NO_BASKET_M0"].append(eval_item)
            else:
                baskets["TOO_TOUGH_CEO_GATE"].append(eval_item)

        # ── Loop 2: Pre-mortem & Lollapalooza ──────────────────────────
        print(f"\n--- Loop 2: Pre-mortem Kill Criteria & Lollapalooza Bias Detection ---")
        # Pick the top action for pre-mortem
        top_action = evaluations[0]["action"] if evaluations else "No action"
        if baskets["YES_BASKET_M1"]:
            top_action = max(baskets["YES_BASKET_M1"], key=lambda x: x["probability"])["action"]

        premortem_result = self.premortem.run_premortem(topic, top_action)
        lollapalooza_result = self.premortem.detect_lollapalooza(topic)
        print(f"  💀 Pre-mortem #1 cause: {premortem_result['premortem_cause']}")
        print(f"  🛑 Kill switch recommended: {premortem_result['kill_switch_recommended']} (P={premortem_result['kill_probability']:.2f})")
        print(f"  🧠 Lollapalooza biases detected: {lollapalooza_result['bias_count']} -> {lollapalooza_result['action']}")

        # ── Loop 3: Optimal Choice + Smart Router ──────────────────────
        print(f"\n--- Loop 3: JEV Choice Selection & Smart OpenRouter ---")
        choice_res = self.jev.choice(
            state=f"TOPIC: {topic}\nCANDIDATES: {json.dumps(candidate_actions, ensure_ascii=False)}",
            question="Select optimal strategic path grounded in ontology facts",
            options=candidate_actions
        )
        score_res = self.jev.score(
            state=f"TOPIC: {topic}",
            rubric="Strategic Decision Urgency from 1 (low) to 5 (critical)",
            min_score=1, max_score=5
        )
        router_result = self.router.route(f"Execute decision: {topic}")
        print(f"  🎯 JEV Choice: {choice_res.get('selected_option', 'N/A')[:50]}... (C={choice_res.get('confidence', 0):.2f})")
        print(f"  📊 Urgency Score: {score_res.get('score', 0)}/5")
        print(f"  🔀 Smart Router: {router_result['recommended_tier']} ({router_result['tier_description']})")

        # ── Loop 4: Dialectical Aufheben ───────────────────────────────
        print(f"\n--- Loop 4: Dialectical Aufheben (Thesis-Antithesis-Synthesis) ---")
        aufheben_result = self.aufheben.detect_and_synthesize(topic, evaluations)
        if aufheben_result:
            print(f"  ☯️ Thesis: {aufheben_result['thesis'][:50]}...")
            print(f"  ☯️ Antithesis: {aufheben_result['antithesis'][:50]}...")
            print(f"  ✨ Synthesis: {aufheben_result['synthesis'][:60]}...")
            print(f"  💥 Creative Destruction: {aufheben_result['creative_destruction']}")
        else:
            print(f"  ✅ No dialectical friction detected (clear winner exists)")

        # ── Loop 5: NDB Value Index & Self-Evolution ───────────────────
        print(f"\n--- Loop 5: NDB Value Index Quantification & Self-Evolution ---")
        ndb_scores = []
        for iteration in range(1, 6):
            ndb = NDBValueScore()
            ndb.compute(all_probabilities, iteration=iteration)
            ndb_scores.append(ndb)

        final_ndb = ndb_scores[-1]
        print(f"  🏆 NDB Evolution Results (5 Loops):")
        for ns in ndb_scores:
            print(f"    Loop {ns.iteration}: NDB Index = {ns.total_ndb_index:.4f} (N={ns.score_new:.2f} D={ns.score_different:.2f} B={ns.score_much_better:.2f} H_penalty={ns.entropy_penalty:.4f})")

        total_latency = round((time.time() - start_time) * 1000, 2)
        print(f"\n⚡ Total Engine Latency: {total_latency}ms")
        print(f"{'='*72}\n")

        return {
            "topic": topic,
            "ontology_context": onto_ctx,
            "loop_1_scenario_evaluations": evaluations,
            "loop_1_munger_baskets": baskets,
            "loop_2_premortem": premortem_result,
            "loop_2_lollapalooza": lollapalooza_result,
            "loop_3_recommended_action": choice_res.get("selected_option"),
            "loop_3_confidence": choice_res.get("confidence", 0.90),
            "loop_3_urgency_score": score_res.get("score", 3.0),
            "loop_3_smart_router": router_result,
            "loop_4_aufheben": aufheben_result,
            "loop_5_ndb_index_final": final_ndb.total_ndb_index,
            "loop_5_ndb_evolution": [asdict(ns) for ns in ndb_scores],
            "audit_trail_count": len(self.jev.audit_log),
            "latency_ms": total_latency,
            "engine": "jev_neurosymbolic_deeptwin_v5_world_best"
        }

if __name__ == "__main__":
    engine = NeurosymbolicDeepTwinEngine()
    res = engine.evaluate_decision(
        topic="NDB Hospital 2026 MISS Robotic Surgery Suite Acquisition & 95B KRW Fund Rebalancing",
        candidate_actions=[
            "Execute phased leasing with 3-month pilot evaluation before purchase commitment",
            "Full immediate cash purchase of 15B KRW from operating fund (high capex risk)",
            "Postpone acquisition entirely and strengthen existing endoscopic equipment maintenance"
        ]
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))
