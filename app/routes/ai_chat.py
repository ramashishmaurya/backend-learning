from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..config import settings
from ..schemas import CharRequest , CharResponse
from ..models import Chathistory

router = APIRouter(prefix="/ai" , tags=["Ai Chat"])

