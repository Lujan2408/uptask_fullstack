# Main entry point for the FastAPI application
from fastapi import FastAPI
from src.core.db import lifespan
from src.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from src.routes.project_routes import api_router
from src.core.middleware.logging_middleware import LoggingMiddleware
from src.middleware.validation import validation_middleware

# Create FastAPI app    
app = FastAPI(lifespan=lifespan)

# Include routes
app.include_router(api_router, prefix="/api")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Add validation middleware
app.middleware("http")(validation_middleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)