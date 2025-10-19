from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .routers import auth, users, tickets, contracts, reports

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ticketing System API",
    description="A comprehensive ticketing system with role-based access control",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(contracts.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Ticketing System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
