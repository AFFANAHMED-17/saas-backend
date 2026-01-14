import base64
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.api import deps
from app.database import get_db
from app.models import User, Subscription, Plan
from app.core.config import settings
import requests
import io

router = APIRouter()

API_URL = "https://router.huggingface.co/hf-inference/models/runwayml/stable-diffusion-v1-5"

@router.post("/generate")
async def generate_image(
    prompt: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # 1. Check if user has an active subscription
    sub = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    
    if not sub:
        raise HTTPException(status_code=403, detail="Active subscription required")
    
    # 2. Check usage limits
    plan = db.query(Plan).filter(Plan.id == sub.plan_id).first()
    limit = plan.request_limit if plan.request_limit else 1000
    
    if sub.usage_count >= limit:
        raise HTTPException(status_code=403, detail="Usage limit exceeded for this plan")

    # 3. Generate Image via HuggingFace API
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
             raise Exception(f"API Error: {response.text}")

        # Convert bytes to base64
        img_base64 = base64.b64encode(response.content).decode("utf-8")
        
        # 4. Increment Usage only on success
        sub.usage_count += 1
        db.commit()
        
        return {
            "image_base64": img_base64,
            "format": "jpeg"
        }

    except Exception as e:
        print(f"Generation Error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
