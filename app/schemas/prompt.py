from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional



class PromptCreate(BaseModel):
    title:str
    raw_text:str


class PromptVersionResponse(BaseModel):
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