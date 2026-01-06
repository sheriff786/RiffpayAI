class AgentRouter:
    def __init__(self, registry):
        self.registry = registry

    async def run(self, payload: dict) -> dict:
        state = payload.copy()

        for agent in self.registry.get_agents():
            result = await agent.run(state)

            # merge output
            state.update(result)

            # override rule
            if agent.can_override and result.get("decision"):
                state["final_decision"] = result["decision"]
                state['risk']['urgency_level'] = result['final_decision']

        return state
