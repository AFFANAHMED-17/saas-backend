from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Subscription, Invoice
import time

def process_billing():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        due_subs = db.query(Subscription).filter(
            Subscription.status == "active",
            Subscription.current_period_end < now
        ).all()

        if due_subs:
            print(f"Processing billing for {len(due_subs)} subscriptions...")

        for sub in due_subs:
            amount = sub.plan.price
            invoice = Invoice(
                user_id=sub.user_id,
                amount=amount,
                status="paid",
                created_at=now
            )
            db.add(invoice)
            sub.current_period_end = sub.current_period_end + timedelta(days=30)
            db.commit()
            print(f"Billed user {sub.user_id} for plan {sub.plan.name}")
            
    except Exception as e:
        print(f"Billing error: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_billing, 'interval', minutes=1)
    scheduler.start()
    return scheduler
