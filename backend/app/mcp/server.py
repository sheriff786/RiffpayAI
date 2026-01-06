# # # app/mcp/server.py
import sys
from pathlib import Path

# ✅ ALWAYS WORKS: force backend/ as root
BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

print("MCP PYTHONPATH:", sys.path[:2]) 
# # from mcp.server.fastmcp import FastMCP
# # from app.agents.doctor_little.agent import DoctorLittleAgent
# # from app.mcp.tools import register_doctor_little_tools

# # # Create MCP server (STDIO-based)
# # mcp = FastMCP(
# #     name="doctor-little-mcp"
# #     # description="Doctor Little MCP Server – Medical AI Agent"
# # )

# # # Initialize agent
# # agent = DoctorLittleAgent()

# # # Register tools
# # register_doctor_little_tools(mcp, agent)

# # def main():
# #     # This is what MCP CLI uses
# #     mcp.run()

# # if __name__ == "__main__":
# #     main()

# # app/mcp/server.py

# # from mcp.server.fastmcp import FastMCP
# # from agents.doctor_little.agent import DoctorLittleAgent
# # from mcp.tools import register_doctor_little_tools

# # # Create MCP server (STDIO-based)
# # mcp = FastMCP(
# #     name="doctor-little-mcp"
# # )

# # # Initialize agent (lazy LLM init already handled)
# # agent = DoctorLittleAgent()

# # # Register tools
# # register_doctor_little_tools(mcp, agent)

# # def main():
# #     mcp.run()

# # if __name__ == "__main__":
# #     main()


# # app/mcp/server.py

# import sys
# from pathlib import Path


# from mcp.server.fastmcp import FastMCP

# # NOW these imports WILL work
# from app.agents.doctor_little.agent import DoctorLittleAgent
# from app.mcp.tools import register_doctor_little_tools
# from typing import Dict
# mcp = FastMCP(
#     name="doctor-little-mcp"
# )

# agent = DoctorLittleAgent()
# # register_doctor_little_tools(mcp, agent)
# @mcp.tool()
# async def extract_medical_entities(text: str) -> Dict:
#     """
#     Extract structured medical entities from clinical text.
#     """
#     return await agent.extract_medical_entities_internal(text)

# @mcp.tool()
# async def search_clinical_evidence(query: str, max_results: int = 5) -> Dict:
#     """
#     Search clinical guidelines and evidence.
#     """
#     return await agent.search_clinical_evidence_internal(query, max_results)

# @mcp.tool()
# async def assess_clinical_risk(entities: Dict, evidence: Dict) -> Dict:
#     """
#     Assess patient clinical risk.
#     """
#     return await agent.assess_clinical_risk_internal(entities, evidence)

# @mcp.tool()
# async def generate_clinical_documentation(
#     entities: Dict,
#     risk_assessment: Dict,
#     template_type: str = "SOAP"
# ) -> Dict:
#     """
#     Generate structured clinical documentation.
#     """
#     return await agent.generate_clinical_documentation_internal(
#         entities, risk_assessment, template_type
#     )

# def main():
#     mcp.run()

# if __name__ == "__main__":
#     main()



# from mcp.server.fastmcp import FastMCP
# from app.agents.registry import AgentRegistry
# from app.agents.bootstrap import load_agents
# import os
# from dotenv import load_dotenv

# # Load .env BEFORE anything else
# load_dotenv()

# # Safety check
# if not os.getenv("OPENAI_API_KEY"):
#     raise RuntimeError("OPENAI_API_KEY not found in environment")
# load_agents() 
# mcp = FastMCP(
#     name="doctor-little-mcp",
# )



# registry = AgentRegistry()   # ✅ instantiate

# for agent in registry.get_agents():
#     mcp.add_tool(
#         name=agent.name,
#         description=f"MCP tool for {agent.name}",
#         fn=agent.run
#     )

# def main():
#     mcp.run()

# if __name__ == "__main__":
#     main()




from mcp.server.fastmcp import FastMCP
from app.agents.registry import AgentRegistry
from app.agents.bootstrap import load_agents
from dotenv import load_dotenv
import os
from typing import Dict

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found")

load_agents()

mcp = FastMCP(name="doctor-little-mcp")
registry = AgentRegistry()

for agent in registry.get_agents():

    @mcp.tool(name=agent.name)
    async def run_agent(payload: Dict, agent=agent):
        """
        MCP adapter → Agent contract
        """

        # 🔒 DoctorLittle special handling
        if agent.name == "doctor-little":
            return await agent.process_consultation(
                patient_id=payload["patient_id"],
                text_input=payload["text_input"],
                template_type=payload.get("template_type", "SOAP"),
                consultation_type=payload.get("consultation_type", "general")
            )

        # 🔁 Other agents (triage / billing / follow-up)
        return await agent.run(payload)

def main():
    mcp.run()

if __name__ == "__main__":
    main()

