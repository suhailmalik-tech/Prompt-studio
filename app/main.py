from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.core.db import get_db, engine
from app.models.prompt import Base






Base.metadata.create_all(bind=engine)



app = FastAPI(title=settings.PROJECT_NAME)



@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}API"}



@app.get("/health")
def health_check(db:Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database":"connected",
            "tables": "initialized"


        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )