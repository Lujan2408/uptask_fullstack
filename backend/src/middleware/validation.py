# Validate request
from fastapi import Request, HTTPException
from typing import Callable
import json

async def validation_middleware(request: Request, call_next: Callable):
    # Validations before processing the request
    if request.method == "POST":
        # Validate Content-Type
        if "application/json" not in request.headers.get("content-type", ""):
            raise HTTPException(status_code=400, detail="Content-Type must be application/json")
        
        # Validate that the body is not empty
        try:
            body = await request.body()
            if not body:
                raise HTTPException(status_code=400, detail="Request body cannot be empty")
            
            # Validate that the body is a valid JSON
            json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    # Validate required headers
    if not request.headers.get("user-agent"):
        raise HTTPException(status_code=400, detail="User-Agent header is required")
    
    # Continue with the request if all validations pass
    response = await call_next(request)
    return response