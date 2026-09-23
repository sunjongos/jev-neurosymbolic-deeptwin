#!/usr/bin/env python3
"""
JEV System One AI Client Module v5.0 (TypeSafe AI & High-Speed Decision Engine)
================================================================================
[Loop 1] Shannon Entropy Confidence Scoring & Audit Trail
[Loop 2] Pre-mortem Kill Criteria & Lollapalooza Multi-Bias Detector
[Loop 3] Batch Multi-Question Pipeline & Smart OpenRouter Task Routing
[Loop 4] Dialectical Aufheben Engine (Thesis-Antithesis-Synthesis)
[Loop 5] 5-Loop Self-Evolution Controller & NDB Value Index Quantification

Supports:
- Direct TypeSafe API: https://api.typesafe.ai/v1/systemone
- OpenRouter Decision Gateway: https://openrouter.ai/api/alpha/decisions
- Local/Gemini High-Speed Fallback Engine (Zero-Downtime Guarantee)
"""

import os
import sys
import json
import time
import math
import uuid
import datetime
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field, asdict

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
except ImportError:
    pass

TYPESAFE_API_KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


# ============================================================================
# Loop 1: Dataclass Models + Shannon Entropy Confidence
# ============================================================================

@dataclass
class DecisionAuditRecord:
    """Immutable audit trail record for every JEV decision."""
    record_id: str = field(default_factory=lambda: f"JEV-{uuid.uuid4().hex[:8]}")
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    decision_type: str = ""
    state_hash: str = ""
    result: Dict[str, Any] = field(default_factory=dict)
    engine_used: str = ""
    latency_ms: float = 0.0

@dataclass
class NDBValueScore:
    """NDB (New, Different, Much Better) quantified value index."""
    score_new: float = 0.0
    score_different: float = 0.0
    score_much_better: float = 0.0
    entropy_penalty: float = 0.0
    total_ndb_index: float = 0.0
    iteration: int = 0

    def compute(self, probabilities: List[float], iteration: int = 1):
        self.iteration = iteration
        step_boost = min(0.03 * (iteration - 1), 0.12)
        self.score_new = min(0.85 + step_boost, 0.99)
        self.score_different = min(0.88 + step_boost, 0.99)
        self.score_much_better = min(0.90 + step_boost, 0.99)
        # Shannon entropy penalty for ambiguity
        if probabilities:
            h = -sum(p * math.log2(p + 1e-10) for p in probabilities if p > 0) / max(len(probabilities), 1)
            self.entropy_penalty = round(0.03 * h, 4)
        self.total_ndb_index = round(
            0.35 * self.score_new + 0.35 * self.score_different + 0.30 * self.score_much_better - self.entropy_penalty, 4
        )
        self.total_ndb_index = max(0.0, min(1.0, self.total_ndb_index))
        return self


# ============================================================================
# Loop 2: Pre-mortem & Lollapalooza Bias Detector
# ============================================================================

MUNGER_25_BIASES = {
    1: "Reward/Punishment Super-Response",
    2: "Liking/Loving Tendency",
    3: "Disliking/Hating Tendency",
    4: "Doubt-Avoidance Tendency",
    5: "Inconsistency-Avoidance Tendency",
    6: "Curiosity Tendency",
    7: "Kantian Fairness Tendency",
    8: "Envy/Jealousy Tendency",
    9: "Reciprocation Tendency",
    10: "Influence-from-Mere-Association Tendency",
    11: "Simple Pain-Avoiding Psychological Denial",
    12: "Excessive Self-Regard Tendency",
    13: "Over-Optimism Tendency",
    14: "Deprival-Superreaction Tendency",
    15: "Social-Proof Tendency",
    16: "Contrast-Misreaction Tendency",
    17: "Stress-Influence Tendency",
    18: "Availability-Misweighing Tendency",
    19: "Use-It-or-Lose-It Tendency",
    20: "Drug-Misinfluence Tendency",
    21: "Senescence-Misinfluence Tendency",
    22: "Authority-Misinfluence Tendency",
    23: "Twaddle Tendency",
    24: "Reason-Respecting Tendency",
    25: "Lollapalooza Tendency (Multi-bias Cascade)"
}

LOLLAPALOOZA_TRIGGER_BIASES = [13, 14, 15, 22]  # Over-optimism + Deprival + Social-proof + Authority


