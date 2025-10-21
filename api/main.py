import re
from fastapi import FastAPI, Depends, status, HTTPException, Request, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
import hashlib
from . import models, schemas
from .database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from collections import Counter
from typing import Optional
from sqlalchemy import cast, Boolean, Integer


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="String analyzer"
)


def parse_natural_language_query(text: str):
    filters = {}

    # Palindrome detection
    if "palindrome" in text or "palindromic" in text:
        filters["is_palindrome"] = True

    # Length-based
    match = re.search(r"longer than (\d+)", text)
    if match:
        filters["min_length"] = int(match.group(1)) + 1

    match = re.search(r"shorter than (\d+)", text)
    if match:
        filters["max_length"] = int(match.group(1)) - 1

    # Word count (e.g., "single word" → 1)
    if "single word" in text:
        filters["word_count"] = 1
    elif "two words" in text:
        filters["word_count"] = 2
    elif "three words" in text:
        filters["word_count"] = 3

    # Contains letter/character
    match = re.search(r"contain(?:s|ing)? the letter ([a-z])", text)
    if match:
        filters["contains_character"] = match.group(1)

    # Handle special phrase like “first vowel”
    if "first vowel" in text:
        filters["contains_character"] = "a"  # heuristic from spec

    return filters

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    error_type = first_error.get("type", "")
    field = first_error.get("loc", ["body"])[-1]

    # Missing field
    if "missing" in error_type:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Invalid request body or missing '{field}' field"}
        )

    # Wrong data type (string expected but got int, list, etc.)
    elif "type_error" in error_type or "string_type" in error_type:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": f"Invalid data type for '{field}' field"}
        )

    # Any other validation issue
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid request body"}
    )

@app.get("/")
def home():
    return RedirectResponse("/docs")
    

@app.post("/strings", status_code=status.HTTP_201_CREATED, response_model=schemas.stringResponse)
def create_string(blob: schemas.stringCreate, db: Session = Depends(get_db)):
    try:
        string_hash = hashlib.sha256(blob.value.encode("utf-8")).hexdigest()
        counter = Counter(blob.value)
        words = blob.value.split(" ")
        data = {} 
        data['id'] = string_hash
        data['value'] = blob.value
        data['properties'] = {
            "length": len(blob.value),
            "is_palindrome": blob.value.lower()[::-1] == blob.value.lower(),
            "unique_characters": len(counter),
            "word_count": len(words),
            "sha256_hash": string_hash,
            "character_frequency_map": dict(counter)
        }
        new_string = models.Strings(**data)
        db.add(new_string)
        db.commit()
        db.refresh(new_string)
        return new_string

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"String {blob.value} already exists"
        )

@app.get("/strings/filter-by-natural-language")
def filter_by_natural_language(
    query: str,
    db: Session = Depends(get_db)
):
    parsed_filters = parse_natural_language_query(query.lower())
    if not parsed_filters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query"
        )

    sql_query = db.query(models.Strings)

    if "is_palindrome" in parsed_filters:
        sql_query = sql_query.where(
            cast(models.Strings.properties["is_palindrome"], Boolean) == parsed_filters["is_palindrome"]
        )

    if "min_length" in parsed_filters:
        sql_query = sql_query.where(
            cast(models.Strings.properties["length"], Integer) >= parsed_filters["min_length"]
        )

    if "word_count" in parsed_filters:
        sql_query = sql_query.where(
            cast(models.Strings.properties["word_count"], Integer) == parsed_filters["word_count"]
        )

    if "contains_character" in parsed_filters:
        sql_query = sql_query.where(
            models.Strings.value.contains(parsed_filters["contains_character"])
        )

    results = sql_query.all()

    return {
        "data": results,
        "count": len(results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }

@app.get("/strings/{string_value}", response_model=schemas.stringResponse)
def get_string(string_value: str, db: Session = Depends(get_db)):
    string = db.query(models.Strings).where(models.Strings.value == string_value).first()
    if string is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String doesn't exist in database"
        )
    return string

@app.get("/strings")
def get_strings(
     is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    word_count: Optional[int] = None,
    contains_character: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Strings)

    if is_palindrome is not None:
        query = query.where(
            cast(models.Strings.properties["is_palindrome"], Boolean) == is_palindrome
        )
    if min_length is not None:
        query = query.where(
            cast(models.Strings.properties["length"], Integer) >= min_length
        )
    if max_length is not None:
        query = query.where(
            cast(models.Strings.properties["length"], Integer) <= max_length
        )
    if word_count is not None:
        query = query.where(
            cast(models.Strings.properties["word_count"], Integer) == word_count
        )
    if contains_character:
        query = query.where(models.Strings.value.contains(contains_character))

    results = query.all()

    return {
        "data": results,
        "count": len(results),
        "filters_applied": {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character,
        },
    }

@app.delete("/strings/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
def delete_string(string_value: str, db: Session = Depends(get_db)):
    string = db.query(models.Strings).where(models.Strings.value==string_value).first()
    if string is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"String {string_value} not found!"
        )
    db.delete(string)
    db.commit()
    return 

