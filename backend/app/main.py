from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, subscriptions, invoices, admin, generation
from app.database import engine, Base
from app.worker import start_scheduler
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="SaaS Subscription Billing Platform", lifespan=lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(subscriptions.router, prefix="/api", tags=["subscriptions"])
app.include_router(invoices.router, prefix="/api", tags=["invoices"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(generation.router, prefix="/api", tags=["generation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the SaaS Billing API"}