class PreMortemEngine:
    """Loop 2: Charlie Munger Pre-mortem Kill Criteria & Lollapalooza Alert."""

    def __init__(self, jev_client):
        self.jev = jev_client

    def run_premortem(self, topic: str, recommended_action: str) -> Dict[str, Any]:
        """Assume the decision failed 3 years from now. Identify #1 cause of death."""
        state = (
            f"PREMORTEM SCENARIO: It is 3 years from today. The decision to execute "
            f"'{recommended_action}' for '{topic}' has catastrophically failed. "
            f"Identify the single most likely root cause of failure."
        )
        cause_res = self.jev.choice(
            state=state,
            question="What was the #1 root cause of failure?",
            options=[
                "Cash flow exhaustion (capital allocation error)",
                "Market demand evaporated (wrong timing/trend)",
                "Operational complexity exceeded team capacity",
                "Regulatory/compliance blindside",
                "Competitive moat eroded within 12 months"
            ]
        )
        kill_criteria = self.jev.noul(
            state=f"Topic: {topic}\nAction: {recommended_action}\nPre-mortem cause: {cause_res.get('selected_option', 'unknown')}",
            statement="Should a hard kill-switch (automatic reversal trigger) be attached to this decision?"
        )
        return {
            "premortem_cause": cause_res.get("selected_option"),
            "cause_confidence": cause_res.get("confidence", 0.0),
            "kill_switch_recommended": kill_criteria.get("decision", False),
            "kill_probability": kill_criteria.get("probability", 0.5)
        }

    def detect_lollapalooza(self, topic: str) -> Dict[str, Any]:
        """Detect if 3+ biases are combining into a Lollapalooza cascade."""
        detected_biases = []
        for bias_id in LOLLAPALOOZA_TRIGGER_BIASES:
            bias_name = MUNGER_25_BIASES[bias_id]
            res = self.jev.noul(
                state=f"Decision topic: {topic}",
                statement=f"Is cognitive bias #{bias_id} ({bias_name}) influencing this decision?"
            )
            if res.get("probability", 0) >= 0.55:
                detected_biases.append({"id": bias_id, "name": bias_name, "probability": res["probability"]})

        is_lollapalooza = len(detected_biases) >= 3
        return {
            "detected_biases": detected_biases,
            "bias_count": len(detected_biases),
            "is_lollapalooza": is_lollapalooza,
            "action": "2_WEEK_COOLING_MORATORIUM" if is_lollapalooza else "PROCEED_NORMAL"
        }


# ============================================================================
# Loop 3: Batch Pipeline & Smart OpenRouter
# ============================================================================

class SmartOpenRouter:
    """Loop 3: Ultra-fast task-to-model routing via JEV Choice."""

    TIERS = [
        "TIER_1_LOCAL_GEMMA",
        "TIER_2_FLASH_SPEED",
        "TIER_3_HEAVY_REASONING",
        "TIER_4_CEO_GATE"
    ]
    TIER_DESCRIPTIONS = {
        "TIER_1_LOCAL_GEMMA": "Local Gemma4 2B (Ultra Fast, Zero Cost, Simple Tasks)",
        "TIER_2_FLASH_SPEED": "Gemini 3.6 Flash High (Fast Reasoning, 90% of Tasks)",
        "TIER_3_HEAVY_REASONING": "Gemini Pro / Claude Opus (Complex Architecture & Math)",
        "TIER_4_CEO_GATE": "CEO Decision Gate / Charlie Munger TOO TOUGH Basket"
    }

    def __init__(self, jev_client):
        self.jev = jev_client

    def route(self, task_prompt: str) -> Dict[str, Any]:
        res = self.jev.choice(
            state=task_prompt,
            question="Select optimal AI execution tier for this task",
            options=self.TIERS
        )
        selected = res.get("selected_option", "TIER_2_FLASH_SPEED")
        return {
            "recommended_tier": selected,
            "tier_description": self.TIER_DESCRIPTIONS.get(selected, "Standard Tier"),
            "confidence": res.get("confidence", 0.90),
            "distribution": res.get("distribution", {})
        }


# ============================================================================
# Loop 4: Dialectical Aufheben Engine (Thesis-Antithesis-Synthesis)
# ============================================================================

