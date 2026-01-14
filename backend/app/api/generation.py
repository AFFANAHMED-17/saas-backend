import base64
import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.database import get_db
from app.models import User, Subscription, Plan
from app.core.config import settings

router = APIRouter()

# Exact Router URL requested
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

@router.post("/generate")
async def generate_image(
    prompt: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # 0. Get Token
    # Try settings first, then env var
    hf_token = settings.HUGGINGFACE_API_KEY or os.getenv("HF_TOKEN")
    if not hf_token:
        raise HTTPException(status_code=500, detail="Missing HF_TOKEN configuration")

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

    # 3. Generate Image via HuggingFace Router API (Raw Request)
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Handle specific HF errors
        if response.status_code != 200:
            error_msg = f"HuggingFace API Error ({response.status_code})"
            try:
                error_json = response.json()
                error_msg = error_json.get("error", error_msg)
            except:
                error_msg = response.text
                
            print(f"Generation Error: {error_msg}")
            
            # Return JSON error format as requested
            return {
                "error": "HuggingFace generation failed",
                "details": error_msg
            }

        # Success - Convert bytes to base64
        img_base64 = base64.b64encode(response.content).decode("utf-8")
        
        # 4. Increment Usage only on success
        sub.usage_count += 1
        db.commit()
        
        return {
            "image_base64": img_base64,
            "format": "jpeg"
        }

    except Exception as e:
        print(f"Generation Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
