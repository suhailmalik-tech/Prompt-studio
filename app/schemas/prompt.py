from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional



class PromptCreate(BaseModel):
    title:str
    raw_text:str
    mode: str = Field(default="semantic", description="Optimization moe: 'caveman' or 'semantic' ")



class PromptVersionResponse(BaseModel):
    id:int
    raw_text: str
    optimized_text: str
    original_token_count: int
    optimized_token_count: int
    compression_ratio: float
    created_at: datetime



    class Config:
        from_attributes = True



class PromptResponse(BaseModel):
    id:int
    title:str
    created_at:datetime
    versions:List[PromptVersionResponse]=[]

    class Config:
        from_attributes =True

class PromptSummaryResponse(BaseModel):
    id:int
    title:str
    created_at:datetime

    class Config:
        from_attributes = True