from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.database import get_db
from app.models import Plan, Subscription, User
from app.schemas import PlanCreate, Plan as PlanSchema, SubscriptionCreate
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/plans", response_model=PlanSchema)
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_plan = Plan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get("/plans", response_model=List[PlanSchema])
def read_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    return db.query(Plan).all()

@router.delete("/plans/{plan_id}", response_model=dict)
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    db.delete(plan)
    db.commit()
    return {"message": "Plan deleted successfully"}

@router.post("/subscribe", response_model=dict)
def create_subscription(
    sub: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Check if plan exists
    plan = db.query(Plan).filter(Plan.id == sub.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Check if already subscribed
    existing_sub = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    
    if existing_sub:
        raise HTTPException(status_code=400, detail="User already has an active subscription")

    # Create subscription (Mock Payment)
    new_sub = Subscription(
        user_id=current_user.id,
        plan_id=sub.plan_id,
        status="active",
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=30) 
    )
    db.add(new_sub)
    db.commit()
    return {"message": "Subscription created successfully"}
