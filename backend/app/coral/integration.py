from app.agents.registry import AgentRegistry
from app.agents.router import AgentRouter

from app.agents.doctor_little.agent import DoctorLittleAgent
from app.agents.triage.agent import TriageAgent
from app.agents.billing.agent import BillingAgent
from app.agents.follow_up.agent import FollowUpAgent

class CoralOrchestrator:
    def __init__(self):
        registry = AgentRegistry()

        # REGISTER AGENTS (order matters)
        registry.register(DoctorLittleAgent())
        registry.register(TriageAgent())
        registry.register(BillingAgent())
        registry.register(FollowUpAgent())

        self.router = AgentRouter(registry)

    async def handle_consultation(self, patient_id: str, text: str):
        initial_state = {
            "patient_id": patient_id,
            "text": text
        }

        final_state = await self.router.run(initial_state)
        return final_state
