# from typing import Dict, List
# from app.agents.base import BaseAgent

# class AgentRegistry:
#     def __init__(self):
#         self._agents: List[BaseAgent] = []

#     def register(self, agent: BaseAgent):
#         self._agents.append(agent)
#         self._agents.sort(key=lambda a: a.priority)

#     def get_agents(self) -> List[BaseAgent]:
#         return self._agents



from typing import List
from app.agents.base import BaseAgent

class AgentRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._agents = []
        return cls._instance

    def register(self, agent: BaseAgent):
        self._agents.append(agent)
        self._agents.sort(key=lambda a: a.priority)

    def get_agents(self) -> List[BaseAgent]:
        return self._agents

