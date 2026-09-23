---
name: JEV Neurosymbolic Deep Twin Decision Engine
description: TypeSafe JEV System One AI(70~200ms)와 0-Dependency SQLite 팩트 온톨로지 DB, Charlie Munger 3-Basket 규율 및 LUCA 이분법 마스크(M=1/0/TOO_TOUGH)가 유기적으로 융합된 차세대 의사결정 딥트윈 스킬입니다.
---

# ⚡ JEV Neurosymbolic Deep Twin Decision Engine Skill (v5.0 World Best)

본 스킬은 **TypeSafe AI JEV (System One Fast Decision AI)**의 초저지연 판단 Primitives와 **0-Dependency SQLite 팩트 온톨로지 DB**, **Charlie Munger 3-Basket 규율** 및 **LUCA 이분법 마스크 Decoupling**을 결합한 차세대 AI 딥트윈 의사결정 지원 스킬입니다.

---

## 🌟 핵심 결합 아키텍처

1. **JEV System One Decision Primitives**:
   - `Noul`: 예/아니오 및 명제 확률 판단 ($P \in [0.0, 1.0]$)
   - `Choice`: 카테고리 분류 및 확신도 분포
   - `Score`: 루브릭 기반 1~5점 정량 점수

2. **LUCA Binary Mask Decoupling ($M \in \{0, 1, \text{'TOO\_TOUGH'}\}$)**:
   - $M = 1$ (취한다 / KEEP): Probability $\ge 0.65$ (핵심 가치 보존)
   - $M = 0$ (버린다 / DISCARD): Probability $\le 0.35$ (소음/함몰 요소 제거)
   - $M = \text{'TOO\_TOUGH'}$ (잘 모르겠다 / CEO Gate): $0.35 < P < 0.65$ (애매한 영역 ➔ 대표님 하사 마스크 대기)

3. **Charlie Munger 3-Basket Discipline**:
   - `YES Basket` ($M=1$)
   - `NO Basket` ($M=0$)
   - `TOO TOUGH Basket` (Ambiguous ➔ CEO Gate)

---

## 💻 Quickstart

```python
from core.neurosymbolic_deeptwin import NeurosymbolicDeepTwinEngine

engine = NeurosymbolicDeepTwinEngine()
result = engine.evaluate_decision(
    topic="남양주백병원 수술 로봇 도입 안건",
    candidate_actions=[
        "단계적 임대 후 매수",
        "전액 일시불 구매",
        "도입 보류"
    ]
)
print(result)
```
