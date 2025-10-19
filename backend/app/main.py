from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .routers import auth, tickets, contracts, slas, reports

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(contracts.router)
app.include_router(slas.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "Ticketing System API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
