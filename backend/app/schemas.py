from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PlanBase(BaseModel):
    name: str
    price: int
    interval: str
    request_limit: Optional[int] = 1000
    description: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: int
    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    plan_id: Optional[int] = None

class SubscriptionCreate(SubscriptionBase):
    plan_id: int

class Subscription(SubscriptionBase):
    id: int
    status: str
    current_period_end: datetime
    usage_count: int
    plan: Optional[Plan] = None # Nested Plan

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    subscription: List[Subscription] = [] # Nested Subscriptions
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