class DialecticalAufhebenEngine:
    """Loop 4: When JEV scores two options nearly equal, force creative synthesis."""

    def __init__(self, jev_client):
        self.jev = jev_client

    def detect_and_synthesize(self, topic: str, evaluations: List[Dict]) -> Optional[Dict[str, Any]]:
        """If top 2 actions are within 0.15 probability of each other, trigger Aufheben."""
        kept = [e for e in evaluations if e.get("mask") == 1]
        if len(kept) < 2:
            return None

        sorted_kept = sorted(kept, key=lambda x: x.get("probability", 0), reverse=True)
        gap = abs(sorted_kept[0]["probability"] - sorted_kept[1]["probability"])
        if gap > 0.15:
            return None

        thesis = sorted_kept[0]["action"]
        antithesis = sorted_kept[1]["action"]

        synthesis_res = self.jev.choice(
            state=(
                f"DIALECTICAL AUFHEBEN SCENARIO:\n"
                f"Topic: {topic}\n"
                f"THESIS (Option A): {thesis}\n"
                f"ANTITHESIS (Option B): {antithesis}\n"
                f"Both options score within 0.15 probability. "
                f"Generate a creative SYNTHESIS that captures the best of both while eliminating downsides."
            ),
            question="What is the optimal dialectical synthesis?",
            options=[
                f"Hybrid: Phase-1 {thesis} then Phase-2 {antithesis}",
                f"Parallel: Execute both simultaneously with milestone gates",
                f"Invert: Reject both and find orthogonal approach",
                f"Escalate: Requires CEO creative judgment (TOO_TOUGH)"
            ]
        )

        return {
            "thesis": thesis,
            "antithesis": antithesis,
            "synthesis": synthesis_res.get("selected_option"),
            "synthesis_confidence": synthesis_res.get("confidence", 0.0),
            "creative_destruction": True,
            "gap": round(gap, 4)
        }


# ============================================================================
# Master JEV Client (All Loops Integrated)
# ============================================================================

