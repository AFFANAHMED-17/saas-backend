from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, subscriptions, invoices, admin, generation
from app.database import engine, Base
from app.worker import start_scheduler
from contextlib import asynccontextmanager
from app.core.config import settings

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="SaaS Subscription Billing Platform", lifespan=lifespan)

# Fetch FRONTEND_URL from env, default to localhost/vercel patterns
frontend_url = settings.FRONTEND_URL
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*.vercel.app",  # Wildcard for Vercel previews
]
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Explicit list is safer, but for Vercel wildcards we might need allow_origin_regex if using strict mode
    # For simplicity and functionality with Vercel's dynamic URLs, we'll use allow_origin_regex if needed, 
    # but Starlette's allow_origins doesn't support wildcards like *.vercel.app natively in the list without allow_origin_regex.
    # Let's use a regex for vercel.
    allow_origin_regex=r"https://.*\.vercel\.app", 
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
