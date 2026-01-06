# app/agents/bootstrap.py

from app.agents.doctor_little.agent import DoctorLittleAgent
from app.agents.triage.agent import TriageAgent
from app.agents.billing.agent import BillingAgent
from app.agents.follow_up.agent import FollowUpAgent

def load_agents():
    """
    Instantiate all agents once.
    This automatically registers them in AgentRegistry.
    """
    DoctorLittleAgent()
    TriageAgent()
    BillingAgent()
    FollowUpAgent()
