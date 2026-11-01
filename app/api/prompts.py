from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.models.user import User
from app.core.deps import get_current_user
from app.core.db import get_db
from app.models.prompt import Prompt, PromptVersion
from app.schemas.prompt import PromptCreate, PromptResponse, PromptSummaryResponse, PromptAnalyticsResponse
from app.services.caveman import caveman_compress, count_tokens
from app.services.llm_services import semantic_compression

router = APIRouter(prefix="/prompts", tags=["Prompts"])

@router.post("/optimize", response_model=PromptResponse)
def optimize_prompt(payload: PromptCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):

    user_prompt_count = db.query(Prompt).filter(Prompt.user_id == current_user.id).count()
    if user_prompt_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quota Exceeded: Free accounts are limited to a maximum of 3 prompt optimizations."
        )   
    if payload.mode.lower() == "caveman":
        optimized_text = caveman_compress(payload.raw_text)
    
    else:
        prefiltered = caveman_compress(payload.raw_text)
        optimized_text = semantic_compression(prefiltered)
    
    orig_tokens = count_tokens(payload.raw_text)
    opt_tokens = count_tokens(optimized_text)
    

    ratio = round(1 - (opt_tokens / orig_tokens), 2) if orig_tokens > 0 else 0.0

    db_prompt = Prompt(title=payload.title)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)

  
    db_version = PromptVersion(
        prompt_id=db_prompt.id,
        raw_text=payload.raw_text,
        optimized_text=optimized_text,
        original_token_count=orig_tokens,
        optimized_token_count=opt_tokens,
        compression_ratio=ratio
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)

    
    db.refresh(db_prompt)
    return db_prompt


@router.get("/", response_model=List[PromptSummaryResponse])
def list_prompts(skip: int=0, limit=20, db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of all saved prompts.
    """
    prompts = db.query(Prompt).offset(skip).limit(limit).all()
    return prompts


@router.get("/analytics/summary", response_model=PromptAnalyticsResponse)
def get_prompt_analytics(db: Session=Depends(get_db)):
    total_prompts = db.query(Prompt).count()
    total_versions = db.query(PromptVersion).count()


    if total_versions == 0:
        return {
            "total_prompts" : 0,
            "total_optimizations":0,
            "total_tokens_saved":0,
            "average_compression_ratio":0.0
}


    stats = db.query(
        func.sum(PromptVersion.original_token_count - PromptVersion.optimized_token_count),
        func.avg(PromptVersion.compression_ratio)
    ).one()


    return {
        "total_prompts": total_prompts,
        "total_optimizations": total_versions,
        "total_tokens_saved": int(stats[0] or 0),
        "average_compression_ratio": round(stats[1], 2) if stats[1] else 0.0

    }

@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt_detail(prompt_id:int, db:Session = Depends(get_db)):
    """
    Retrieve a specific prompt and all its optimization version history by ID.

    """

    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    raise prompt


@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int, db:Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    db.delete(prompt)
    db.commit()


    return {"message":f"Prompt {prompt_id} deleted successfully. "}
