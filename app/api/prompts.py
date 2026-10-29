from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.prompt import Prompt, PromptVersion
from app.schemas.prompt import PromptCreate, PromptResponse
from app.services.caveman import caveman_compress, count_tokens

router = APIRouter(prefix="/prompts", tags=["Prompts"])

@router.post("/optimize", response_model=PromptResponse)
def optimize_prompt(payload: PromptCreate, db: Session = Depends(get_db)):
    
    optimized_text = caveman_compress(payload.raw_text)

    
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