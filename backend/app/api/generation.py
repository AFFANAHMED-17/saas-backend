import base64
import io
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.database import get_db
from app.models import User, Subscription, Plan
from app.core.config import settings
from huggingface_hub import InferenceClient

router = APIRouter()

# Using FLUX.1-schnell as it is currently supported and working on Serverless API
MODEL_ID = "black-forest-labs/FLUX.1-schnell"

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

    # 3. Generate Image via HuggingFace InferenceClient
    client = InferenceClient(token=settings.HUGGINGFACE_API_KEY)

    try:
        # returns a PIL Image
        image = client.text_to_image(prompt, model=MODEL_ID)
        
        # Convert PIL Image to Bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Convert bytes to base64
        img_base64 = base64.b64encode(img_byte_arr).decode("utf-8")
        
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
