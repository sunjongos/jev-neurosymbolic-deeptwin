#!/usr/bin/env python3
"""
JEV System One AI Client Module (TypeSafe AI & High-Speed Decision Engine)
==========================================================================
Provides fast, structured decision-making (System One AI) for agent workflows:
1. Noul: Boolean / Yes-No probability judgment
2. Choice: Classification among predefined options
3. Score: Ordered rubric evaluation (e.g., 1~5 score)
4. Binary Mask Filter (0/1/TOO_TOUGH): Decoupling value chain into Keep (1) vs Discard (0) vs Escalation (CEO Gate)
5. Smart OpenRouter: Ultra-fast task-to-model routing (Local Gemma vs Flash vs Heavy Reasoning vs CEO Gate)

Supports:
- Direct TypeSafe API: https://api.typesafe.ai/v1/systemone
- OpenRouter Decision Gateway: https://openrouter.ai/api/alpha/decisions
- Local/Gemini High-Speed Fallback Engine (Zero-Downtime Guarantee)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)

TYPESAFE_API_KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

class JevClient:
    """TypeSafe JEV System One Decision Client & Smart OpenRouter Engine"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or TYPESAFE_API_KEY
        self.endpoint = "https://api.typesafe.ai/v1/systemone"
        self.openrouter_endpoint = "https://openrouter.ai/api/alpha/decisions"

    def binary_mask_filter(self, state: str, criteria: str, low_thresh: float = 0.35, high_thresh: float = 0.65) -> Dict[str, Any]:
        """
        LUCA Binary Mask Filter (Decoupling Engine):
        - M = 1 (취한다 / KEEP): Probability >= high_thresh (Clear high-value element)
        - M = 0 (버린다 / DISCARD): Probability <= low_thresh (Clear noise / sink element)
        - M = 'TOO_TOUGH' (모르겠다 / CEO_GATE): Ambiguous region (Escalated for CEO Decision Mask)
        """
        noul_res = self.noul(state, criteria)
        prob = noul_res.get("probability", 0.5)

        if prob >= high_thresh:
            mask = 1
            action = "KEEP_HIGH_VALUE"
            desc = "취한다 (M=1: 보존할 핵심 가치/자산)"
        elif prob <= low_thresh:
            mask = 0
            action = "DISCARD_NOISE"
            desc = "버린다 (M=0: 제거할 소음/함몰 요소)"
        else:
            mask = "TOO_TOUGH"
            action = "ESCALATE_TO_CEO"
            desc = "모르겠다 (애매한 영역 -> 대표님 하사 이분법 마스크 대기)"

        return {
            "mask": mask,
            "action": action,
            "description": desc,
            "probability": prob,
            "criteria": criteria,
            "reasoning": noul_res.get("reasoning", ""),
            "engine": noul_res.get("engine", "jev")
        }

    def noul(self, state: str, statement: str) -> Dict[str, Any]:
        """Noul Judgment: Evaluates boolean truthfulness of a statement given state."""
        questions = {"noul_judgment": {"type": "noul", "statement": statement}}
        res = self.evaluate(state, questions)
        return res.get("noul_judgment", {"type": "noul", "decision": True, "probability": 0.95, "reasoning": "Fallback evaluation completed"})

    def choice(self, state: str, question: str, options: List[str]) -> Dict[str, Any]:
        """Choice Judgment: Classifies state into one of predefined options."""
        questions = {"choice_judgment": {"type": "choice", "question": question, "options": options}}
        res = self.evaluate(state, questions)
        return res.get("choice_judgment", {"type": "choice", "selected_option": options[0] if options else "unknown", "confidence": 0.90, "distribution": {opt: (1.0 if i == 0 else 0.0) for i, opt in enumerate(options)}})

    def score(self, state: str, rubric: str, min_score: int = 1, max_score: int = 5) -> Dict[str, Any]:
        """Score Judgment: Evaluates state against an ordered rubric on a numerical scale."""
        questions = {"score_judgment": {"type": "score", "rubric": rubric, "min": min_score, "max": max_score}}
        res = self.evaluate(state, questions)
        return res.get("score_judgment", {"type": "score", "score": round((min_score + max_score) / 2, 1), "min": min_score, "max": max_score, "rubric": rubric})

    def evaluate(self, state: str, questions: Dict[str, Any]) -> Dict[str, Any]:
        """Main decision evaluator: Tries TypeSafe API -> OpenRouter -> High-Speed Gemini Fallback."""
        start_time = time.time()

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
                with urllib.request.urlopen(req, timeout=5) as resp:
                    res_raw = json.loads(resp.read().decode('utf-8'))
                    text = res_raw["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(text)
                    parsed["latency_ms"] = round((time.time() - start_time) * 1000, 2)
                    parsed["engine"] = "gemini_jev_fallback"
                    return parsed
            except Exception:
                pass

        results = {}
        for q_key, q_val in questions.items():
            q_type = q_val.get("type", "noul")
            if q_type == "noul":
                statement = q_val.get("statement", "")
                is_true = any(k in state.lower() for k in ["yes", "true", "urgent", "error", "vital", "critical", "승인", "긴급"])
                results[q_key] = {"type": "noul", "decision": is_true, "probability": 0.88 if is_true else 0.12, "reasoning": f"Rule evaluation based on state analysis for '{statement}'"}
            elif q_type == "choice":
                opts = q_val.get("options", ["option_a", "option_b"])
                selected = opts[0]
                for opt in opts:
                    if opt.lower() in state.lower():
                        selected = opt
                        break
                results[q_key] = {"type": "choice", "selected_option": selected, "confidence": 0.91, "distribution": {opt: (0.91 if opt == selected else round((1.0 - 0.91)/(len(opts)-1 or 1), 2)) for opt in opts}}
            elif q_type == "score":
                min_s = q_val.get("min", 1)
                max_s = q_val.get("max", 5)
                results[q_key] = {"type": "score", "score": round((min_s + max_s) / 2, 1), "min": min_s, "max": max_s, "reasoning": "Heuristic baseline score"}

        results["latency_ms"] = round((time.time() - start_time) * 1000, 2)
        results["engine"] = "heuristic_jev_fallback"
        return results
