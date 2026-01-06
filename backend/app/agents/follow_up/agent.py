import json
from typing import Dict
from langchain_openai import ChatOpenAI
from langsmith import traceable
from typer import prompt
from .prompts import FOLLOW_UP_PROMPT
from app.agents.registry import AgentRegistry
import os
class FollowUpAgent:
    """
    Patient-facing follow-up communication agent.
    """
    name = "follow-up"
    priority = 40
    can_override = False

    def __init__(self):
        AgentRegistry().register(self)
        self.llm = None   # 🔥 DO NOT initialize here

    def _get_llm(self):
        if self.llm is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set")

            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                api_key=api_key
            )
        return self.llm
   
    async def generate_follow_up(
        self,
        entities: Dict,
        risk: Dict,
        soap_note: Dict
    ) -> Dict:
        try:
            prompt = FOLLOW_UP_PROMPT.format(
                chief_complaint=entities.get("chief_complaint"),
                urgency=risk.get("urgency_level"),
                risk_score=risk.get("risk_score"),
                plan=soap_note["sections"].get("plan")
            )

            llm = self._get_llm()
            response = await llm.ainvoke(prompt)
            raw = response.content.strip()

            return json.loads(raw)

        except Exception:
            return self._fallback(risk)

    def _fallback(self, risk: Dict) -> Dict:
        """
        Deterministic fallback (NO LLM)
        """
        urgency = risk.get("urgency_level", "low")

        if urgency in ["high", "critical"]:
            message = (
                "Your symptoms may be serious. Please seek medical care immediately."
            )
            follow_up = "Immediately"
            seek_help = [
                "worsening pain",
                "shortness of breath",
                "dizziness or collapse"
            ]
        else:
            message = (
                "Your symptoms appear stable at this time. Please monitor how you feel "
                "and follow the recommended plan."
            )
            follow_up = "Within 24–48 hours"
            seek_help = [
                "pain becomes severe",
                "new symptoms develop"
            ]

        return {
            "message": message,
            "follow_up_timing": follow_up,
            "seek_help_if": seek_help,
            "confidence": 0.6,
            "fall_back": True
        }
    @traceable(name="FollowUpAgent",run_type="chain")
    async def run(self, state: dict) -> dict:
        """
        BaseAgent adapter — patient-facing messaging
        """

        follow_up = await self.generate_follow_up(
            entities=state.get("entities", {}),
            risk=state.get("risk", {}),
            soap_note=state.get("note", {})
        )

        return {
            "follow_up": follow_up
        }