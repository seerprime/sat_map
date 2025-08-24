from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import random
import uuid
from datetime import datetime, timedelta
from utils.config import settings

router = APIRouter()

# Pydantic models
class UserAction(BaseModel):
    user_id: str
    action_type: str  # "report", "verification", "cleanup", "share", "false_report"