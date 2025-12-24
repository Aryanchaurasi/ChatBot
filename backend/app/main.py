from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .routers import chat
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="DualLLM TruthBot API",
    description="Multi-LLM chatbot with judge comparison",
    version="1.0.0"
)

# CORS middleware
origins = os.getenv("ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
create_tables()

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "DualLLM TruthBot API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}