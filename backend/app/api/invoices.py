from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.database import get_db
from app.models import Invoice, User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class InvoiceSchema(BaseModel):
    id: int
    amount: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

@router.get("/invoices", response_model=List[InvoiceSchema])
def read_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return db.query(Invoice).filter(Invoice.user_id == current_user.id).all()

@router.get("/invoices/{invoice_id}/download")
def download_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id, 
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    content = f"Invoice ID: {invoice.id}\nAmount: {invoice.amount}\nStatus: {invoice.status}"
    return {"content": content, "filename": f"invoice_{invoice.id}.txt"}
