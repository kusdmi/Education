from datetime import date
import json
import os
from pydantic import BaseModel, EmailStr, validator
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Appeal Service")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


class Appeal(BaseModel):
    surname: str
    name: str
    birth_date: date
    phone: str
    email: EmailStr

    @validator('surname', 'name')
    def validate_cyrillic(cls, v):
        if not v.isalpha() or not v.isupper() or not all('А' <= char <= 'я' for char in v):
            raise ValueError('Must contain only Cyrillic characters and start with capital letter')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        cleaned = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not cleaned.startswith('+7') or len(cleaned) != 12 or not cleaned[1:].isdigit():
            raise ValueError('Phone must be in format +7 XXX XXX XX XX')
        return cleaned


@app.post("/appeal")
async def create_appeal(appeal: Appeal):
    try:
        filename = f"{appeal.surname}_{appeal.name}_{appeal.birth_date}.json"
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(appeal.dict(), f, indent=4, ensure_ascii=False, default=str)

        return {"message": "Appeal saved successfully", "file": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")