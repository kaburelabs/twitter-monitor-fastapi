from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import datetime
from datetime import date as date_type


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150)


class UserRegister(User):
    password: str = Field(..., min_length=6)


class ProjectDisplay(BaseModel):
    project_name: str
    alias_name: str
    total_followers: int
    following: int
    Location: Optional[str]
    created_at: Optional[datetime]
    website_url: Optional[HttpUrl]
    image_url: HttpUrl
    last_updated: Optional[datetime]
    verified: Optional[bool]
    oficial_drop: Optional[date_type]


class ProjectInCards(BaseModel):
    project_name: str
    alias_name: str
    total_followers: int
    following: int
    Location: Optional[str]
    website_url: Optional[HttpUrl]
    image_url: HttpUrl
    last_updated: Optional[datetime]


class HistoricalData(BaseModel):
    date: datetime
    followers: int
    following: int
    

class OutputHistorical(BaseModel):
    project: str
    history: List[HistoricalData]


class UpdateProject(BaseModel):
    Location: Optional[str]
    website_url: Optional[HttpUrl]
    oficial_drop: Optional[date_type]