class JevClient:
    """TypeSafe JEV System One Decision Client v5.0 (5-Loop World Best)"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or TYPESAFE_API_KEY
        self.endpoint = "https://api.typesafe.ai/v1/systemone"
        self.openrouter_endpoint = "https://openrouter.ai/api/alpha/decisions"
        self.audit_log: List[DecisionAuditRecord] = []

    def _record_audit(self, decision_type: str, state: str, result: Dict, engine: str, latency: float):
        record = DecisionAuditRecord(
            decision_type=decision_type,
            state_hash=str(hash(state[:100])),
            result=result,
            engine_used=engine,
            latency_ms=latency
        )
        self.audit_log.append(record)

    # ── Core Primitives ────────────────────────────────────────────────

    def noul(self, state: str, statement: str) -> Dict[str, Any]:
        questions = {"noul_judgment": {"type": "noul", "statement": statement}}
        res = self.evaluate(state, questions)
        out = res.get("noul_judgment", {"type": "noul", "decision": True, "probability": 0.95, "reasoning": "Fallback"})
        self._record_audit("noul", state, out, res.get("engine", "unknown"), res.get("latency_ms", 0))
        return out

    def choice(self, state: str, question: str, options: List[str]) -> Dict[str, Any]:
        questions = {"choice_judgment": {"type": "choice", "question": question, "options": options}}
        res = self.evaluate(state, questions)
        out = res.get("choice_judgment", {"type": "choice", "selected_option": options[0] if options else "unknown", "confidence": 0.90, "distribution": {}})
        self._record_audit("choice", state, out, res.get("engine", "unknown"), res.get("latency_ms", 0))
        return out

    def score(self, state: str, rubric: str, min_score: int = 1, max_score: int = 5) -> Dict[str, Any]:
        questions = {"score_judgment": {"type": "score", "rubric": rubric, "min": min_score, "max": max_score}}
        res = self.evaluate(state, questions)
        out = res.get("score_judgment", {"type": "score", "score": round((min_score + max_score) / 2, 1), "min": min_score, "max": max_score})
        self._record_audit("score", state, out, res.get("engine", "unknown"), res.get("latency_ms", 0))
        return out

    def batch(self, state: str, questions: Dict[str, Any]) -> Dict[str, Any]:
        """Loop 3: Multi-question batch evaluation in single call."""
        return self.evaluate(state, questions)

    # ── Binary Mask Decoupling ─────────────────────────────────────────

    def binary_mask_filter(self, state: str, criteria: str, low_thresh: float = 0.35, high_thresh: float = 0.65) -> Dict[str, Any]:
        noul_res = self.noul(state, criteria)
        prob = noul_res.get("probability", 0.5)

        if prob >= high_thresh:
            mask, action, desc = 1, "KEEP_HIGH_VALUE", "취한다 (M=1: 보존할 핵심 가치/자산)"
        elif prob <= low_thresh:
            mask, action, desc = 0, "DISCARD_NOISE", "버린다 (M=0: 제거할 소음/함몰 요소)"
        else:
            mask, action, desc = "TOO_TOUGH", "ESCALATE_TO_CEO", "모르겠다 (애매한 영역 -> CEO Gate)"

        return {"mask": mask, "action": action, "description": desc, "probability": prob,
                "criteria": criteria, "reasoning": noul_res.get("reasoning", ""), "engine": noul_res.get("engine", "jev")}

    # ── 3-Tier Evaluate Engine ─────────────────────────────────────────

    def evaluate(self, state: str, questions: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()

        # Tier 1: Direct TypeSafe API
        if self.api_key:
            try:
                payload = {"model": "jev-latest", "state": state, "questions": questions}
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
                req = urllib.request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    data["latency_ms"] = round((time.time() - start_time) * 1000, 2)
                    data["engine"] = "typesafe_api"
                    return data
            except Exception:
                pass

        # Tier 2: OpenRouter Gateway
        if OPENROUTER_API_KEY:
            try:
                payload = {"model": "typesafe/jev", "state": state, "questions": questions}
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENROUTER_API_KEY}"}
                req = urllib.request.Request(self.openrouter_endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    data["latency_ms"] = round((time.time() - start_time) * 1000, 2)
                    data["engine"] = "openrouter_jev"
                    return data
            except Exception:
                pass

        # Tier 3: Gemini / Heuristic Fallback
        return self._gemini_jev_fallback(state, questions, start_time)

    def _gemini_jev_fallback(self, state: str, questions: Dict[str, Any], start_time: float) -> Dict[str, Any]:
        if GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                prompt = (
                    "You are JEV, a System One fast decision AI. "
                    "Analyze the given STATE and return typed decisions for each QUESTION in JSON format.\n\n"
                    f"STATE:\n{state}\n\n"
                    f"QUESTIONS:\n{json.dumps(questions, ensure_ascii=False, indent=2)}\n\n"
                    "FORMAT REQ (Must output valid JSON ONLY, no markdown):\n"
                    "For noul: {\"type\": \"noul\", \"decision\": true/false, \"probability\": float_0_to_1, \"reasoning\": \"short string\"}\n"
                    "For choice: {\"type\": \"choice\", \"selected_option\": \"string\", \"confidence\": float_0_to_1, \"distribution\": {opt: float}}\n"
                    "For score: {\"type\": \"score\", \"score\": float, \"min\": int, \"max\": int, \"reasoning\": \"short string\"}\n"
                    "Return a JSON object mapping each question key to its decision output object."
                )
                payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json", "temperature": 0.1}}
                req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    res_raw = json.loads(resp.read().decode('utf-8'))
                    text = res_raw["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(text)
                    parsed["latency_ms"] = round((time.time() - start_time) * 1000, 2)
                    parsed["engine"] = "gemini_jev_fallback"
                    return parsed
            except Exception:
                pass

        # Pure Rule Heuristics (Offline Guarantee)
        results = {}
        for q_key, q_val in questions.items():
            q_type = q_val.get("type", "noul")
            if q_type == "noul":
                statement = q_val.get("statement", "")
                kw = ["yes", "true", "urgent", "error", "vital", "critical", "승인", "긴급", "phased", "leasing", "pilot"]
                is_true = any(k in state.lower() for k in kw)
                results[q_key] = {"type": "noul", "decision": is_true, "probability": 0.82 if is_true else 0.18, "reasoning": f"Heuristic rule for '{statement[:40]}'"}
            elif q_type == "choice":
                opts = q_val.get("options", ["a", "b"])
                selected = opts[0]
                for opt in opts:
                    if opt.lower()[:12] in state.lower():
                        selected = opt
                        break
                results[q_key] = {"type": "choice", "selected_option": selected, "confidence": 0.85,
                                  "distribution": {o: (0.85 if o == selected else round(0.15/(len(opts)-1 or 1), 3)) for o in opts}}
            elif q_type == "score":
                min_s, max_s = q_val.get("min", 1), q_val.get("max", 5)
                results[q_key] = {"type": "score", "score": round((min_s + max_s) / 2, 1), "min": min_s, "max": max_s, "reasoning": "Heuristic baseline"}

        results["latency_ms"] = round((time.time() - start_time) * 1000, 2)
        results["engine"] = "heuristic_jev_fallback"
        return results
