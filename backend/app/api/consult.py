from fastapi import APIRouter
from pydantic import BaseModel
from app.coral.integration import CoralOrchestrator

router = APIRouter()
coral = CoralOrchestrator()

class ConsultRequest(BaseModel):
    patient_id: str
    text: str

@router.post("/consult")
async def consult(req: ConsultRequest):
    return await coral.handle_consultation(
        patient_id=req.patient_id,
        text=req.text
    )
