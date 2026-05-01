from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from . import models

router = APIRouter()

@router.get("/accounts")
def read_accounts():
    return models.get_accounts()

@router.post("/transactions")
def create_transaction(payload: Dict[str, Any]):
    date = payload.get("date")
    description = payload.get("description")
    entries = payload.get("entries")
    
    if not date or not entries:
        raise HTTPException(status_code=400, detail="Missing date or entries")
        
    if not description:
        description = "Initial Balance / Entry"
        
    debits = sum(e.get('debit', 0) for e in entries)
    credits = sum(e.get('credit', 0) for e in entries)
    
    if abs(debits - credits) > 0.01:
        raise HTTPException(status_code=400, detail="Debits must equal credits")
        
    success, msg = models.add_transaction(date, description, entries)
    if not success:
        raise HTTPException(status_code=500, detail=msg)
    return {"message": msg}

@router.get("/journal")
def read_journal():
    return models.get_journal()
