from abc import ABC, abstractmethod
class BaseAgent(ABC):
    """
    Base contract for all agents
    """

    name: str = "base-agent"
    priority: int = 100
    can_override: bool = False

    @abstractmethod
    async def run(self, state: dict) -> dict:
        pass
