#!/usr/bin/env python3
"""
Master JEV Neurosymbolic Deep Twin Engine v5.0 (World Best Decision Model)
==========================================================================
Combines:
1. SQLite Fact Ontology DB (0-Dependency Standalone Knowledge Base)
2. JEV System One Fast Decision Engine (Noul, Choice, Score, Binary Mask Filter)
3. Decoupling Engine (M=1 Keep, M=0 Discard, M=TOO_TOUGH CEO Gate)
4. Charlie Munger 3-Basket Discipline (YES / NO / TOO TOUGH)
"""

import os
import sys
import json
import time
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.append(str(Path(__file__).resolve().parent))
from jev_client import JevClient


class NeurosymbolicDeepTwinEngine:
    """Master JEV Neurosymbolic Deep Twin Engine"""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._find_ontology_db()
        self.jev = JevClient()

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
        if os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [t[0] for t in cur.fetchall()]
                tables_summary = tables[:10]
                conn.close()
            except Exception as e:
                tables_summary = [f"DB error: {e}"]
        return {
            "db_path": self.db_path,
            "status": "ONLINE" if os.path.exists(self.db_path) else "STANDALONE_LOCAL",
            "active_tables": len(tables_summary)
        }

    def evaluate_decision(self, topic: str, candidate_actions: List[str]) -> Dict[str, Any]:
        """
        Evaluate candidate actions with JEV System One Binary Masking (0/1/TOO_TOUGH)
        and categorize into Charlie Munger Baskets.
        """
        start_time = time.time()
        onto_ctx = self.fetch_ontology_context(topic)

        evaluations = []
        baskets = {
            "YES_BASKET_M1": [],
            "NO_BASKET_M0": [],
            "TOO_TOUGH_CEO_GATE": []
        }

        for action in candidate_actions:
            state = f"TOPIC: {topic}\nPROPOSED ACTION: {action}"
            mask_res = self.jev.binary_mask_filter(
                state=state,
                criteria="Is this action aligned with long-term strategic ROI and high-value creation?"
            )

            eval_item = {
                "action": action,
                "mask": mask_res["mask"],
                "description": mask_res["description"],
                "probability": mask_res["probability"],
                "reasoning": mask_res["reasoning"]
            }
            evaluations.append(eval_item)

            if mask_res["mask"] == 1:
                baskets["YES_BASKET_M1"].append(eval_item)
            elif mask_res["mask"] == 0:
                baskets["NO_BASKET_M0"].append(eval_item)
            else:
                baskets["TOO_TOUGH_CEO_GATE"].append(eval_item)

        # Optimal choice selection via JEV Choice
        choice_res = self.jev.choice(
            state=f"TOPIC: {topic}\nCANDIDATES: {json.dumps(candidate_actions, ensure_ascii=False)}",
            question="Select optimal strategic path",
            options=candidate_actions
        )

        score_res = self.jev.score(
            state=f"TOPIC: {topic}",
            rubric="Strategic Decision Urgency from 1 (low) to 5 (critical)",
            min_score=1,
            max_score=5
        )

        return {
            "topic": topic,
            "ontology_context": onto_ctx,
            "scenario_evaluations": evaluations,
            "munger_baskets": baskets,
            "recommended_action": choice_res.get("selected_option"),
            "confidence": choice_res.get("confidence", 0.90),
            "urgency_score": score_res.get("score", 3.0),
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "engine": "jev_neurosymbolic_v5"
        }

if __name__ == "__main__":
    print("=== Testing JEV Neurosymbolic Deep Twin Engine ===")
    engine = NeurosymbolicDeepTwinEngine()
    res = engine.evaluate_decision(
        topic="NDB Hospital Clinical & Capital Resource Allocation",
        candidate_actions=[
            "Execute phased leasing for MISS robotic surgical suite",
            "Full immediate cash purchase (high capex risk)",
            "Postpone expansion and keep traditional equipment"
        ]
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))
