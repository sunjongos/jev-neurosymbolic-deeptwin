#!/usr/bin/env python3
"""
Real-world NDB Hospital Strategic & Emergency Decision Demo using JEV Neurosymbolic Deep Twin
"""

import sys
import io
import json
from pathlib import Path

# Fix cp949 encoding on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass



sys.path.append(str(Path(__file__).resolve().parent.parent / "core"))
from neurosymbolic_deeptwin import NeurosymbolicDeepTwinEngine

def run_demo():
    print("========================================================================")
    print("🏥 NDB Hospital Strategic & Clinical Decision Engine (JEV Powered v5.0)")
    print("========================================================================")

    engine = NeurosymbolicDeepTwinEngine()

    topic = "남양주백병원 2026년 척추미세침습(MISS) 센터 신규 수술 로봇 장비 도입 및 95억 운영자금 리밸런싱 안건"
    actions = [
        "전격 도입 (95억 운영자금 중 15억 일시 일시불 구매 실행)",
        "단계적 도입 (3개월 임대 성능 검증 후 성과연동 매수 진행)",
        "도입 보류 (기존 내시경 수술 장비 유지보수 강화 및 마케팅 전념)"
    ]

    result = engine.evaluate_decision(topic, actions)

    print("\n📊 1. JEV Binary Mask Decoupling (M=1, M=0, M=TOO_TOUGH):")
    for ev in result["loop_1_scenario_evaluations"]:
        print(f"  - Action: {ev['action']}")
        print(f"    Mask: {ev['mask']} ({ev['description']}) | Prob: {ev['probability']:.2f}")
        print(f"    Reasoning: {ev['reasoning']}\n")

    print("🏆 2. Charlie Munger 3-Basket Classification:")
    print("  • YES Basket (M=1):", [item['action'] for item in result['loop_1_munger_baskets']['YES_BASKET_M1']])
    print("  • NO Basket (M=0):", [item['action'] for item in result['loop_1_munger_baskets']['NO_BASKET_M0']])
    print("  • TOO TOUGH / CEO Gate (Ambiguous):", [item['action'] for item in result['loop_1_munger_baskets']['TOO_TOUGH_CEO_GATE']])

    print(f"\n🌟 3. Recommended Action: {result['loop_3_recommended_action']} (Confidence: {result['loop_3_confidence']:.2f})")
    print(f"📈 4. Final NDB Value Index: {result['loop_5_ndb_index_final']:.4f}")
    print(f"⚡ Total Engine Latency: {result['latency_ms']} ms")

if __name__ == "__main__":
    run_demo()
